"""
End-to-end test script for RFP Agent workflow
Tests the complete flow from data collection to document generation
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from application.services.docx_placeholder_service import DocxPlaceholderService
from application.services.rfp_content_generator import RFPContentGenerator
from application.services.docx_filler_service import DocxFillerService
from application.models.rfp_placeholders import RFPPlaceholders


def test_placeholder_extraction():
    """Test 1: Extract placeholders from template"""
    print("\n" + "="*50)
    print("Test 1: Extracting Placeholders from Template")
    print("="*50)

    template_path = "inputs/templates/rfp_template_with_placeholders.docx"

    try:
        service = DocxPlaceholderService(template_path)
        placeholders = service.extract_placeholders()
        dropdowns = service.extract_dropdown_fields()

        print(f"✅ Successfully extracted {len(placeholders)} placeholders")
        print(f"✅ Found {len(dropdowns)} dropdown fields")

        # Show sample placeholders
        print("\nSample placeholders:")
        for i, (name, info) in enumerate(list(placeholders.items())[:5]):
            print(f"  - {{{{name}}}}: appears {info.count} times")

        return True

    except Exception as e:
        print(f"❌ Failed to extract placeholders: {e}")
        return False


def test_content_generation():
    """Test 2: Generate content for placeholders"""
    print("\n" + "="*50)
    print("Test 2: Generating Content for Placeholders")
    print("="*50)

    # Sample project data
    project_data = {
        "entity_name": "وزارة الصحة",
        "project_name": "نظام إدارة المواعيد الإلكتروني",
        "tender_number": "2024-001",
        "project_type": "تقنية المعلومات",
        "duration_months": 6,
        "project_scope": "تطوير نظام متكامل لإدارة المواعيد الطبية",
        "training_required": "نعم",
        "payment_method": "دفعات حسب المراحل",
        "technical_weight": 60,
        "financial_weight": 40
    }

    try:
        generator = RFPContentGenerator()

        # Test generating content for special placeholders
        scope_content = generator.generate_content("project_scope", project_data)
        phases_content = generator.generate_content("work_program_phases", project_data)
        payment_content = generator.generate_content("work_program_payment_method", project_data)

        print("✅ Successfully generated content for placeholders")
        print(f"\nGenerated project scope (first 200 chars):")
        print(f"  {scope_content[:200]}...")

        print(f"\nGenerated phases (first 200 chars):")
        print(f"  {phases_content[:200]}...")

        return True

    except Exception as e:
        print(f"❌ Failed to generate content: {e}")
        return False


def test_document_filling():
    """Test 3: Fill template with data"""
    print("\n" + "="*50)
    print("Test 3: Filling Template with Data")
    print("="*50)

    # Complete project data
    project_data = {
        "entity_name": "وزارة الصحة",
        "project_name": "نظام إدارة المواعيد الإلكتروني",
        "tender_number": "2024-001",
        "project_type": "تقنية المعلومات",
        "duration_months": 6,
        "project_scope": "تطوير نظام متكامل لإدارة المواعيد الطبية في جميع المستشفيات التابعة للوزارة",
        "project_objectives": "أتمتة عملية حجز المواعيد وتحسين تجربة المرضى",
        "deliverables": "نظام ويب متكامل، تطبيقات موبايل، لوحة تحكم إدارية",
        "requirements": "خبرة في تطوير الأنظمة الطبية، فريق متخصص، دعم فني مستمر",
        "budget_range": "1,000,000 - 2,000,000 ريال سعودي",
        "training_required": "نعم",
        "location": "الرياض",
        "contact_department": "إدارة تقنية المعلومات",
        "contact_email": "it@moh.gov.sa",
        "submission_deadline": "2024-12-31",
        "warranty_period": "24 شهر",
        "local_content_percentage": 40,
        "payment_method": "دفعات حسب المراحل",
        "technical_weight": 60,
        "financial_weight": 40
    }

    template_path = "inputs/templates/rfp_template_with_placeholders.docx"
    output_path = f"outputs/test_rfp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"

    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Fill the template
        filler_service = DocxFillerService(template_path)
        generated_path = filler_service.fill_template(project_data, output_path)

        print(f"✅ Successfully generated RFP document")
        print(f"📄 Document saved to: {generated_path}")

        # Generate preview
        preview = filler_service.generate_preview_text(project_data)
        print(f"\nDocument preview (first 300 chars):")
        print(f"  {preview[:300]}...")

        return True

    except Exception as e:
        print(f"❌ Failed to fill template: {e}")
        return False


def test_validation():
    """Test 4: Validate data completeness"""
    print("\n" + "="*50)
    print("Test 4: Validating Data Completeness")
    print("="*50)

    # Incomplete data (missing some required fields)
    incomplete_data = {
        "entity_name": "وزارة الصحة",
        "project_name": "نظام إدارة المواعيد",
        # Missing: tender_number, project_scope, duration_months, etc.
    }

    template_path = "inputs/templates/rfp_template_with_placeholders.docx"

    try:
        service = DocxPlaceholderService(template_path)
        service.extract_placeholders()

        is_valid, missing_fields = service.validate_placeholder_data(incomplete_data)

        print(f"✅ Validation completed")
        print(f"  Is valid: {is_valid}")
        print(f"  Missing fields ({len(missing_fields)}):")

        # Get questions for missing fields
        questions = RFPPlaceholders.get_questions_for_missing_data(missing_fields[:5])
        for q in questions:
            print(f"    - {q['arabic_name']}: {q['question']}")

        return True

    except Exception as e:
        print(f"❌ Failed to validate data: {e}")
        return False


def test_rfp_agent_integration():
    """Test 5: Test RFP Agent integration"""
    print("\n" + "="*50)
    print("Test 5: Testing RFP Agent Integration")
    print("="*50)

    try:
        from application.agents.rfp_agent import RFPAgent, create_rfp_agent_config

        # Get agent configuration
        config = create_rfp_agent_config()

        print("✅ RFP Agent configuration created")
        print(f"  Name: {config['name']}")
        print(f"  Type: {config['agent_type']}")
        print(f"  Tools: {config['tools']}")

        # Test agent initialization (simplified, without full dependencies)
        print("\n✅ RFP Agent class is properly defined")

        return True

    except Exception as e:
        print(f"❌ Failed to test RFP Agent: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("RFP AGENT END-TO-END WORKFLOW TEST")
    print("="*60)

    tests = [
        ("Placeholder Extraction", test_placeholder_extraction),
        ("Content Generation", test_content_generation),
        ("Document Filling", test_document_filling),
        ("Data Validation", test_validation),
        ("RFP Agent Integration", test_rfp_agent_integration)
    ]

    results = []

    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with error: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {test_name}: {status}")

    print("\n" + "-"*60)
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! RFP Agent is ready for use.")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Please review the errors above.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)