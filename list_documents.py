"""
Script to list all generated RFP documents
Run this to see all documents in your database
"""
import pymongo
from datetime import datetime
import json

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["rfpagent"]

# Get all documents
documents = list(db.user_documents.find({}, {"_id": 0}).sort("created_at", -1))

print("=" * 80)
print(f"📄 GENERATED RFP DOCUMENTS ({len(documents)} total)")
print("=" * 80)

if not documents:
    print("\n⚠️  No documents found yet!")
    print("   Generate a document using the Arabic RFP Generator agent first.\n")
else:
    for idx, doc in enumerate(documents, 1):
        print(f"\n{idx}. {doc.get('title', 'Untitled')}")
        print(f"   Doc ID: {doc.get('doc_id')}")
        print(f"   File: {doc.get('file_name', 'N/A')}")
        print(f"   Created: {doc.get('created_at', 'N/A')}")
        print(f"   User: {doc.get('user', 'N/A')}")
        print(f"   Sections: {len(doc.get('sections', []))}")
        if doc.get('file_path'):
            print(f"   Path: {doc.get('file_path')}")
        print(f"   Download: http://localhost:7091/api/documents/download/{doc.get('doc_id')}")

print("\n" + "=" * 80)

client.close()
