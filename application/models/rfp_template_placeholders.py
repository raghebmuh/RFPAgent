"""
RFP Template Placeholder Definitions - CORRECTED
Defines all placeholders that match the actual template: rfp_template_with_placeholders.docx
"""

from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field


class PlaceholderType(Enum):
    """Types of placeholders in the RFP template"""
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    TIME = "time"
    EMAIL = "email"
    DROPDOWN = "dropdown"
    MULTI_LINE = "multi_line"
    STRUCTURED = "structured"
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


class RFPTemplatePlaceholders:
    """Central registry of all actual RFP template placeholders"""

    # Basic Tender Information
    TENDER_INFO = {
        "tender_name": PlaceholderDefinition(
            name="tender_name",
            arabic_name="اسم المنافسة",
            type=PlaceholderType.TEXT,
            required=True,
            example="تطوير نظام إدارة المواعيد الإلكتروني",
            question_prompt="ما هو اسم المنافسة أو المشروع؟"
        ),
        "tender_number": PlaceholderDefinition(
            name="tender_number",
            arabic_name="رقم المنافسة",
            type=PlaceholderType.TEXT,
            required=True,
            example="2024-001",
            validation_pattern=r"^[0-9A-Za-z\-]+$",
            question_prompt="ما هو رقم المنافسة (مثل: 2024-001)؟"
        ),
        "tender_purpose": PlaceholderDefinition(
            name="tender_purpose",
            arabic_name="الغرض من المنافسة",
            type=PlaceholderType.MULTI_LINE,
            required=True,
            min_length=50,
            question_prompt="ما هو الغرض من المنافسة؟ (وصف مختصر للهدف)"
        ),
        "tender_documents_fees": PlaceholderDefinition(
            name="tender_documents_fees",
            arabic_name="رسوم وثائق المنافسة",
            type=PlaceholderType.TEXT,
            required=False,
            default_value="غير محدد",
            example="1500 ريال سعودي",
            question_prompt="ما هي رسوم الحصول على وثائق المنافسة؟"
        )
    }

    # Organization Information
    ORGANIZATION_INFO = {
        "technical_organization_name": PlaceholderDefinition(
            name="technical_organization_name",
            arabic_name="اسم الجهة الفنية",
            type=PlaceholderType.TEXT,
            required=True,
            example="وزارة الصحة",
            question_prompt="ما هو اسم الجهة الحكومية أو المنظمة المسؤولة؟"
        ),
        "definition_department": PlaceholderDefinition(
            name="definition_department",
            arabic_name="الإدارة المسؤولة",
            type=PlaceholderType.TEXT,
            required=False,
            default_value="إدارة المشاريع",
            example="إدارة تقنية المعلومات",
            question_prompt="ما هي الإدارة أو القسم المسؤول عن المشروع؟"
        )
    }

    # Project Details
    PROJECT_DETAILS = {
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
        "work_execution_method": PlaceholderDefinition(
            name="work_execution_method",
            arabic_name="طريقة تنفيذ الأعمال",
            type=PlaceholderType.MULTI_LINE,
            required=True,
            generation_instructions="""
            الخدمة التي سيتم عملها من قبل المتعاقد.
            التفاصيل المتعلقة بالخدمة.
            المواد التي سيتم استعمالها.
            القياسات المتعلقة بالمواد.
            تفاصيل الاختبارات المطلوبة.
            """,
            question_prompt="كيف سيتم تنفيذ الأعمال؟ (الطريقة، المواد، الاختبارات المطلوبة)"
        ),
        "work_program_phases": PlaceholderDefinition(
            name="work_program_phases",
            arabic_name="مراحل البرنامج الزمني",
            type=PlaceholderType.STRUCTURED,
            required=True,
            generation_instructions="""
            تحديد مراحل التنفيذ ومدة كل مرحلة.
            المرحلة الأولى: [الوصف] مدة [المدة]
            المرحلة الثانية: [الوصف] مدة [المدة]
            """,
            question_prompt="ما هي مراحل تنفيذ المشروع والمدة الزمنية لكل مرحلة؟"
        ),
        "work_program_payment_method": PlaceholderDefinition(
            name="work_program_payment_method",
            arabic_name="طريقة الدفع",
            type=PlaceholderType.STRUCTURED,
            required=True,
            generation_instructions="""
            تحديد طريقة الدفع ونسب الدفعات.
            الدفعة الأولى: X% بعد [الحدث]
            الدفعة الثانية: X% بعد [الحدث]
            """,
            question_prompt="ما هي طريقة الدفع ونسب الدفعات؟"
        )
    }

    # Technical Inquiries
    TECHNICAL_INQUIRIES = {
        "technical_inquiries_entity_name": PlaceholderDefinition(
            name="technical_inquiries_entity_name",
            arabic_name="جهة الاستفسارات الفنية",
            type=PlaceholderType.TEXT,
            required=True,
            example="إدارة المشاريع - وزارة الصحة",
            question_prompt="ما هي الجهة المسؤولة عن الاستفسارات الفنية؟"
        ),
        "technical_inquiries_email": PlaceholderDefinition(
            name="technical_inquiries_email",
            arabic_name="البريد الإلكتروني للاستفسارات",
            type=PlaceholderType.EMAIL,
            required=True,
            validation_pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            example="rfp@organization.gov.sa",
            question_prompt="ما هو البريد الإلكتروني للاستفسارات الفنية؟"
        ),
        "technical_inquiries_alt_email": PlaceholderDefinition(
            name="technical_inquiries_alt_email",
            arabic_name="البريد الإلكتروني البديل",
            type=PlaceholderType.EMAIL,
            required=False,
            validation_pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            question_prompt="ما هو البريد الإلكتروني البديل للاستفسارات (اختياري)؟"
        ),
        "technical_inquiries_duration": PlaceholderDefinition(
            name="technical_inquiries_duration",
            arabic_name="مدة الاستفسارات",
            type=PlaceholderType.TEXT,
            required=False,
            default_value="5 أيام عمل",
            example="5 أيام عمل",
            question_prompt="ما هي المدة المتاحة لتقديم الاستفسارات الفنية؟"
        )
    }

    # Bids and Proposals
    BIDS_INFO = {
        "bids_review_proposals": PlaceholderDefinition(
            name="bids_review_proposals",
            arabic_name="مراجعة العروض والمقترحات",
            type=PlaceholderType.MULTI_LINE,
            required=False,
            generation_instructions="معايير مراجعة وتقييم العروض المقدمة",
            question_prompt="ما هي معايير مراجعة العروض والمقترحات؟"
        ),
        "purchase_reference": PlaceholderDefinition(
            name="purchase_reference",
            arabic_name="المرجع الشرائي",
            type=PlaceholderType.TEXT,
            required=False,
            question_prompt="ما هو المرجع الشرائي أو رقم أمر الشراء (إن وجد)؟"
        )
    }

    # Samples Delivery Information
    SAMPLES_DELIVERY = {
        "supplier_samples_delivery_address": PlaceholderDefinition(
            name="supplier_samples_delivery_address",
            arabic_name="عنوان تسليم العينات",
            type=PlaceholderType.TEXT,
            required=False,
            example="المبنى الرئيسي، شارع الملك فهد، الرياض",
            question_prompt="ما هو عنوان تسليم العينات (إن وجد)؟"
        ),
        "samples_delivery_building": PlaceholderDefinition(
            name="samples_delivery_building",
            arabic_name="المبنى",
            type=PlaceholderType.TEXT,
            required=False,
            example="المبنى A",
            question_prompt="في أي مبنى يتم تسليم العينات؟"
        ),
        "samples_delivery_floor": PlaceholderDefinition(
            name="samples_delivery_floor",
            arabic_name="الطابق",
            type=PlaceholderType.TEXT,
            required=False,
            example="الطابق الثالث",
            question_prompt="في أي طابق يتم تسليم العينات؟"
        ),
        "samples_delivery_room_or_department": PlaceholderDefinition(
            name="samples_delivery_room_or_department",
            arabic_name="الغرفة أو القسم",
            type=PlaceholderType.TEXT,
            required=False,
            example="قسم المشتريات - غرفة 301",
            question_prompt="ما هي الغرفة أو القسم لتسليم العينات؟"
        ),
        "samples_delivery_time": PlaceholderDefinition(
            name="samples_delivery_time",
            arabic_name="وقت تسليم العينات",
            type=PlaceholderType.TEXT,
            required=False,
            example="من 9:00 صباحاً إلى 2:00 مساءً",
            question_prompt="ما هو وقت استلام العينات؟"
        )
    }

    @classmethod
    def get_all_placeholders(cls) -> Dict[str, PlaceholderDefinition]:
        """Get all placeholder definitions"""
        all_placeholders = {}
        all_placeholders.update(cls.TENDER_INFO)
        all_placeholders.update(cls.ORGANIZATION_INFO)
        all_placeholders.update(cls.PROJECT_DETAILS)
        all_placeholders.update(cls.TECHNICAL_INQUIRIES)
        all_placeholders.update(cls.BIDS_INFO)
        all_placeholders.update(cls.SAMPLES_DELIVERY)
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
        """Generate questions for missing data fields"""
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
                    "required": definition.required,
                    "example": definition.example,
                    "options": definition.dropdown_options if definition.dropdown_options else None,
                    "default": definition.default_value
                }
                questions.append(question)

        return questions

    @classmethod
    def validate_placeholder_value(cls, field_name: str, value: Any) -> Tuple[bool, str]:
        """Validate a placeholder value"""
        all_placeholders = cls.get_all_placeholders()

        if field_name not in all_placeholders:
            return False, f"حقل غير معروف: {field_name}"

        definition = all_placeholders[field_name]

        # Check required
        if definition.required and not value:
            return False, f"الحقل مطلوب: {definition.arabic_name}"

        # Check pattern
        if definition.validation_pattern and value:
            import re
            if not re.match(definition.validation_pattern, str(value)):
                return False, f"قيمة غير صحيحة للحقل: {definition.arabic_name}"

        # Check length
        if definition.min_length and value and len(str(value)) < definition.min_length:
            return False, f"القيمة قصيرة جداً للحقل: {definition.arabic_name} (الحد الأدنى: {definition.min_length})"

        if definition.max_length and value and len(str(value)) > definition.max_length:
            return False, f"القيمة طويلة جداً للحقل: {definition.arabic_name} (الحد الأقصى: {definition.max_length})"

        return True, ""

    @classmethod
    def get_rfp_json_schema(cls) -> Dict[str, Any]:
        """Generate JSON schema for RFP data validation"""
        all_placeholders = cls.get_all_placeholders()
        required_fields = cls.get_required_placeholders()

        properties = {}
        for name, definition in all_placeholders.items():
            prop = {"type": "string", "description": definition.arabic_name}

            if definition.example:
                prop["example"] = definition.example

            if definition.dropdown_options:
                prop["enum"] = definition.dropdown_options

            if definition.min_length:
                prop["minLength"] = definition.min_length

            if definition.max_length:
                prop["maxLength"] = definition.max_length

            if definition.validation_pattern:
                prop["pattern"] = definition.validation_pattern

            properties[name] = prop

        return {
            "type": "object",
            "properties": properties,
            "required": required_fields,
            "additionalProperties": False
        }