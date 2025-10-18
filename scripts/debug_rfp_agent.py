"""
Debug script to identify RFP Agent issues
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))


def check_environment():
    """Check the environment and identify issues"""

    print("🔍 RFP Agent Diagnostic Tool")
    print("="*50)

    # Check 1: Python version
    print(f"\n1. Python Version: {sys.version}")

    # Check 2: Required modules
    print("\n2. Checking required modules:")
    modules_to_check = [
        ("docx", "python-docx"),
        ("arabic_reshaper", "arabic-reshaper"),
        ("bidi", "python-bidi")
    ]

    missing_modules = []
    for module_name, package_name in modules_to_check:
        try:
            __import__(module_name)
            print(f"   ✅ {package_name} is installed")
        except ImportError:
            print(f"   ❌ {package_name} is NOT installed")
            missing_modules.append(package_name)

    # Check 3: Template file
    print("\n3. Checking template file:")
    template_paths = [
        "inputs/templates/rfp_template_with_placeholders.docx",
        "/app/inputs/templates/rfp_template_with_placeholders.docx",
        "../inputs/templates/rfp_template_with_placeholders.docx"
    ]

    template_found = False
    for path in template_paths:
        if os.path.exists(path):
            print(f"   ✅ Template found at: {path}")
            template_found = True
            break

    if not template_found:
        print(f"   ❌ Template file NOT found in any of these locations:")
        for path in template_paths:
            print(f"      - {path}")

    # Check 4: Agent imports
    print("\n4. Checking agent imports:")
    try:
        from application.agents.react_agent import ReActAgent
        print("   ✅ ReActAgent imports successfully")
    except Exception as e:
        print(f"   ❌ ReActAgent import failed: {e}")

    try:
        from application.agents.rfp_agent import RFPAgent
        print("   ✅ RFPAgent imports successfully")
    except Exception as e:
        print(f"   ❌ RFPAgent import failed: {e}")

    try:
        from application.agents.simple_rfp_agent import SimpleRFPAgent
        print("   ✅ SimpleRFPAgent imports successfully")
    except Exception as e:
        print(f"   ❌ SimpleRFPAgent import failed: {e}")

    # Check 5: Directory structure
    print("\n5. Current directory structure:")
    print(f"   Current working directory: {os.getcwd()}")
    print(f"   Script location: {Path(__file__).parent}")

    # Recommendations
    print("\n" + "="*50)
    print("📋 RECOMMENDATIONS:")
    print("="*50)

    if missing_modules:
        print("\n1. Install missing modules:")
        print(f"   pip install {' '.join(missing_modules)}")

    if not template_found:
        print("\n2. Template file issue:")
        print("   The DOCX template file is not accessible.")
        print("   Solutions:")
        print("   - Use the SimpleRFPAgent which doesn't require files")
        print("   - Or mount the template directory in Docker:")
        print("     docker-compose.yml should include:")
        print("     volumes:")
        print("       - ./inputs:/app/inputs")

    print("\n3. Quick workaround:")
    print("   Change your agent type to 'react' instead of 'rfp'")
    print("   and use the conversation to guide the RFP creation")

    print("\n" + "="*50)


def test_rfp_processing():
    """Test RFP message processing"""
    print("\n6. Testing RFP message processing:")

    test_message = """اسم المنافسة: تطوير منظومة متكاملة من الملاحق والأدلة
رقم المنافسة: rfp-2025
موعد التسليم: 20/10/2025
مكان التنفيذ: الرياض"""

    try:
        from application.agents.rfp_fallback import RFPFallbackHandler
        result = RFPFallbackHandler.process_rfp_request(test_message)

        if result['success']:
            print("   ✅ Fallback handler works!")
            print(f"   Extracted data: {result['data']}")
        else:
            print(f"   ❌ Fallback handler failed: {result['message']}")

    except Exception as e:
        print(f"   ❌ Could not test fallback handler: {e}")


if __name__ == "__main__":
    check_environment()
    test_rfp_processing()

    print("\n" + "="*50)
    print("🏁 Diagnostic complete!")
    print("="*50)