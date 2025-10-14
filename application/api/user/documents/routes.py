"""Document management API routes for RFP document generation and download"""

import logging
import os
from pathlib import Path

from bson.objectid import ObjectId
from flask import current_app, jsonify, make_response, request, send_file
from flask_restx import fields, Namespace, Resource

from application.api import api
from application.api.user.base import user_documents_collection
from application.cache import get_redis_instance

logger = logging.getLogger(__name__)

documents_ns = Namespace(
    "documents", description="Document management operations", path="/api/documents"
)


# Document model for API documentation
document_model = api.model(
    "DocumentModel",
    {
        "doc_id": fields.String(required=True, description="Document ID from MCP server"),
        "title": fields.String(required=True, description="Document title"),
        "conversation_id": fields.String(
            required=False, description="Associated conversation ID"
        ),
        "file_path": fields.String(required=False, description="File path on server"),
        "file_name": fields.String(required=False, description="File name"),
    },
)


@documents_ns.route("/download/<string:doc_id>")
class DownloadDocument(Resource):
    @api.doc(description="Download a generated Word document")
    def get(self, doc_id):
        """Download a Word document by document ID"""
        try:
            decoded_token = request.decoded_token
            if not decoded_token:
                return make_response(jsonify({"success": False}), 401)

            user = decoded_token.get("sub")

            # Get document metadata from MongoDB
            document = user_documents_collection.find_one(
                {"doc_id": doc_id, "user": user}
            )

            if not document:
                return make_response(
                    jsonify({"success": False, "error": "Document not found"}), 404
                )

            file_path = document.get("file_path")
            file_name = document.get("file_name", f"document_{doc_id[:8]}.docx")

            # Check if file exists at original path or in mounted MCP documents volume
            if file_path and not Path(file_path).exists():
                # Try alternate path in mounted volume
                alt_file_path = Path("/app/mcp_documents") / Path(file_path).name
                if alt_file_path.exists():
                    file_path = str(alt_file_path)

            if not file_path or not Path(file_path).exists():
                return make_response(
                    jsonify(
                        {
                            "success": False,
                            "error": "Document file not found on server",
                        }
                    ),
                    404,
                )

            # Send file for download
            return send_file(
                file_path,
                as_attachment=True,
                download_name=file_name,
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

        except Exception as e:
            logger.error(f"Error downloading document: {e}", exc_info=True)
            return make_response(
                jsonify({"success": False, "error": f"Download failed: {str(e)}"}), 500
            )


@documents_ns.route("/preview/<string:doc_id>")
class PreviewDocument(Resource):
    @api.doc(description="Get document preview information")
    def get(self, doc_id):
        """Get preview information for a document"""
        try:
            decoded_token = request.decoded_token
            if not decoded_token:
                return make_response(jsonify({"success": False}), 401)

            user = decoded_token.get("sub")

            # Get document metadata from MongoDB
            document = user_documents_collection.find_one(
                {"doc_id": doc_id, "user": user}
            )

            if not document:
                return make_response(
                    jsonify({"success": False, "error": "Document not found"}), 404
                )

            # Return document preview information
            preview = {
                "success": True,
                "doc_id": document.get("doc_id"),
                "title": document.get("title"),
                "file_name": document.get("file_name"),
                "created_at": str(document.get("created_at")),
                "conversation_id": document.get("conversation_id"),
                "preview_text": document.get("preview_text", ""),
                "sections": document.get("sections", []),
            }

            return make_response(jsonify(preview), 200)

        except Exception as e:
            logger.error(f"Error getting document preview: {e}", exc_info=True)
            return make_response(
                jsonify({"success": False, "error": f"Preview failed: {str(e)}"}), 500
            )


@documents_ns.route("/list")
class ListDocuments(Resource):
    @api.doc(description="List all documents for the current user")
    def get(self):
        """List all documents created by the user"""
        try:
            decoded_token = request.decoded_token
            if not decoded_token:
                return make_response(jsonify({"success": False}), 401)

            user = decoded_token.get("sub")

            # Get all documents for user
            documents = list(
                user_documents_collection.find(
                    {"user": user}, {"_id": 0}
                ).sort("created_at", -1)
            )

            return make_response(
                jsonify({"success": True, "count": len(documents), "documents": documents}),
                200,
            )

        except Exception as e:
            logger.error(f"Error listing documents: {e}", exc_info=True)
            return make_response(
                jsonify({"success": False, "error": f"List failed: {str(e)}"}), 500
            )


@documents_ns.route("/save")
class SaveDocumentMetadata(Resource):
    @api.expect(document_model)
    @api.doc(description="Save document metadata to database")
    def post(self):
        """Save document metadata after generation"""
        try:
            decoded_token = request.decoded_token
            if not decoded_token:
                return make_response(jsonify({"success": False}), 401)

            user = decoded_token.get("sub")
            data = request.get_json()

            # Validate required fields
            required_fields = ["doc_id", "title"]
            for field in required_fields:
                if field not in data:
                    return make_response(
                        jsonify({"success": False, "error": f"Missing field: {field}"}),
                        400,
                    )

            # Create document metadata
            document_data = {
                "doc_id": data["doc_id"],
                "title": data["title"],
                "file_path": data.get("file_path"),
                "file_name": data.get("file_name"),
                "conversation_id": data.get("conversation_id"),
                "preview_text": data.get("preview_text", ""),
                "sections": data.get("sections", []),
                "user": user,
                "created_at": data.get("created_at"),
            }

            # Check if document already exists
            existing = user_documents_collection.find_one(
                {"doc_id": data["doc_id"], "user": user}
            )

            if existing:
                # Update existing document
                user_documents_collection.update_one(
                    {"doc_id": data["doc_id"], "user": user}, {"$set": document_data}
                )
                message = "Document metadata updated"
            else:
                # Insert new document
                user_documents_collection.insert_one(document_data)
                message = "Document metadata saved"

            return make_response(
                jsonify({"success": True, "message": message, "doc_id": data["doc_id"]}),
                200,
            )

        except Exception as e:
            logger.error(f"Error saving document metadata: {e}", exc_info=True)
            return make_response(
                jsonify({"success": False, "error": f"Save failed: {str(e)}"}), 500
            )


@documents_ns.route("/delete/<string:doc_id>")
class DeleteDocument(Resource):
    @api.doc(description="Delete a document")
    def delete(self, doc_id):
        """Delete a document and its file"""
        try:
            decoded_token = request.decoded_token
            if not decoded_token:
                return make_response(jsonify({"success": False}), 401)

            user = decoded_token.get("sub")

            # Get document metadata
            document = user_documents_collection.find_one(
                {"doc_id": doc_id, "user": user}
            )

            if not document:
                return make_response(
                    jsonify({"success": False, "error": "Document not found"}), 404
                )

            # Delete file if exists
            file_path = document.get("file_path")
            if file_path and Path(file_path).exists():
                try:
                    Path(file_path).unlink()
                except Exception as e:
                    logger.warning(f"Could not delete file {file_path}: {e}")

            # Delete from database
            user_documents_collection.delete_one({"doc_id": doc_id, "user": user})

            return make_response(
                jsonify({"success": True, "message": "Document deleted"}), 200
            )

        except Exception as e:
            logger.error(f"Error deleting document: {e}", exc_info=True)
            return make_response(
                jsonify({"success": False, "error": f"Delete failed: {str(e)}"}), 500
            )
