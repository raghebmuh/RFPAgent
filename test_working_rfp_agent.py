#!/usr/bin/env python
"""
Test script to verify WorkingRFPAgent with document generation and download functionality
"""

import sys
import os
from pathlib import Path

# Add application to path
sys.path.insert(0, str(Path(__file__).parent))

def test_rfp_agent():
    """Test the WorkingRFPAgent"""

    print("=" * 70)
    print("RFP Agent Test - Document Generation & Download")
    print("=" * 70)

    # Test imports
    print("\n1. Testing imports...")
    try:
        from application.agents.working_rfp_agent import WorkingRFPAgent
        print("✅ WorkingRFPAgent imported successfully")
    except Exception as e:
        print(f"❌ Failed to import WorkingRFPAgent: {e}")
        return

    # Test agent creation
    print("\n2. Creating agent instance...")
    try:
        agent = WorkingRFPAgent(
            name="RFP Agent",
            description="Agent for RFP document generation",
            llm_config={
                "provider": "openai",
                "model": "gpt-3.5-turbo",
                "api_key": os.getenv("API_KEY", "test-key")
            }
        )
        print(f"✅ Agent created successfully")
        print(f"   Template path: {agent.template_path}")
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        return

    # Test message with RFP data
    print("\n3. Processing RFP request...")
    test_message = """
    اسم المنافسة: تطوير نظام إدارة المحتوى الرقمي
    رقم المنافسة: RFP-2025-001
    موعد التسليم: 15/12/2025
    موعد الفتح: 20/12/2025
    مكان التنفيذ: الرياض
    وصف النشاط: تطوير وتنفيذ نظام متكامل لإدارة المحتوى الرقمي يشمل إدارة الوثائق والملفات والأرشفة الإلكترونية
    """

    try:
        # Run the agent
        response_generator = agent.run(test_message)
        full_response = ""

        for chunk in response_generator:
            full_response += chunk

        print("✅ Agent processed the request")

        # Check if document block is in response
        if "```document" in full_response:
            print("✅ Document metadata block found in response")

            # Extract document metadata
            import json
            import re
            doc_match = re.search(r'```document\n({[^}]+})\n```', full_response, re.DOTALL)
            if doc_match:
                try:
                    doc_data = json.loads(doc_match.group(1))
                    print(f"✅ Document ID: {doc_data.get('doc_id')}")
                    print(f"✅ Document Title: {doc_data.get('title')}")
                    print(f"✅ Download URL: {doc_data.get('download_url')}")
                except:
                    print("⚠️ Could not parse document metadata")
        else:
            print("⚠️ No document block found in response")

        # Print response preview
        print("\n4. Response preview:")
        print("-" * 50)
        print(full_response[:500] + "..." if len(full_response) > 500 else full_response)
        print("-" * 50)

    except Exception as e:
        print(f"❌ Failed to process message: {e}")
        import traceback
        traceback.print_exc()

    # Check if document file was created
    print("\n5. Checking document file...")
    outputs_dir = "outputs/rfp_documents"
    if os.path.exists(outputs_dir):
        files = list(Path(outputs_dir).glob("*.docx"))
        if files:
            print(f"✅ Found {len(files)} document(s) in {outputs_dir}")
            for f in files[-3:]:  # Show last 3 files
                print(f"   - {f.name}")
        else:
            print(f"⚠️ No documents found in {outputs_dir}")
    else:
        print(f"⚠️ Output directory {outputs_dir} does not exist")

    print("\n" + "=" * 70)
    print("✅ Test completed!")
    print("\nNext steps:")
    print("1. Restart Docker services: docker-compose up")
    print("2. Create an RFP agent in the UI with type 'rfp'")
    print("3. Send an Arabic RFP request to the agent")
    print("4. Look for the document download button in the response")
    print("=" * 70)


if __name__ == "__main__":
    test_rfp_agent()