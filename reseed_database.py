#!/usr/bin/env python3
"""
Script to reseed the database with updated agent configurations.
This ensures the Arabic RFP Generator uses the template-based approach.
"""

import os
import sys
from pathlib import Path

# Add application directory to path
sys.path.insert(0, str(Path(__file__).parent / "application"))

from dotenv import load_dotenv
from pymongo import MongoClient
from application.seed.seeder import DatabaseSeeder

# Load environment variables
load_dotenv()

def main():
    """Reseed the database with updated agent configurations"""
    print("Starting database reseeding process...")

    # Get MongoDB connection details
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/rfpagent")
    db_name = os.getenv("MONGO_DB_NAME", "rfpagent")

    print(f"Connecting to MongoDB at: {mongo_uri}")
    print(f"Database: {db_name}")

    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]

        # Create seeder instance
        seeder = DatabaseSeeder(db)

        # Force reseed to ensure updated configuration is applied
        print("\nReseeding database with force=True to apply updated agent configurations...")
        seeder.seed_initial_data(force=True)

        print("\n✅ Database reseeding completed successfully!")
        print("\nThe Arabic RFP Generator agent has been updated to:")
        print("- Use the template file: كراسة تطبيق أتمتة خدمات تقنية المعلومات للمركز (المرحلة الأولى).docx")
        print("- Fill the template with user-provided project details")
        print("- Generate a download button for the completed document")
        print("\nYou can now restart the application to use the updated agent.")

    except Exception as e:
        print(f"\n❌ Error during reseeding: {str(e)}")
        print("\nPlease ensure:")
        print("1. MongoDB is running (docker compose up mongo)")
        print("2. The MONGO_URI environment variable is correctly set")
        print("3. You have the necessary permissions to connect to the database")
        sys.exit(1)

if __name__ == "__main__":
    main()