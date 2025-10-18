"""
Working RFP Agent that uses the exact template file and generates downloadable documents
"""

import os
import json
import logging
import uuid
from typing import Dict, List, Any, Optional, Generator
from datetime import datetime
from pathlib import Path

from application.agents.react_agent import ReActAgent

logger = logging.getLogger(__name__)


class WorkingRFPAgent(ReActAgent):
    """
    RFP Agent that properly uses the template and generates downloadable documents
    """

    def __init__(self, *args, **kwargs):
        # Set default JSON schema for RFP if not provided
        if 'json_schema' not in kwargs or not kwargs['json_schema']:
            kwargs['json_schema'] = self.get_rfp_schema()

        super().__init__(*args, **kwargs)

        # RFP-specific attributes
        self.collected_data = {}
        self.conversation_state = "initial"
        self.completion_percentage = 0

        # Define template path - try multiple locations
        self.template_paths = [
            "/app/inputs/templates/rfp_template_with_placeholders.docx",  # Docker path
            "inputs/templates/rfp_template_with_placeholders.docx",  # Relative path
            "D:\\_Tec Solution\\AI Agents\\RFPAgent\\inputs\\templates\\rfp_template_with_placeholders.docx"  # Absolute Windows path
        ]

        self.template_path = None
        for path in self.template_paths:
            if os.path.exists(path):
                self.template_path = path
                logger.info(f"Found template at: {path}")
                break

    def get_rfp_schema(self):
        """Get RFP JSON schema"""
        return {
            "type": "object",
            "properties": {
                "entity_name": {"type": "string", "description": "اسم الجهة الحكومية"},
                "project_name": {"type": "string", "description": "اسم المشروع"},
                "tender_number": {"type": "string", "description": "رقم المنافسة"},
                "project_scope": {"type": "string", "description": "نطاق العمل"},
                "project_type": {"type": "string", "description": "نوع المشروع"},
                "duration_months": {"type": "number", "description": "مدة التنفيذ بالأشهر"},
                "location": {"type": "string", "description": "مكان التنفيذ"},
                "submission_deadline": {"type": "string", "description": "موعد التسليم"},
                "opening_date": {"type": "string", "description": "موعد الفتح"},
                "budget_range": {"type": "string", "description": "نطاق الميزانية"},
                "work_program_phases": {"type": "string", "description": "مراحل التنفيذ"},
                "work_program_payment_method": {"type": "string", "description": "طريقة الدفع"},
                "work_execution_method": {"type": "string", "description": "طريقة تنفيذ الأعمال"},
                "training_required": {"type": "string", "description": "هل التدريب مطلوب"},
                "warranty_period": {"type": "string", "description": "فترة الضمان"},
                "local_content_percentage": {"type": "number", "description": "نسبة المحتوى المحلي"}
            },
            "required": ["entity_name", "project_name", "project_scope"]
        }

    def extract_project_data(self, message: str) -> Dict[str, Any]:
        """Extract project data from user message"""
        data = {}

        # Extract from structured format
        lines = message.split('\n')
        for line in lines:
            # Look for numbered items with Arabic labels
            if '1️⃣' in line or '2️⃣' in line or '3️⃣' in line or '4️⃣' in line or '5️⃣' in line or '6️⃣' in line:
                # Remove emoji and extract key-value
                clean_line = line.replace('1️⃣', '').replace('2️⃣', '').replace('3️⃣', '')
                clean_line = clean_line.replace('4️⃣', '').replace('5️⃣', '').replace('6️⃣', '')

                if ':' in clean_line:
                    parts = clean_line.split(':', 1)
                    key = parts[0].strip()
                    value = parts[1].strip() if len(parts) > 1 else ""

                    # Map Arabic keys to placeholder names
                    mapping = {
                        "اسم المنافسة": "project_name",
                        "رقم المنافسة": "tender_number",
                        "موعد التسليم": "submission_deadline",
                        "موعد الفتح": "opening_date",
                        "مكان التنفيذ": "location",
                        "وصف النشاط": "project_scope",
                        "وصف الشغط": "project_scope",
                        "الجهة": "entity_name",
                        "اسم الجهة": "entity_name",
                        "المدة": "duration_months",
                        "الميزانية": "budget_range"
                    }

                    for ar_key, en_key in mapping.items():
                        if ar_key in key:
                            data[en_key] = value
                            break

            # Also check for simple key:value format
            elif ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()

                    mapping = {
                        "اسم المنافسة": "project_name",
                        "رقم المنافسة": "tender_number",
                        "موعد التسليم": "submission_deadline",
                        "موعد الفتح": "opening_date",
                        "مكان التنفيذ": "location",
                        "وصف النشاط": "project_scope",
                        "وصف الشغط": "project_scope",
                        "الجهة": "entity_name",
                        "اسم الجهة": "entity_name"
                    }

                    for ar_key, en_key in mapping.items():
                        if ar_key in key:
                            data[en_key] = value
                            break

        return data

    def generate_rfp_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content for placeholders based on provided data"""

        # Enhance the data with generated content for special placeholders
        enhanced_data = data.copy()

        # Generate project scope if too short
        if "project_scope" in enhanced_data and len(enhanced_data["project_scope"]) < 100:
            base_scope = enhanced_data["project_scope"]
            enhanced_data["project_scope"] = f"""{base_scope}

