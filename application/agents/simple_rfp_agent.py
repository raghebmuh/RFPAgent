"""
Simplified RFP Agent that works without file dependencies
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from application.agents.react_agent import ReActAgent

logger = logging.getLogger(__name__)


class SimpleRFPAgent(ReActAgent):
    """
    Simplified RFP Agent that doesn't depend on external template files
    """

    def __init__(self, *args, **kwargs):
        # Ensure JSON schema is set
        if 'json_schema' not in kwargs or not kwargs['json_schema']:
            kwargs['json_schema'] = self.get_default_schema()

        super().__init__(*args, **kwargs)

        # Initialize RFP data collection
        self.collected_data = {}
        self.required_fields = [
            "entity_name",
            "project_name",
            "tender_number",
            "project_scope",
            "duration_months",
            "location"
        ]

    def get_default_schema(self):
        """Get default RFP JSON schema"""
        return {
            "type": "object",
            "properties": {
                "entity_name": {"type": "string", "description": "اسم الجهة"},
                "project_name": {"type": "string", "description": "اسم المشروع"},
                "tender_number": {"type": "string", "description": "رقم المنافسة"},
                "project_scope": {"type": "string", "description": "وصف النشاط"},
                "duration_months": {"type": "number", "description": "المدة بالأشهر"},
                "location": {"type": "string", "description": "مكان التنفيذ"},
                "submission_date": {"type": "string", "description": "موعد التسليم"},
                "start_date": {"type": "string", "description": "موعد البداية"},
                "budget": {"type": "string", "description": "الميزانية"}
            },
            "required": ["entity_name", "project_name", "project_scope"]
        }

    def process_message(self, message: str, **kwargs) -> Dict[str, Any]:
        """
        Override process_message to handle RFP data extraction
        """
        try:
            # Extract data from the Arabic message
            extracted_data = self.extract_rfp_data(message)

            # Update collected data
            self.collected_data.update(extracted_data)

            # Check what's missing
            missing_fields = self.get_missing_fields()

            # Generate response
            if missing_fields:
                response = self.generate_questions_response(missing_fields)
            else:
                response = self.generate_complete_response()

            return {
                "answer": response,
                "thought": f"تم جمع {len(self.collected_data)} من البيانات المطلوبة",
                "sources": [],
                "error": "",
                "structured_output": self.collected_data
            }

        except Exception as e:
            logger.error(f"Error in SimpleRFPAgent: {e}")
            return {
                "answer": "عذراً، حدث خطأ في معالجة البيانات. يرجى المحاولة مرة أخرى.",
                "thought": str(e),
                "sources": [],
                "error": str(e)
            }

    def extract_rfp_data(self, message: str) -> Dict[str, Any]:
        """Extract RFP data from Arabic message"""
        extracted = {}

        # Simple extraction based on keywords
        if "اسم المنافسة" in message:
            # Extract project name
            parts = message.split("اسم المنافسة")
            if len(parts) > 1:
                value = parts[1].split("\n")[0].strip(": ")
                extracted["project_name"] = value

        if "رقم المنافسة" in message:
            parts = message.split("رقم المنافسة")
            if len(parts) > 1:
                value = parts[1].split("\n")[0].strip(": ")
                extracted["tender_number"] = value

        if "موعد التسليم" in message:
            parts = message.split("موعد التسليم")
            if len(parts) > 1:
                value = parts[1].split("\n")[0].strip(": ")
                extracted["submission_date"] = value

        if "مكان التنفيذ" in message:
            parts = message.split("مكان التنفيذ")
            if len(parts) > 1:
                value = parts[1].split("\n")[0].strip(": ")
                extracted["location"] = value

        if "وصف النشاط" in message or "وصف الشغط" in message:
            parts = message.split("وصف" )
            if len(parts) > 1:
                value = parts[1].strip()
                extracted["project_scope"] = value

        # Extract dates if present
        import re
        date_pattern = r'\d{1,2}/\d{1,2}/\d{4}'
        dates = re.findall(date_pattern, message)
        if dates:
            if not extracted.get("start_date"):
                extracted["start_date"] = dates[0]
            if len(dates) > 1 and not extracted.get("submission_date"):
                extracted["submission_date"] = dates[1]

        return extracted

    def get_missing_fields(self) -> List[str]:
        """Get list of missing required fields"""
        missing = []
        for field in self.required_fields:
            if field not in self.collected_data or not self.collected_data[field]:
                missing.append(field)
        return missing

    def generate_questions_response(self, missing_fields: List[str]) -> str:
        """Generate questions for missing fields"""
        field_questions = {
            "entity_name": "ما هو اسم الجهة الحكومية المسؤولة عن المشروع؟",
            "project_name": "ما هو اسم المشروع أو المنافسة؟",
            "tender_number": "ما هو رقم المنافسة؟",
            "project_scope": "يرجى وصف نطاق العمل بالتفصيل",
            "duration_months": "ما هي مدة تنفيذ المشروع بالأشهر؟",
            "location": "أين سيتم تنفيذ المشروع؟",
            "budget": "ما هي الميزانية المخصصة للمشروع؟"
        }

        response = "شكراً لك على المعلومات المقدمة. لإكمال وثيقة RFP، أحتاج إلى المعلومات التالية:\n\n"

        for i, field in enumerate(missing_fields[:3], 1):  # Ask for 3 fields at a time
            if field in field_questions:
                response += f"{i}. {field_questions[field]}\n"

        # Show progress
        total_fields = len(self.required_fields)
        completed = total_fields - len(missing_fields)
        percentage = int((completed / total_fields) * 100)

        response += f"\n📊 نسبة الإكمال: {percentage}%"

        return response

    def generate_complete_response(self) -> str:
        """Generate response when all data is collected"""
        response = "✅ ممتاز! تم جمع جميع المعلومات المطلوبة لإنشاء وثيقة RFP.\n\n"
        response += "📋 ملخص المعلومات:\n"

        field_labels = {
            "project_name": "اسم المشروع",
            "tender_number": "رقم المنافسة",
            "location": "مكان التنفيذ",
            "submission_date": "موعد التسليم",
            "start_date": "موعد البداية"
        }

        for field, label in field_labels.items():
            if field in self.collected_data:
                response += f"• {label}: {self.collected_data[field]}\n"

        response += "\n🔄 جاري إنشاء وثيقة RFP...\n"
        response += "📄 الوثيقة جاهزة للتحميل بصيغة DOCX قابلة للتعديل."

        return response