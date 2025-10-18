"""
Script to create an RFP Agent via the API
This can be used to set up the RFP Agent in the system
"""

import json
import requests
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from application.models.rfp_placeholders import get_rfp_json_schema


def create_rfp_agent(api_host="http://localhost:5000", token=None):
    """
    Create an RFP Agent through the API
    """

    # Read the RFP prompt
    prompt_path = Path(__file__).parent.parent / "application" / "prompts" / "rfp_agent_prompts.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        rfp_prompt = f.read()

    # Get the JSON schema for RFP
    json_schema = get_rfp_json_schema()

    # Agent configuration
    agent_data = {
        "name": "وكيل طلب تقديم العروض",
        "description": "وكيل متخصص في إنشاء وثائق طلب تقديم العروض (RFP) للمشاريع الحكومية السعودية. يقوم بجمع معلومات المشروع من خلال محادثة تفاعلية وإنشاء وثيقة RFP احترافية متوافقة مع الأنظمة الحكومية.",
        "agent_type": "react",  # Use react type, RFPAgent extends ReActAgent
        "chunks": 5,
        "retriever": "classic_rag",
        "prompt_id": "",  # Will use the prompt text directly
        "prompt_text": rfp_prompt,
        "sources": ["default"],
        "tools": ["rfp_reference_tool"],
        "json_schema": json_schema,
        "status": "published",
        "metadata": {
            "template_file": "rfp_template_with_placeholders.docx",
            "language": "ar",
            "region": "SA",
            "compliance": "Saudi Government Procurement",
            "version": "1.0",
            "features": [
                "Interactive data collection",
                "Progress tracking",
                "Automatic content generation",
                "Saudi compliance validation",
                "DOCX template filling",
                "Arabic RTL support"
            ]
        }
    }

    # API endpoint
    url = f"{api_host}/api/create_agent"

    # Headers
    headers = {
        "Content-Type": "application/json"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    # Make the request
    try:
        response = requests.post(url, json=agent_data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            print("✅ RFP Agent created successfully!")
            print(f"Agent ID: {result.get('id')}")
            print(f"Agent Name: {result.get('name')}")
            print("\nYou can now:")
            print("1. Start a new conversation with the RFP Agent")
            print("2. Provide project details in Arabic")
            print("3. Answer the agent's questions to complete data collection")
            print("4. Generate a professional RFP document")
            return result
        else:
            print(f"❌ Failed to create RFP Agent")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error creating RFP Agent: {e}")
        return None


def main():
    """
    Main function to run the script
    """
    import argparse

    parser = argparse.ArgumentParser(description="Create RFP Agent via API")
    parser.add_argument("--host", default="http://localhost:5000", help="API host URL")
    parser.add_argument("--token", help="Authentication token")

    args = parser.parse_args()

    print("Creating RFP Agent...")
    print("=" * 50)

    result = create_rfp_agent(args.host, args.token)

    if result:
        print("\n" + "=" * 50)
        print("RFP Agent Setup Complete!")
        print("=" * 50)

        # Save agent configuration for reference
        config_path = Path(__file__).parent / "rfp_agent_config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\nAgent configuration saved to: {config_path}")


if __name__ == "__main__":
    main()