يتضمن نطاق العمل:
• دراسة وتحليل الوضع الحالي
• تصميم وتطوير الحلول المطلوبة
• التنفيذ والتطبيق
• الاختبار والتشغيل التجريبي
• التدريب ونقل المعرفة
• الدعم الفني والصيانة

مع الالتزام بجميع المعايير والمواصفات المعتمدة وعدم الإشارة إلى أي علامات تجارية محددة."""

        # Generate work phases if not provided
        if "work_program_phases" not in enhanced_data or not enhanced_data["work_program_phases"]:
            duration = enhanced_data.get("duration_months", 6)
            enhanced_data["work_program_phases"] = f"""برنامج العمل ومراحل التنفيذ:

المرحلة الأولى: الدراسة والتحليل - مدة شهر واحد
المرحلة الثانية: التصميم والتخطيط - مدة شهر واحد
المرحلة الثالثة: التنفيذ والتطوير - مدة {duration - 3} أشهر
المرحلة الرابعة: الاختبار والتسليم - مدة شهر واحد

إجمالي مدة التنفيذ: {duration} أشهر"""

        # Generate payment method if not provided
        if "work_program_payment_method" not in enhanced_data or not enhanced_data["work_program_payment_method"]:
            enhanced_data["work_program_payment_method"] = """طريقة الدفع:

يكون الدفع وفقاً لشهادة الإنجاز الصادرة من الإدارة المشرفة على التنفيذ مع تقديم الفواتير والمستندات المطلوبة.

الدفعة الأولى: 20% بعد توقيع العقد وتقديم ضمان حسن الأداء
الدفعة الثانية: 30% بعد إنجاز 50% من الأعمال
الدفعة الثالثة: 30% بعد إنجاز 80% من الأعمال
الدفعة الرابعة: 20% بعد التسليم النهائي واعتماد جميع المخرجات"""

        # Generate work execution method if not provided
        if "work_execution_method" not in enhanced_data or not enhanced_data["work_execution_method"]:
            enhanced_data["work_execution_method"] = """طريقة تنفيذ الأعمال:

الخدمات المطلوبة:
• تحليل المتطلبات وإعداد الخطط التنفيذية
• تطوير وتنفيذ الحلول المطلوبة
• إجراء الاختبارات الشاملة
• تقديم التدريب والدعم الفني

المواد والأدوات:
• استخدام أحدث التقنيات والأدوات المناسبة
• توفير جميع الموارد اللازمة للتنفيذ

معايير الجودة:
• الالتزام بالمعايير المعتمدة
• ضمان الجودة في جميع مراحل التنفيذ

الاختبارات المطلوبة:
• اختبارات الوظائف والأداء
• اختبارات القبول النهائي"""

        # Add default values for other fields
        defaults = {
            "entity_name": enhanced_data.get("entity_name", "[اسم الجهة]"),
            "tender_number": enhanced_data.get("tender_number", f"RFP-{datetime.now().year}-001"),
            "project_type": enhanced_data.get("project_type", "خدمات"),
            "warranty_period": enhanced_data.get("warranty_period", "12 شهر"),
            "local_content_percentage": enhanced_data.get("local_content_percentage", 30),
            "training_required": enhanced_data.get("training_required", "نعم"),
            "evaluation_criteria": """معايير التقييم:
• التقييم الفني: 60%
• التقييم المالي: 40%""",
            "required_certificates": """الشهادات المطلوبة:
• السجل التجاري ساري المفعول
• شهادة الزكاة والدخل
• شهادة التأمينات الاجتماعية
• شهادة الغرفة التجارية"""
        }

        for key, value in defaults.items():
            if key not in enhanced_data or not enhanced_data[key]:
                enhanced_data[key] = value

        return enhanced_data

    def generate_response_with_document(self, message: str) -> Dict[str, Any]:
        """Process message and generate RFP document"""

        # Extract data from message
        extracted_data = self.extract_project_data(message)
        self.collected_data.update(extracted_data)

        # Check if we have minimum required data
        required = ["project_name", "project_scope"]
        missing = [f for f in required if f not in self.collected_data or not self.collected_data[f]]

        if missing:
            # Ask for missing data
            questions = {
                "project_name": "ما هو اسم المشروع أو المنافسة؟",
                "project_scope": "يرجى وصف نطاق العمل والأنشطة المطلوبة",
                "entity_name": "ما هو اسم الجهة الحكومية؟",
                "tender_number": "ما هو رقم المنافسة؟"
            }

            response = "شكراً لك. لإكمال وثيقة RFP، أحتاج إلى المعلومات التالية:\n\n"
            for field in missing[:3]:
                if field in questions:
                    response += f"• {questions[field]}\n"

            return {
                "answer": response,
                "thought": "جمع البيانات المطلوبة",
                "sources": [],
                "error": ""
            }

        # Generate complete RFP data
        complete_data = self.generate_rfp_content(self.collected_data)

        # Try to generate DOCX document
        doc_info = self.create_rfp_document(complete_data)

        # Create response with document info
        response = f"""✅ تم إنشاء وثيقة RFP بنجاح!

