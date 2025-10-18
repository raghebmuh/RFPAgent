"""
RFP Agent Implementation
Specialized agent for generating RFP documents through intelligent conversation
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Generator, Tuple
from datetime import datetime

from application.agents.react_agent import ReActAgent
from application.models.rfp_placeholders import (
    RFPPlaceholders,
    PlaceholderDefinition,
    get_rfp_json_schema
)
from application.services.docx_placeholder_service import DocxPlaceholderService
from application.retriever.base import BaseRetriever

logger = logging.getLogger(__name__)


class RFPAgent(ReActAgent):
    """
    Specialized ReAct agent for RFP document generation
    Extends ReActAgent to provide RFP-specific functionality
    """

    def __init__(self, *args, **kwargs):
        # Set default JSON schema for RFP if not provided
        if 'json_schema' not in kwargs or not kwargs['json_schema']:
            kwargs['json_schema'] = get_rfp_json_schema()

        super().__init__(*args, **kwargs)

        # RFP-specific attributes
        self.template_path = os.path.join("inputs", "templates", "rfp_template_with_placeholders.docx")
        self.placeholder_service = DocxPlaceholderService(self.template_path)
        self.collected_data: Dict[str, Any] = {}
        self.missing_fields: List[str] = []
        self.conversation_state = "initial"  # initial, collecting, validating, generating
        self.completion_percentage = 0

        # Load template placeholders
        self._initialize_template()

    def _initialize_template(self):
        """Initialize the RFP template and extract placeholders"""
        try:
            self.placeholder_service.extract_placeholders()
            self.placeholder_service.extract_dropdown_fields()
            logger.info(f"Initialized RFP template with {len(self.placeholder_service.placeholders)} placeholders")
        except Exception as e:
            logger.error(f"Failed to initialize RFP template: {e}")
            raise

    def analyze_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze user input to extract RFP-relevant information
        Maps extracted information to placeholder names
        """
        extracted_data = {}

        # Keywords to placeholder mapping
        keyword_mappings = {
            "entity_name": ["الجهة", "المؤسسة", "الوزارة", "الهيئة", "المركز", "الشركة"],
            "project_name": ["المشروع", "المنافسة", "العملية", "النظام", "التطبيق"],
            "tender_number": ["رقم المنافسة", "الرقم المرجعي", "رقم المشروع"],
            "duration_months": ["المدة", "مدة التنفيذ", "فترة العمل", "شهر", "أشهر"],
            "budget_range": ["الميزانية", "التكلفة", "القيمة", "ريال"],
            "location": ["المكان", "الموقع", "المدينة", "المنطقة"],
            "project_type": ["نوع المشروع", "تقنية", "بناء", "استشارات", "توريد"]
        }

        # Simple extraction based on keywords (can be enhanced with NLP)
        user_input_lower = user_input.lower()

        for field, keywords in keyword_mappings.items():
            for keyword in keywords:
                if keyword in user_input:
                    # Extract the value after the keyword
                    # This is a simplified extraction - can be improved with better NLP
                    parts = user_input.split(keyword)
                    if len(parts) > 1:
                        # Extract the next few words as the value
                        value = parts[1].split('.')[0].split('،')[0].strip()
                        if value and len(value) > 2:
                            extracted_data[field] = value
                            break

        # Special handling for project scope - extract longer descriptions
        scope_keywords = ["نطاق العمل", "وصف المشروع", "الأهداف", "المتطلبات"]
        for keyword in scope_keywords:
            if keyword in user_input:
                # Extract everything after the keyword as scope
                parts = user_input.split(keyword)
                if len(parts) > 1:
                    extracted_data["project_scope"] = parts[1].strip()
                    break

        return extracted_data

    def identify_missing_fields(self) -> List[str]:
        """
        Identify which required placeholders are missing data
        """
        self.missing_fields = []
        required_fields = RFPPlaceholders.get_required_placeholders()

        for field in required_fields:
            if field not in self.collected_data or not self.collected_data[field]:
                self.missing_fields.append(field)

        # Calculate completion percentage
        total_required = len(required_fields)
        completed = total_required - len(self.missing_fields)
        self.completion_percentage = int((completed / total_required) * 100) if total_required > 0 else 0

        return self.missing_fields

    def generate_questions_for_missing_data(self) -> str:
        """
        Generate natural language questions for missing data
        """
        if not self.missing_fields:
            return "جميع البيانات المطلوبة متوفرة. يمكننا الآن إنشاء وثيقة RFP."

        questions = RFPPlaceholders.get_questions_for_missing_data(self.missing_fields[:3])  # Ask 3 at a time

        question_text = "لإكمال وثيقة RFP، أحتاج إلى بعض المعلومات الإضافية:\n\n"

        for i, q in enumerate(questions, 1):
            question_text += f"{i}. {q['question']}"
            if q.get('example'):
                question_text += f" (مثال: {q['example']})"
            if q.get('options'):
                question_text += f"\n   الخيارات: {', '.join(q['options'])}"
            question_text += "\n"

        question_text += f"\n📊 نسبة الإكمال الحالية: {self.completion_percentage}%"

        return question_text

    def validate_collected_data(self) -> Tuple[bool, List[str]]:
        """
        Validate all collected data against placeholder rules
        Returns: (is_valid, error_messages)
        """
        errors = []

        for field_name, value in self.collected_data.items():
            is_valid, error_msg = RFPPlaceholders.validate_placeholder_value(field_name, value)
            if not is_valid:
                errors.append(error_msg)

        # Check for missing required fields
        missing = self.identify_missing_fields()
        if missing:
            for field in missing[:5]:  # Show max 5 missing fields
                definition = RFPPlaceholders.get_placeholder_by_name(field)
                if definition:
                    errors.append(f"حقل مطلوب: {definition.arabic_name}")

        return len(errors) == 0, errors

    def format_structured_output(self) -> Dict[str, Any]:
        """
        Format collected data according to the JSON schema
        Applies special formatting rules for specific placeholders
        """
        formatted_data = self.collected_data.copy()

        # Apply special formatting for structured fields
        if "work_program_phases" in formatted_data:
            # Format phases if provided as plain text
            if isinstance(formatted_data["work_program_phases"], str):
                formatted_data["work_program_phases"] = self._format_phases(
                    formatted_data["work_program_phases"]
                )

        if "work_program_payment_method" in formatted_data:
            # Format payment schedule if provided as plain text
            if isinstance(formatted_data["work_program_payment_method"], str):
                formatted_data["work_program_payment_method"] = self._format_payment_schedule(
                    formatted_data["work_program_payment_method"]
                )

        return formatted_data

    def _format_phases(self, phases_text: str) -> str:
        """Format project phases according to template requirements"""
        # If phases are provided as a list or structured text, format them properly
        formatted = "مراحل تنفيذ المشروع كالتالي:\n"

        # Simple parsing - can be enhanced
        lines = phases_text.split('\n')
        phase_num = 1
        for line in lines:
            if line.strip():
                formatted += f"المرحلة {self._arabic_number(phase_num)}: {line.strip()}\n"
                phase_num += 1

        return formatted

    def _format_payment_schedule(self, payment_text: str) -> str:
        """Format payment schedule according to template requirements"""
        formatted = "طريقة الدفع:\n"
        formatted += "يكون طريقة الدفع وفقاً لشهادة الإنجاز الصادرة من الإدارة المشرفة على التنفيذ\n"

        # Parse payment information
        lines = payment_text.split('\n')
        payment_num = 1
        for line in lines:
            if line.strip():
                formatted += f"الدفعة {self._arabic_number(payment_num)}: {line.strip()}\n"
                payment_num += 1

        return formatted

    def _arabic_number(self, num: int) -> str:
        """Convert number to Arabic text"""
        arabic_numbers = {
            1: "الأولى", 2: "الثانية", 3: "الثالثة", 4: "الرابعة",
            5: "الخامسة", 6: "السادسة", 7: "السابعة", 8: "الثامنة",
            9: "التاسعة", 10: "العاشرة"
        }
        return arabic_numbers.get(num, f"رقم {num}")

    def generate_rfp_content(self) -> Dict[str, Any]:
        """
        Generate content for all RFP placeholders based on collected data
        This includes generating appropriate content for fields with special instructions
        """
        rfp_content = self.collected_data.copy()

        # Generate content for special placeholders if not provided
        if "project_scope" in rfp_content and len(rfp_content["project_scope"]) < 100:
            # Enhance project scope based on other data
            rfp_content["project_scope"] = self._enhance_project_scope(rfp_content)

        # Add default values for optional fields if not provided
        all_placeholders = RFPPlaceholders.get_all_placeholders()
        for name, definition in all_placeholders.items():
            if name not in rfp_content and definition.default_value:
                rfp_content[name] = definition.default_value

        # Add timestamp
        rfp_content["generation_date"] = datetime.now().strftime("%Y-%m-%d")

        return rfp_content

    def _enhance_project_scope(self, data: Dict[str, Any]) -> str:
        """Enhance project scope description based on available data"""
        scope = data.get("project_scope", "")
        project_name = data.get("project_name", "المشروع")
        project_type = data.get("project_type", "")

        enhanced_scope = f"""نطاق عمل {project_name}:

{scope}

المخرجات المتوقعة:
- تسليم جميع مخرجات المشروع حسب المواصفات المطلوبة
- توفير الوثائق الفنية والأدلة التشغيلية
- ضمان الجودة والأداء حسب المعايير المعتمدة
"""

        # Add training section if required
        if data.get("training_required") == "نعم":
            enhanced_scope += """
التدريب ونقل المعرفة:
يلتزم المتعاقد بتدريب فريق عمل الجهة الحكومية ونقل المعرفة والخبرة لموظفيها بكافة الوسائل الممكنة ومن ذلك:
- التدريب على رأس العمل
- العمل جنباً إلى جنب معهم
- ورش العمل التدريبية
وذلك بما يكفل حصولهم على المعرفة والخبرة اللازمة لمخرجات المشروع.
"""

        return enhanced_scope

    def process_conversation_turn(self, user_input: str) -> Dict[str, Any]:
        """
        Process a conversation turn and manage RFP data collection
        Returns response with current state and next steps
        """
        response = {
            "message": "",
            "state": self.conversation_state,
            "completion": self.completion_percentage,
            "missing_fields": [],
            "ready_to_generate": False
        }

        # Extract data from user input
        extracted_data = self.analyze_user_input(user_input)
        self.collected_data.update(extracted_data)

        # Identify missing fields
        self.identify_missing_fields()

        if self.missing_fields:
            # Still collecting data
            self.conversation_state = "collecting"
            response["message"] = self.generate_questions_for_missing_data()
            response["missing_fields"] = self.missing_fields[:3]  # Show next 3 fields
        else:
            # All required data collected, validate
            self.conversation_state = "validating"
            is_valid, errors = self.validate_collected_data()

            if is_valid:
                self.conversation_state = "ready"
                response["ready_to_generate"] = True
                response["message"] = """✅ ممتاز! لقد جمعت جميع المعلومات المطلوبة لإنشاء وثيقة RFP.

📋 ملخص المعلومات:
- اسم المشروع: {project_name}
- الجهة: {entity_name}
- المدة: {duration_months} شهر
- نوع المشروع: {project_type}

سأقوم الآن بإنشاء وثيقة RFP كاملة وفقاً للمواصفات الحكومية السعودية.

🔄 جاري إنشاء الوثيقة...""".format(**self.collected_data)
            else:
                response["message"] = "⚠️ يوجد بعض الأخطاء في البيانات:\n"
                response["message"] += "\n".join(f"• {error}" for error in errors)

        response["completion"] = self.completion_percentage
        response["state"] = self.conversation_state

        return response

    def generate_agent_prompt(self) -> str:
        """
        Generate the specialized prompt for the RFP Agent
        This will be used when creating the agent in the system
        """
        prompt = """أنت وكيل متخصص في إنشاء وثائق طلب تقديم العروض (RFP) للمشاريع الحكومية في المملكة العربية السعودية.

مهمتك الأساسية:
1. جمع معلومات المشروع من المستخدم بشكل تدريجي ومنظم
2. التحقق من اكتمال البيانات المطلوبة
3. إنشاء وثيقة RFP احترافية وفقاً للمعايير الحكومية السعودية

عند التواصل مع المستخدم:
- ابدأ بالترحيب واسأل عن المعلومات الأساسية للمشروع
- اطرح أسئلة واضحة ومحددة للحصول على البيانات المطلوبة
- قدم أمثلة عند الحاجة لتوضيح المطلوب
- أظهر نسبة إنجاز جمع البيانات
- تحقق من صحة البيانات المدخلة

القواعد المهمة:
- استخدم اللغة العربية الفصحى الرسمية
- تجنب ذكر أي علامات تجارية محددة في نطاق العمل
- اتبع نظام المنافسات والمشتريات الحكومية السعودي
- تأكد من وضوح ودقة نطاق العمل
- احرص على تضمين متطلبات المحتوى المحلي

البيانات المطلوبة تشمل:
- معلومات الجهة والمشروع
- نطاق العمل والمتطلبات
- الجدول الزمني ومراحل التنفيذ
- طريقة الدفع والميزانية
- المواصفات الفنية
- معايير التقييم
- الشهادات والمتطلبات النظامية

عند اكتمال جميع البيانات، قم بإنشاء وثيقة RFP شاملة ومفصلة."""

        return prompt


def create_rfp_agent_config() -> Dict[str, Any]:
    """
    Create the configuration for RFP Agent to be stored in the database
    This can be used when creating the agent through the API
    """
    config = {
        "name": "وكيل طلب تقديم العروض",
        "description": "وكيل متخصص في إنشاء وثائق طلب تقديم العروض (RFP) للمشاريع الحكومية السعودية. يقوم بجمع معلومات المشروع وإنشاء وثيقة RFP احترافية متوافقة مع الأنظمة الحكومية.",
        "agent_type": "ReActRFP",  # Special type to identify RFP agents
        "prompt_template": RFPAgent().generate_agent_prompt(),
        "json_schema": get_rfp_json_schema(),
        "tools": ["rfp_reference_tool", "document_search"],  # Tools the agent can use
        "chunks": 5,
        "retriever": "classic_rag",
        "sources": ["default"],  # Can include RFP knowledge base sources
        "status": "published",
        "metadata": {
            "template_file": "rfp_template_with_placeholders.docx",
            "language": "ar",
            "region": "SA",
            "compliance": "Saudi Government Procurement",
            "version": "1.0"
        }
    }
    return config