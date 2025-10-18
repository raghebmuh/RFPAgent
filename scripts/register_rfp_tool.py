"""
Script to register the RFP Reference Tool in the database
This will make it available in the UI tools dropdown
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from application.api.user.base import user_tools_collection, db
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def register_rfp_tool():
    """Register the RFP Reference Tool in the database"""

    # Connect to MongoDB
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB_NAME", "docsgpt")

    client = MongoClient(mongo_uri)
    database = client[db_name]
    tools_collection = database["user_tools"]

    # Define the RFP tool
    rfp_tool = {
        "name": "rfp_reference_tool",
        "display_name": "RFP Reference Tool",
        "description": "Search for RFP examples, best practices, and compliance requirements",
        "type": "custom",
        "category": "document",
        "enabled": True,
        "config": {
            "actions": [
                {
                    "name": "search",
                    "description": "Search RFP knowledge base",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "search_type": {
                                "type": "string",
                                "enum": ["similar_rfp", "best_practices", "compliance", "templates"],
                                "default": "similar_rfp"
                            }
                        },
                        "required": ["query"]
                    }
                }
            ]
        },
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

    # Check if tool already exists
    existing = tools_collection.find_one({"name": "rfp_reference_tool"})

    if existing:
        # Update existing tool
        tools_collection.update_one(
            {"name": "rfp_reference_tool"},
            {"$set": rfp_tool}
        )
        print("✅ RFP Reference Tool updated in database")
    else:
        # Insert new tool
        tools_collection.insert_one(rfp_tool)
        print("✅ RFP Reference Tool registered in database")

    print("The tool should now appear in the UI dropdown")

    return True


if __name__ == "__main__":
    success = register_rfp_tool()
    if success:
        print("\n🎉 Tool registration complete!")
        print("Please refresh the UI and check the tools dropdown again.")