📋 ملخص المعلومات:
• اسم المشروع: {complete_data.get('project_name', '')}
• رقم المنافسة: {complete_data.get('tender_number', '')}
• مكان التنفيذ: {complete_data.get('location', 'غير محدد')}
• موعد التسليم: {complete_data.get('submission_deadline', 'غير محدد')}

📄 الوثيقة جاهزة للتحميل بصيغة DOCX قابلة للتعديل.
"""

        # Return response with document metadata
        result = {
            "answer": response,
            "thought": "تم إنشاء وثيقة RFP",
            "sources": [],
            "error": "",
            "structured_output": complete_data
        }

        # Add document info if generation succeeded
        if doc_info and doc_info.get("success"):
            result["document"] = {
                "doc_id": doc_info["doc_id"],
                "title": f"RFP - {complete_data.get('project_name', 'Document')}",
                "file_name": doc_info.get("file_name", "rfp_document.docx"),
                "preview_text": response,
                "sections": [
                    {"heading": "معلومات المنافسة", "level": 1},
                    {"heading": "نطاق العمل", "level": 1},
                    {"heading": "مراحل التنفيذ", "level": 1},
                    {"heading": "طريقة الدفع", "level": 1},
                    {"heading": "المتطلبات", "level": 1}
                ],
                "type": "rfp",
                "download_url": f"/api/documents/download/{doc_info['doc_id']}"
            }

        return result

    def create_rfp_document(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create RFP document using the template"""
        try:
            # Check if template exists
            if not self.template_path:
                logger.warning("Template file not found, returning data only")
                return {
                    "success": False,
                    "error": "Template file not found"
                }

            # Import required modules
            try:
                from application.services.docx_filler_service import DocxFillerService
                from application.extensions import mongo_db
            except ImportError as e:
                logger.warning(f"Required service not available: {e}")
                return {
                    "success": False,
                    "error": "Document service not available"
                }

            # Generate document
            doc_id = str(uuid.uuid4())[:8]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Define output path
            output_dir = "/app/outputs/rfp_documents" if os.path.exists("/app/outputs") else "outputs/rfp_documents"
            os.makedirs(output_dir, exist_ok=True)

            file_name = f"RFP_{data.get('project_name', 'Document')[:20].replace(' ', '_')}_{timestamp}.docx"
            output_path = os.path.join(output_dir, file_name)

            # Fill the template
            filler = DocxFillerService(self.template_path)
            generated_path = filler.fill_template(data, output_path)

            # Save document metadata to MongoDB for download endpoint
            try:
                user_documents_collection = mongo_db.db.user_documents
                document_metadata = {
                    "doc_id": doc_id,
                    "user": "system",  # Default user for agent-generated documents
                    "title": f"RFP - {data.get('project_name', 'Document')}",
                    "file_name": file_name,
                    "file_path": generated_path,
                    "type": "rfp",
                    "created_at": datetime.utcnow(),
                    "data": data
                }
                user_documents_collection.insert_one(document_metadata)
                logger.info(f"Document metadata saved to MongoDB with doc_id: {doc_id}")
            except Exception as mongo_error:
                logger.warning(f"Could not save to MongoDB (download may not work): {mongo_error}")
                # Continue even if MongoDB save fails

            return {
                "success": True,
                "doc_id": doc_id,
                "file_path": generated_path,
                "file_name": file_name
            }

        except Exception as e:
            logger.error(f"Error creating RFP document: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def run(self, message: str, **kwargs) -> Generator[str, None, None]:
        """Override run method to handle RFP generation"""
        try:
            # Process the message and generate response with document
            result = self.generate_response_with_document(message)

            # Format response for streaming
            response_text = result["answer"]

            # If document was generated, add it as a markdown code block
            if "document" in result:
                # Format document metadata for frontend parsing
                doc_block = f"""

```document
{{
  "doc_id": "{result['document']['doc_id']}",
  "title": "{result['document']['title']}",
  "file_name": "{result['document']['file_name']}",
  "preview_text": "{result['document']['preview_text']}",
  "sections": {json.dumps(result['document']['sections'], ensure_ascii=False)},
  "type": "{result['document']['type']}",
  "download_url": "{result['document']['download_url']}"
}}
```"""
                yield response_text + doc_block
            else:
                yield response_text

        except Exception as e:
            logger.error(f"Error in RFP Agent: {e}")
            yield f"عذراً، حدث خطأ في معالجة الطلب: {str(e)}"