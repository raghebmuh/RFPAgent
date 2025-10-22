"""Document management API routes for RFP document generation and download"""

import logging
import os
import uuid
from pathlib import Path
from datetime import datetime

from bson.objectid import ObjectId
from flask import current_app, jsonify, make_response, request, send_file
from flask_restx import fields, Namespace, Resource

from application.api import api
from application.api.user.base import user_documents_collection
from application.cache import get_redis_instance
from application.services.docx_filler_service import DocxFillerService
from application.services.docx_placeholder_service import DocxPlaceholderService
from application.services.rfp_content_generator import RFPContentGenerator

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
            # Try to get authenticated user, but allow system documents
            decoded_token = request.decoded_token
            user = decoded_token.get("sub") if decoded_token else None

            # Try to get document metadata from MongoDB
            document = None
            if user:
                document = user_documents_collection.find_one(
                    {"doc_id": doc_id, "user": user}
                )

            file_path = None
            file_name = f"document_{doc_id[:8]}.docx"

            if document:
                # Use metadata from MongoDB if available
                file_path = document.get("file_path")
                file_name = document.get("file_name", file_name)

                # Check if file exists at original path
                if file_path and not Path(file_path).exists():
                    # Try alternate path in mounted volume
                    alt_file_path = Path("/app/mcp_documents") / Path(file_path).name
                    if alt_file_path.exists():
                        file_path = str(alt_file_path)
                    else:
                        file_path = None

            # If no metadata or file not found, try to find file in mounted volume by doc_id
            if not file_path:
                logger.info(f"No metadata found for doc_id {doc_id}, searching in mounted volume")
                mcp_docs_dir = Path("/app/mcp_documents")

                # Search for files containing the doc_id prefix (first 8 chars)
                doc_id_prefix = doc_id[:8] if len(doc_id) >= 8 else doc_id
                matching_files = list(mcp_docs_dir.glob(f"*{doc_id_prefix}*.docx"))

                if matching_files:
                    # Use the most recently modified file
                    file_path = str(max(matching_files, key=lambda p: p.stat().st_mtime))
                    file_name = Path(file_path).name
                    logger.info(f"Found document file: {file_path}")

            if not file_path or not Path(file_path).exists():
                return make_response(
                    jsonify(
                        {
                            "success": False,
                            "error": "Document file not found. The document may not have been saved yet.",
                        }
                    ),
                    404,
                )

            # Send file for download
            response = send_file(
                file_path,
                as_attachment=True,
                download_name=file_name,
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            
            # Add additional headers for better download handling
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
            
            return response

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


# RFP-specific endpoints

# RFP data model for API documentation
rfp_data_model = api.model(
    "RFPDataModel",
    {
        "entity_name": fields.String(required=True, description="Government entity name"),
        "project_name": fields.String(required=True, description="Project name"),
        "tender_number": fields.String(required=True, description="Tender number"),
        "project_scope": fields.String(required=True, description="Project scope description"),
        "project_type": fields.String(description="Project type: IT, construction, consulting, etc."),
        "duration_months": fields.Integer(description="Project duration in months"),
        "conversation_id": fields.String(description="Associated conversation ID"),
        "placeholders": fields.Raw(description="All placeholder data as key-value pairs"),
    },
)


@documents_ns.route("/rfp/generate")
class GenerateRFPDocument(Resource):
    @api.expect(rfp_data_model)
    @api.doc(description="Generate an RFP document from template and data")
    def post(self):
        """Generate an RFP document by filling the template with provided data"""
        try:
            decoded_token = request.decoded_token
            if not decoded_token:
                return make_response(jsonify({"success": False}), 401)

            user = decoded_token.get("sub")
            data = request.get_json()

            # Validate required fields
            required_fields = ["entity_name", "project_name", "project_scope"]
            for field in required_fields:
                if field not in data or not data[field]:
                    return make_response(
                        jsonify({"success": False, "error": f"Missing required field: {field}"}),
                        400,
                    )

            # Get all placeholder data
            placeholder_data = data.get("placeholders", {})

            # Merge specific fields into placeholder data
            for key in ["entity_name", "project_name", "tender_number", "project_scope",
                       "project_type", "duration_months"]:
                if key in data:
                    placeholder_data[key] = data[key]

            # Generate document ID
            doc_id = str(uuid.uuid4())[:8]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Define paths
            template_path = os.path.join("inputs", "templates", "rfp_template_with_placeholders.docx")
            output_dir = os.path.join("outputs", "rfp_documents", user)
            os.makedirs(output_dir, exist_ok=True)

            file_name = f"RFP_{data['project_name'][:20].replace(' ', '_')}_{timestamp}.docx"
            output_path = os.path.join(output_dir, file_name)

            # Generate the document
            filler_service = DocxFillerService(template_path)
            generated_path = filler_service.fill_template(placeholder_data, output_path)

            # Get document sections for preview
            sections = filler_service.get_document_sections()

            # Generate preview text
            preview_text = filler_service.generate_preview_text(placeholder_data)

            # Save metadata to database
            document_data = {
                "doc_id": doc_id,
                "title": f"RFP - {data['project_name']}",
                "file_path": generated_path,
                "file_name": file_name,
                "conversation_id": data.get("conversation_id"),
                "preview_text": preview_text[:1000],  # Store first 1000 chars
                "sections": sections,
                "user": user,
                "created_at": datetime.now(),
                "document_type": "rfp",
                "metadata": {
                    "entity_name": data.get("entity_name"),
                    "project_name": data.get("project_name"),
                    "tender_number": data.get("tender_number"),
                    "project_type": data.get("project_type"),
                    "duration_months": data.get("duration_months"),
                }
            }

            user_documents_collection.insert_one(document_data)

            return make_response(
                jsonify({
                    "success": True,
                    "doc_id": doc_id,
                    "file_name": file_name,
                    "sections": sections,
                    "preview_text": preview_text[:500],
                    "message": "تم إنشاء وثيقة RFP بنجاح"
                }),
                200,
            )

        except Exception as e:
            logger.error(f"Error generating RFP document: {e}", exc_info=True)
            return make_response(
                jsonify({"success": False, "error": f"RFP generation failed: {str(e)}"}),
                500,
            )


@documents_ns.route("/rfp/placeholders")
class GetRFPPlaceholders(Resource):
    @api.doc(description="Get all placeholders from the RFP template")
    def get(self):
        """Extract and return all placeholders from the RFP template"""
        try:
            decoded_token = request.decoded_token
            if not decoded_token:
                return make_response(jsonify({"success": False}), 401)

            # Extract placeholders from template
            template_path = os.path.join("inputs", "templates", "rfp_template_with_placeholders.docx")
            placeholder_service = DocxPlaceholderService(template_path)

            placeholders = placeholder_service.extract_placeholders()
            dropdown_fields = placeholder_service.extract_dropdown_fields()
            summary = placeholder_service.get_placeholder_summary()

            # Get placeholder definitions
            from application.models.rfp_placeholders import RFPPlaceholders
            all_definitions = RFPPlaceholders.get_all_placeholders()

            # Build response with definitions
            placeholder_info = {}
            for name, info in placeholders.items():
                definition = all_definitions.get(name)
                placeholder_info[name] = {
                    "count": info.count,
                    "locations": info.locations,
                    "required": info.is_required,
                    "description": info.description,
                    "special_instructions": info.special_instructions,
                    "arabic_name": definition.arabic_name if definition else "",
                    "type": definition.type.value if definition else "text",
                    "example": definition.example if definition else None,
                    "question": definition.question_prompt if definition else None,
                }

            return make_response(
                jsonify({
                    "success": True,
                    "placeholders": placeholder_info,
                    "dropdown_fields": [
                        {
                            "location": field.location,
                            "text": field.text,
                            "options": field.options
                        } for field in dropdown_fields
                    ],
                    "summary": summary,
                    "total_placeholders": len(placeholders),
                    "required_count": len([p for p in placeholders.values() if p.is_required])
                }),
                200,
            )

        except Exception as e:
            logger.error(f"Error extracting placeholders: {e}", exc_info=True)
            return make_response(
                jsonify({"success": False, "error": f"Placeholder extraction failed: {str(e)}"}),
                500,
            )


@documents_ns.route("/rfp/preview")
class PreviewRFPDocument(Resource):
    @api.expect(rfp_data_model)
    @api.doc(description="Generate a preview of the RFP document without saving")
    def post(self):
        """Generate a text preview of the RFP document"""
        try:
            decoded_token = request.decoded_token
            if not decoded_token:
                return make_response(jsonify({"success": False}), 401)

            data = request.get_json()

            # Get all placeholder data
            placeholder_data = data.get("placeholders", {})

            # Merge specific fields
            for key in ["entity_name", "project_name", "tender_number", "project_scope",
                       "project_type", "duration_months"]:
                if key in data:
                    placeholder_data[key] = data[key]

            # Generate preview
            template_path = os.path.join("inputs", "templates", "rfp_template_with_placeholders.docx")
            filler_service = DocxFillerService(template_path)

            preview_text = filler_service.generate_preview_text(placeholder_data)
            sections = filler_service.get_document_sections()
            filled_content = filler_service.extract_filled_content(placeholder_data)

            return make_response(
                jsonify({
                    "success": True,
                    "preview_text": preview_text,
                    "sections": sections,
                    "filled_placeholders": list(filled_content.keys()),
                    "completion_percentage": int(
                        (len(filled_content) / 30) * 100  # Assuming ~30 placeholders
                    )
                }),
                200,
            )

        except Exception as e:
            logger.error(f"Error generating RFP preview: {e}", exc_info=True)
            return make_response(
                jsonify({"success": False, "error": f"Preview generation failed: {str(e)}"}),
                500,
            )


@documents_ns.route("/rfp/validate")
class ValidateRFPData(Resource):
    @api.expect(rfp_data_model)
    @api.doc(description="Validate RFP data completeness and correctness")
    def post(self):
        """Validate that all required RFP data is present and correct"""
        try:
            decoded_token = request.decoded_token
            if not decoded_token:
                return make_response(jsonify({"success": False}), 401)

            data = request.get_json()
            placeholder_data = data.get("placeholders", {})

            # Merge specific fields
            for key in ["entity_name", "project_name", "tender_number", "project_scope"]:
                if key in data:
                    placeholder_data[key] = data[key]

            # Validate using placeholder service
            template_path = os.path.join("inputs", "templates", "rfp_template_with_placeholders.docx")
            placeholder_service = DocxPlaceholderService(template_path)

            is_valid, missing_fields = placeholder_service.validate_placeholder_data(placeholder_data)

            # Get questions for missing fields
            from application.models.rfp_placeholders import RFPPlaceholders
            questions = RFPPlaceholders.get_questions_for_missing_data(missing_fields)

            return make_response(
                jsonify({
                    "success": True,
                    "is_valid": is_valid,
                    "missing_fields": missing_fields,
                    "questions": questions,
                    "completion_percentage": int(
                        ((30 - len(missing_fields)) / 30) * 100  # Assuming ~30 required fields
                    )
                }),
                200,
            )

        except Exception as e:
            logger.error(f"Error validating RFP data: {e}", exc_info=True)
            return make_response(
                jsonify({"success": False, "error": f"Validation failed: {str(e)}"}),
                500,
            )
