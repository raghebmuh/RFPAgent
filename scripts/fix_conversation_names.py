"""
Migration script to fix conversations with missing or empty names.

This script:
1. Finds all conversations with missing or empty names
2. Updates them with a name based on the first question
3. Logs the changes made

Usage:
    python scripts/fix_conversation_names.py
"""

import sys
from pathlib import Path

# Add parent directory to path to import application modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from application.core.mongo_db import MongoDB
from application.core.settings import settings


def fix_conversation_names():
    """Fix conversations with missing or empty names."""
    mongo = MongoDB.get_client()
    db = mongo[settings.MONGO_DB_NAME]
    conversations_collection = db["conversations"]

    # Find conversations with missing or empty names
    conversations = conversations_collection.find({
        "$or": [
            {"name": {"$exists": False}},
            {"name": ""},
            {"name": None}
        ]
    })

    updated_count = 0
    error_count = 0

    for conversation in conversations:
        try:
            conversation_id = conversation["_id"]

            # Generate name from first query
            if "queries" in conversation and len(conversation["queries"]) > 0:
                first_query = conversation["queries"][0]
                question = first_query.get("prompt", "")

                if question:
                    # Use first 30 characters of question
                    new_name = question[:30] + ("..." if len(question) > 30 else "")
                else:
                    new_name = "Untitled Chat"
            else:
                new_name = "Untitled Chat"

            # Update the conversation
            result = conversations_collection.update_one(
                {"_id": conversation_id},
                {"$set": {"name": new_name}}
            )

            if result.modified_count > 0:
                print(f"✓ Updated conversation {conversation_id}: '{new_name}'")
                updated_count += 1
            else:
                print(f"○ No update needed for conversation {conversation_id}")

        except Exception as e:
            print(f"✗ Error updating conversation {conversation.get('_id', 'unknown')}: {str(e)}")
            error_count += 1

    print(f"\n{'='*60}")
    print(f"Migration complete!")
    print(f"{'='*60}")
    print(f"Conversations updated: {updated_count}")
    print(f"Errors encountered: {error_count}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    print("Starting conversation names migration...\n")
    fix_conversation_names()
