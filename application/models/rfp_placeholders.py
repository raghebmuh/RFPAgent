"""
RFP Template Placeholder Definitions
Defines all placeholders expected in the RFP template and their metadata
"""

from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field


class PlaceholderType(Enum):
    """Types of placeholders in the RFP template"""
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    DROPDOWN = "dropdown"
    MULTI_LINE = "multi_line"
    STRUCTURED = "structured"  # For complex fields like phases, payments
    TABLE = "table"


@dataclass
class PlaceholderDefinition:
    """Definition for a single placeholder"""
    name: str
    arabic_name: str
    type: PlaceholderType
    required: bool = True
    default_value: Optional[Any] = None
    dropdown_options: List[str] = field(default_factory=list)
    validation_pattern: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    example: Optional[str] = None
    generation_instructions: Optional[str] = None
    question_prompt: Optional[str] = None  # Question to ask user for this field


class RFPPlaceholders:
    """Central registry of all RFP template placeholders"""

    # Basic Information Placeholders
    BASIC_INFO = {
        "entity_name": PlaceholderDefinition(
            name="entity_name",
            arabic_name="اسم الجهة الحكومية",
            type=PlaceholderType.TEXT,
            required=True,
            example="المركز الوطني لتنمية الغطاء النباتي ومكافحة التصحر",
            question_prompt="ما هو اسم الجهة الحكومية المسؤولة عن المشروع؟"
        ),
        "project_name": PlaceholderDefinition(
            name="project_name",
            arabic_name="اسم المشروع",
            type=PlaceholderType.TEXT,
            required=True,
            example="تطبيق أتمتة خدمات تقنية المعلومات",
            question_prompt="ما هو اسم المشروع أو المنافسة؟"
        ),
        "tender_number": PlaceholderDefinition(
            name="tender_number",
            arabic_name="رقم المنافسة",
            type=PlaceholderType.TEXT,
            required=True,
            example="9301471",
            validation_pattern=r"^\d+$",
            question_prompt="ما هو رقم المنافسة أو المرجع؟"
        ),
        "project_type": PlaceholderDefinition(
            name="project_type",
            arabic_name="نوع المشروع",
            type=PlaceholderType.DROPDOWN,
            required=True,
            dropdown_options=[
                "تقنية المعلومات",
                "البناء والتشييد",
                "الاستشارات",
                "التوريد",
                "الخدمات",
                "مشروع متعدد الأنواع"
            ],
            question_prompt="ما هو نوع المشروع؟"
        ),
        "classification": PlaceholderDefinition(
            name="classification",
            arabic_name="تصنيف المشروع",
            type=PlaceholderType.TEXT,
            required=False,
            default_value="غير محدد",
            question_prompt="ما هو التصنيف الفني للمشروع؟"
        )
    }

    # Project Scope and Details
    SCOPE_DETAILS = {
        "project_scope": PlaceholderDefinition(
            name="project_scope",
            arabic_name="نطاق العمل",
            type=PlaceholderType.MULTI_LINE,
            required=True,
            min_length=100,
            generation_instructions="""
            يجب كتابة نطاق العمل كاملاً باللغة العربية مع:
            - وصف دقيق وواضح للمشروع
            - تحديد مخرجات المشروع
            - عدم الإشارة إلى علامة تجارية محددة
            - ذكر متطلبات التدريب ونقل المعرفة إذا لزم
            """,
            question_prompt="يرجى وصف نطاق العمل بالتفصيل (الأهداف، المخرجات، المتطلبات الأساسية)"
        ),
        "project_objectives": PlaceholderDefinition(
            name="project_objectives",
            arabic_name="أهداف المشروع",
            type=PlaceholderType.MULTI_LINE,
            required=True,
            question_prompt="ما هي الأهداف الرئيسية للمشروع؟"
        ),
        "deliverables": PlaceholderDefinition(
            name="deliverables",
            arabic_name="مخرجات المشروع",
            type=PlaceholderType.MULTI_LINE,
            required=True,
            question_prompt="ما هي المخرجات المتوقعة من المشروع؟"
        ),
        "requirements": PlaceholderDefinition(
            name="requirements",
            arabic_name="المتطلبات",
            type=PlaceholderType.MULTI_LINE,
            required=True,
            question_prompt="ما هي المتطلبات الفنية والإدارية للمشروع؟"
        )
    }

    # Timeline and Phases
    TIMELINE = {
        "start_date": PlaceholderDefinition(
            name="start_date",
            arabic_name="تاريخ البداية",
            type=PlaceholderType.DATE,
            required=True,
            question_prompt="ما هو التاريخ المتوقع لبدء المشروع؟"
        ),
        "duration_months": PlaceholderDefinition(
            name="duration_months",
            arabic_name="مدة المشروع",
            type=PlaceholderType.NUMBER,
            required=True,
            example="6",
            question_prompt="ما هي مدة تنفيذ المشروع بالأشهر؟"
        ),
        "work_program_phases": PlaceholderDefinition(
            name="work_program_phases",
            arabic_name="مراحل البرنامج الزمني",
            type=PlaceholderType.STRUCTURED,
            required=True,
            generation_instructions="""
            تنسيق المراحل:
            المرحلة الأولى: [وصف المرحلة] مدة [X] شهر
            المرحلة الثانية: [وصف المرحلة] مدة [X] شهر
            المرحلة الثالثة: [وصف المرحلة] مدة [X] شهر
            """,
            question_prompt="ما هي مراحل تنفيذ المشروع والمدة الزمنية لكل مرحلة؟"
        )
    }

    # Financial Information
    FINANCIAL = {
        "budget_range": PlaceholderDefinition(
            name="budget_range",
            arabic_name="نطاق الميزانية",
            type=PlaceholderType.TEXT,
            required=False,
            example="500,000 - 1,000,000 ريال سعودي",
            question_prompt="ما هو نطاق الميزانية المخصصة للمشروع (اختياري)؟"
        ),
        "work_program_payment_method": PlaceholderDefinition(
            name="work_program_payment_method",
            arabic_name="طريقة الدفع",
            type=PlaceholderType.STRUCTURED,
            required=True,
            generation_instructions="""
            تنسيق طريقة الدفع:
            الدفعة الأولى: X% بعد [الحدث/المرحلة]
            الدفعة الثانية: X% بعد [الحدث/المرحلة]
            الدفعة الثالثة: X% بعد [الحدث/المرحلة]
            """,
            question_prompt="ما هي طريقة الدفع المفضلة ونسب الدفعات؟"
        ),
        "payment_method": PlaceholderDefinition(
            name="payment_method",
            arabic_name="آلية الدفع",
            type=PlaceholderType.DROPDOWN,
            required=True,
            dropdown_options=[
                "دفعات حسب المراحل",
                "دفعة شهرية",
                "دفعة واحدة عند الانتهاء",
                "نسبة مئوية مقسمة",
                "جدول دفعات مخصص"
            ],
            question_prompt="ما هي آلية الدفع المفضلة؟"
        ),
        "warranty_period": PlaceholderDefinition(
            name="warranty_period",
            arabic_name="فترة الضمان",
            type=PlaceholderType.TEXT,
            required=True,
            default_value="12 شهر",
            example="12 شهر",
            question_prompt="ما هي فترة الضمان المطلوبة؟"
        )
    }

    # Technical Specifications
    TECHNICAL = {
        "work_execution_method": PlaceholderDefinition(
            name="work_execution_method",
            arabic_name="طريقة تنفيذ الأعمال",
            type=PlaceholderType.MULTI_LINE,
            required=True,
            generation_instructions="""
            يجب تضمين:
            - الخدمة التي سيتم عملها من قبل المتعاقد
            - التفاصيل المتعلقة بالخدمة
            - المواد التي سيتم استعمالها
            - القياسات المتعلقة بالمواد
            - تفاصيل الاختبارات المطلوبة
            """,
            question_prompt="كيف سيتم تنفيذ الأعمال (الخدمات، المواد، الاختبارات)؟"
        ),
        "technical_specifications": PlaceholderDefinition(
            name="technical_specifications",
            arabic_name="المواصفات الفنية",
            type=PlaceholderType.MULTI_LINE,
            required=True,
            question_prompt="ما هي المواصفات الفنية التفصيلية للمشروع؟"
        ),
        "quality_standards": PlaceholderDefinition(
            name="quality_standards",
            arabic_name="معايير الجودة",
            type=PlaceholderType.MULTI_LINE,
            required=False,
            question_prompt="ما هي معايير الجودة المطلوبة؟"
        ),
        "safety_requirements": PlaceholderDefinition(
            name="safety_requirements",
            arabic_name="متطلبات السلامة",
            type=PlaceholderType.MULTI_LINE,
            required=False,
            question_prompt="ما هي متطلبات السلامة والأمان؟"
        )
    }

    # Evaluation and Selection
    EVALUATION = {
        "evaluation_criteria": PlaceholderDefinition(
            name="evaluation_criteria",
            arabic_name="معايير التقييم",
            type=PlaceholderType.STRUCTURED,
            required=True,
            generation_instructions="""
            معايير التقييم القياسية:
            - الملاءمة الفنية: 40%
            - منهجية التنفيذ: 20%
            - القدرات والخبرات: 20%
            - السعر: 20%
            """,
            question_prompt="ما هي معايير تقييم العروض والأوزان المخصصة لكل معيار؟"
        ),
        "technical_weight": PlaceholderDefinition(
            name="technical_weight",
            arabic_name="وزن التقييم الفني",
            type=PlaceholderType.NUMBER,
            required=True,
            default_value="60",
            validation_pattern=r"^\d{1,3}$",
            question_prompt="ما هو الوزن النسبي للتقييم الفني (%)؟"
        ),
        "financial_weight": PlaceholderDefinition(
            name="financial_weight",
            arabic_name="وزن التقييم المالي",
            type=PlaceholderType.NUMBER,
            required=True,
            default_value="40",
            validation_pattern=r"^\d{1,3}$",
            question_prompt="ما هو الوزن النسبي للتقييم المالي (%)؟"
        )
    }

    # Compliance and Requirements
    COMPLIANCE = {
        "required_certificates": PlaceholderDefinition(
            name="required_certificates",
            arabic_name="الشهادات المطلوبة",
            type=PlaceholderType.MULTI_LINE,
            required=True,
            default_value="""السجل التجاري
شهادة الزكاة والدخل
شهادة التأمينات الاجتماعية
شهادة الغرفة التجارية
رخصة الاستثمار (إن وجدت)""",
            question_prompt="ما هي الشهادات والوثائق المطلوبة من المتقدمين؟"
        ),
        "local_content_percentage": PlaceholderDefinition(
            name="local_content_percentage",
            arabic_name="نسبة المحتوى المحلي",
            type=PlaceholderType.NUMBER,
            required=False,
            default_value="30",
            example="30",
            question_prompt="ما هي نسبة المحتوى المحلي المطلوبة (%)؟"
        ),
        "submission_deadline": PlaceholderDefinition(
            name="submission_deadline",
            arabic_name="آخر موعد للتقديم",
            type=PlaceholderType.DATE,
            required=True,
            question_prompt="ما هو آخر موعد لتقديم العروض؟"
        )
    }

    # Additional Information
    ADDITIONAL = {
        "contact_department": PlaceholderDefinition(
            name="contact_department",
            arabic_name="الإدارة المسؤولة",
            type=PlaceholderType.TEXT,
            required=True,
            example="إدارة تقنية المعلومات",
            question_prompt="ما هي الإدارة المسؤولة عن المشروع؟"
        ),
        "contact_email": PlaceholderDefinition(
            name="contact_email",
            arabic_name="البريد الإلكتروني",
            type=PlaceholderType.TEXT,
            required=True,
            validation_pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            question_prompt="ما هو البريد الإلكتروني للتواصل؟"
        ),
        "contact_phone": PlaceholderDefinition(
            name="contact_phone",
            arabic_name="رقم الهاتف",
            type=PlaceholderType.TEXT,
            required=False,
            validation_pattern=r"^\+?[\d\s\-\(\)]+$",
            question_prompt="ما هو رقم الهاتف للتواصل (اختياري)؟"
        ),
        "location": PlaceholderDefinition(
            name="location",
            arabic_name="مكان التنفيذ",
            type=PlaceholderType.TEXT,
            required=True,
            question_prompt="أين سيتم تنفيذ المشروع؟"
        ),
        "training_required": PlaceholderDefinition(
            name="training_required",
            arabic_name="التدريب مطلوب",
            type=PlaceholderType.DROPDOWN,
            required=True,
            dropdown_options=["نعم", "لا"],
            default_value="نعم",
            question_prompt="هل يتطلب المشروع تدريب ونقل معرفة؟"
        )
    }

    @classmethod
    def get_all_placeholders(cls) -> Dict[str, PlaceholderDefinition]:
        """Get all placeholder definitions"""
        all_placeholders = {}
        for category in [cls.BASIC_INFO, cls.SCOPE_DETAILS, cls.TIMELINE,
                        cls.FINANCIAL, cls.TECHNICAL, cls.EVALUATION,
                        cls.COMPLIANCE, cls.ADDITIONAL]:
            all_placeholders.update(category)
        return all_placeholders

    @classmethod
    def get_required_placeholders(cls) -> List[str]:
        """Get list of required placeholder names"""
        all_placeholders = cls.get_all_placeholders()
        return [name for name, definition in all_placeholders.items() if definition.required]

    @classmethod
    def get_placeholder_by_name(cls, name: str) -> Optional[PlaceholderDefinition]:
        """Get a specific placeholder definition by name"""
        all_placeholders = cls.get_all_placeholders()
        return all_placeholders.get(name)

    @classmethod
    def get_questions_for_missing_data(cls, missing_fields: List[str]) -> List[Dict[str, Any]]:
        """Generate questions for missing placeholder data"""
        questions = []
        all_placeholders = cls.get_all_placeholders()

        for field_name in missing_fields:
            if field_name in all_placeholders:
                definition = all_placeholders[field_name]
                question = {
                    "field": field_name,
                    "arabic_name": definition.arabic_name,
                    "question": definition.question_prompt or f"يرجى إدخال {definition.arabic_name}",
                    "type": definition.type.value,
                    "required": definition.required
                }

                if definition.dropdown_options:
                    question["options"] = definition.dropdown_options

                if definition.example:
                    question["example"] = definition.example

                questions.append(question)

        return questions

    @classmethod
    def validate_placeholder_value(cls, name: str, value: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate a placeholder value
        Returns: (is_valid, error_message)
        """
        definition = cls.get_placeholder_by_name(name)
        if not definition:
            return False, f"Unknown placeholder: {name}"

        # Check required fields
        if definition.required and not value:
            return False, f"{definition.arabic_name} مطلوب"

        # Type validation
        if value:
            if definition.type == PlaceholderType.NUMBER:
                try:
                    float(value)
                except ValueError:
                    return False, f"{definition.arabic_name} يجب أن يكون رقماً"

            # Pattern validation
            if definition.validation_pattern:
                import re
                if not re.match(definition.validation_pattern, str(value)):
                    return False, f"{definition.arabic_name} غير صحيح الصيغة"

            # Length validation
            if definition.min_length and len(str(value)) < definition.min_length:
                return False, f"{definition.arabic_name} قصير جداً (الحد الأدنى {definition.min_length} حرف)"

            if definition.max_length and len(str(value)) > definition.max_length:
                return False, f"{definition.arabic_name} طويل جداً (الحد الأقصى {definition.max_length} حرف)"

            # Dropdown validation
            if definition.dropdown_options and value not in definition.dropdown_options:
                return False, f"{definition.arabic_name} يجب أن يكون من الخيارات المتاحة"

        return True, None


# Convenience function to get placeholder schema for JSON validation
def get_rfp_json_schema() -> Dict[str, Any]:
    """Generate JSON schema for RFP data validation"""
    schema = {
        "type": "object",
        "properties": {},
        "required": []
    }

    all_placeholders = RFPPlaceholders.get_all_placeholders()

    for name, definition in all_placeholders.items():
        property_schema = {
            "description": definition.arabic_name
        }

        if definition.type == PlaceholderType.TEXT:
            property_schema["type"] = "string"
        elif definition.type == PlaceholderType.NUMBER:
            property_schema["type"] = "number"
        elif definition.type == PlaceholderType.DATE:
            property_schema["type"] = "string"
            property_schema["format"] = "date"
        elif definition.type == PlaceholderType.DROPDOWN:
            property_schema["type"] = "string"
            property_schema["enum"] = definition.dropdown_options
        elif definition.type == PlaceholderType.MULTI_LINE:
            property_schema["type"] = "string"
        elif definition.type == PlaceholderType.STRUCTURED:
            property_schema["type"] = "object"

        if definition.example:
            property_schema["example"] = definition.example

        schema["properties"][name] = property_schema

        if definition.required:
            schema["required"].append(name)

    return schema