"""
RFP Content Generation Service
Generates appropriate content for RFP placeholders based on project data and Saudi government requirements
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)


class RFPContentGenerator:
    """
    Service for generating content for RFP placeholders
    Applies Saudi government RFP standards and business language rules
    """

    # Arabic number names for ordinal numbers
    ARABIC_ORDINALS = {
        1: "الأولى", 2: "الثانية", 3: "الثالثة", 4: "الرابعة", 5: "الخامسة",
        6: "السادسة", 7: "السابعة", 8: "الثامنة", 9: "التاسعة", 10: "العاشرة",
        11: "الحادية عشرة", 12: "الثانية عشرة", 13: "الثالثة عشرة", 14: "الرابعة عشرة",
        15: "الخامسة عشرة", 16: "السادسة عشرة", 17: "السابعة عشرة", 18: "الثامنة عشرة",
        19: "التاسعة عشرة", 20: "العشرون"
    }

    def __init__(self):
        self.project_data = {}

    def generate_content(self, placeholder_name: str, project_data: Dict[str, Any]) -> str:
        """
        Generate appropriate content for a specific placeholder
        """
        self.project_data = project_data

        # Map placeholder names to generation methods
        generator_methods = {
            "project_scope": self._generate_project_scope,
            "work_program_phases": self._generate_work_phases,
            "work_program_payment_method": self._generate_payment_schedule,
            "work_execution_method": self._generate_execution_method,
            "evaluation_criteria": self._generate_evaluation_criteria,
            "required_certificates": self._generate_required_certificates,
            "technical_specifications": self._generate_technical_specs,
            "quality_standards": self._generate_quality_standards,
            "safety_requirements": self._generate_safety_requirements,
            "deliverables": self._generate_deliverables,
            "project_objectives": self._generate_objectives
        }

        # Check if we have a specific generator for this placeholder
        if placeholder_name in generator_methods:
            return generator_methods[placeholder_name]()

        # Return the raw value if no special generation needed
        return str(project_data.get(placeholder_name, ""))

    def _generate_project_scope(self) -> str:
        """
        Generate comprehensive project scope following Saudi government guidelines
        Must be clear, detailed, and avoid brand-specific references
        """
        project_name = self.project_data.get("project_name", "المشروع")
        project_type = self.project_data.get("project_type", "")
        objectives = self.project_data.get("project_objectives", "")
        deliverables = self.project_data.get("deliverables", "")
        requirements = self.project_data.get("requirements", "")
        training_required = self.project_data.get("training_required", "نعم")

        # Start with user-provided scope if available
        base_scope = self.project_data.get("project_scope", "")

        # Build comprehensive scope
        scope = f"""نطاق عمل {project_name}

{base_scope if base_scope else 'يتضمن هذا المشروع تنفيذ الأعمال والخدمات المطلوبة وفقاً للمواصفات والشروط المحددة في هذه الكراسة.'}

الأهداف الرئيسية:
{objectives if objectives else self._generate_default_objectives(project_type)}

المخرجات المتوقعة:
{deliverables if deliverables else self._generate_default_deliverables(project_type)}

المتطلبات الأساسية:
{requirements if requirements else self._generate_default_requirements(project_type)}
"""

        # Add training section if required
        if training_required == "نعم":
            scope += """
التدريب ونقل المعرفة:
يلتزم المتعاقد بتدريب فريق عمل الجهة الحكومية ونقل المعرفة والخبرة لموظفيها بكافة الوسائل الممكنة ومن ذلك:
• التدريب على رأس العمل
• العمل جنباً إلى جنب مع الموظفين
• ورش العمل التدريبية المتخصصة
• توفير الأدلة والوثائق التدريبية
وذلك بما يكفل حصولهم على المعرفة والخبرة اللازمة لإدارة وتشغيل مخرجات المشروع.
"""

        # Add compliance note
        scope += """
ملاحظة مهمة:
• يجب عدم الإشارة إلى علامة تجارية أو ماركة محددة أو نوع محدد في العرض المقدم
• يجب أن تتوافق جميع المواصفات مع المعايير المعتمدة في المملكة العربية السعودية
• يلتزم المتعاقد بتطبيق متطلبات المحتوى المحلي حسب النسب المحددة
"""

        return scope.strip()

    def _generate_work_phases(self) -> str:
        """
        Generate work program phases with timeline
        """
        duration_months = self.project_data.get("duration_months", 6)
        phases_data = self.project_data.get("work_program_phases", "")

        # If phases are provided as structured data
        if isinstance(phases_data, list):
            return self._format_phases_from_list(phases_data)

        # If phases are provided as text
        if phases_data and isinstance(phases_data, str):
            return self._format_phases_from_text(phases_data)

        # Generate default phases based on project type
        return self._generate_default_phases(duration_months)

    def _format_phases_from_list(self, phases: List[Dict[str, Any]]) -> str:
        """Format phases from structured list"""
        formatted = f"""برنامج العمل ومراحل التنفيذ

تبدأ الأعمال الخاصة بالمشروع من تاريخ توقيع العقد وإشعار المباشرة.
المدة الكلية للتنفيذ: {self.project_data.get('duration_months', 6)} شهراً ميلادياً.

مراحل تنفيذ المشروع كالتالي:
"""
        for i, phase in enumerate(phases, 1):
            phase_name = phase.get("phase_name", f"مرحلة {i}")
            phase_duration = phase.get("duration", "")
            phase_description = phase.get("description", "")

            formatted += f"\nالمرحلة {self.ARABIC_ORDINALS.get(i, f'رقم {i}')}: {phase_name}\n"
            formatted += f"المدة: {phase_duration}\n"
            if phase_description:
                formatted += f"الوصف: {phase_description}\n"

        formatted += """
ملاحظات:
• يجب عرض أي أعمال أو مواد تحتاج إلى اعتماد على الإدارة المشرفة خلال 15 يوم عمل من توقيع العقد
• بمجرد اعتماد العمل أو المادة، يجب البدء الفوري في التنفيذ
• يلتزم المتعاقد بتقديم تقارير دورية عن سير العمل
"""

        return formatted

    def _format_phases_from_text(self, phases_text: str) -> str:
        """Format phases from plain text input"""
        formatted = f"""برنامج العمل ومراحل التنفيذ

تبدأ الأعمال الخاصة بالمشروع من تاريخ توقيع العقد وإشعار المباشرة.
المدة الكلية للتنفيذ: {self.project_data.get('duration_months', 6)} شهراً ميلادياً.

مراحل تنفيذ المشروع كالتالي:
"""

        # Parse text to extract phases
        lines = phases_text.split('\n')
        phase_num = 1
        for line in lines:
            if line.strip():
                # Check if line already starts with phase number
                if not re.match(r'^المرحلة', line):
                    formatted += f"\nالمرحلة {self.ARABIC_ORDINALS.get(phase_num, f'رقم {phase_num}')}: {line.strip()}\n"
                    phase_num += 1
                else:
                    formatted += f"\n{line.strip()}\n"

        return formatted

    def _generate_default_phases(self, duration_months: int) -> str:
        """Generate default phases based on project duration"""
        phases = []

        if duration_months <= 3:
            phases = [
                ("التحضير والتخطيط", "2 أسابيع"),
                ("التنفيذ والتطوير", f"{duration_months - 1} شهر"),
                ("الاختبار والتسليم", "2 أسابيع")
            ]
        elif duration_months <= 6:
            phases = [
                ("التحليل والتصميم", "1 شهر"),
                ("التطوير والتنفيذ", f"{duration_months - 2} أشهر"),
                ("الاختبار والتدريب", "2 أسابيع"),
                ("التسليم والدعم", "2 أسابيع")
            ]
        else:
            phases = [
                ("دراسة الوضع الحالي والتحليل", "1.5 شهر"),
                ("التصميم والتخطيط التفصيلي", "1.5 شهر"),
                ("التنفيذ والتطوير", f"{duration_months - 5} أشهر"),
                ("الاختبار والتحسين", "1 شهر"),
                ("التدريب ونقل المعرفة", "2 أسابيع"),
                ("التسليم النهائي والدعم", "2 أسابيع")
            ]

        formatted = f"""برنامج العمل ومراحل التنفيذ

تبدأ الأعمال الخاصة بالمشروع من تاريخ توقيع العقد وإشعار المباشرة.
المدة الكلية للتنفيذ: {duration_months} شهراً ميلادياً.

مراحل تنفيذ المشروع كالتالي:
"""

        for i, (phase_name, duration) in enumerate(phases, 1):
            formatted += f"\nالمرحلة {self.ARABIC_ORDINALS.get(i, f'رقم {i}')}: {phase_name}\n"
            formatted += f"المدة: {duration}\n"

        return formatted

    def _generate_payment_schedule(self) -> str:
        """
        Generate payment schedule and method
        """
        payment_method = self.project_data.get("payment_method", "دفعات حسب المراحل")
        payment_data = self.project_data.get("work_program_payment_method", "")

        # If payment schedule is provided
        if payment_data and isinstance(payment_data, str):
            return self._format_payment_from_text(payment_data)

        # Generate default payment schedule
        return self._generate_default_payment_schedule(payment_method)

    def _format_payment_from_text(self, payment_text: str) -> str:
        """Format payment schedule from text"""
        formatted = """طريقة الدفع:

يكون طريقة الدفع وفقاً لشهادة الإنجاز الصادرة من الإدارة المشرفة على التنفيذ مع تقديم الفواتير والمستندات المطلوبة.

جدول الدفعات:
"""

        lines = payment_text.split('\n')
        payment_num = 1
        for line in lines:
            if line.strip():
                if not re.match(r'^الدفعة', line):
                    formatted += f"\nالدفعة {self.ARABIC_ORDINALS.get(payment_num, f'رقم {payment_num}')}: {line.strip()}\n"
                    payment_num += 1
                else:
                    formatted += f"\n{line.strip()}\n"

        formatted += """
شروط الدفع:
• يتم الصرف بعد اعتماد الإنجاز من الإدارة المشرفة
• تقديم الفواتير الضريبية حسب النظام
• تقديم ضمان حسن الأداء عند الدفعة الأولى
• الالتزام بالجدول الزمني المعتمد
"""

        return formatted

    def _generate_default_payment_schedule(self, payment_method: str) -> str:
        """Generate default payment schedule based on method"""
        if payment_method == "دفعة واحدة عند الانتهاء":
            return """طريقة الدفع:

يتم صرف كامل قيمة العقد (100%) عند الانتهاء من جميع الأعمال واعتمادها من الإدارة المشرفة على التنفيذ."""

        elif payment_method == "دفعة شهرية":
            return """طريقة الدفع:

يتم الدفع بشكل شهري بناءً على الإنجاز الفعلي للأعمال وبعد اعتماد التقرير الشهري من الإدارة المشرفة."""

        else:  # Default to milestone-based payments
            return """طريقة الدفع:

يكون طريقة الدفع وفقاً لشهادة الإنجاز الصادرة من الإدارة المشرفة على التنفيذ مع تقديم الفواتير والمستندات المطلوبة.

جدول الدفعات:

الدفعة الأولى: 20% بعد توقيع العقد وتقديم ضمان حسن الأداء
الدفعة الثانية: 30% بعد إنجاز 50% من الأعمال
الدفعة الثالثة: 30% بعد إنجاز 80% من الأعمال
الدفعة الرابعة: 20% بعد التسليم النهائي واعتماد جميع المخرجات

شروط الدفع:
• يتم الصرف بعد اعتماد الإنجاز من الإدارة المشرفة
• تقديم الفواتير الضريبية حسب النظام
• الالتزام بالجدول الزمني المعتمد"""

    def _generate_execution_method(self) -> str:
        """
        Generate work execution method details
        """
        execution_data = self.project_data.get("work_execution_method", "")
        project_type = self.project_data.get("project_type", "")

        if execution_data:
            return execution_data

        # Generate based on project type
        if project_type == "تقنية المعلومات":
            return self._generate_it_execution_method()
        elif project_type == "البناء والتشييد":
            return self._generate_construction_execution_method()
        elif project_type == "الاستشارات":
            return self._generate_consulting_execution_method()
        else:
            return self._generate_general_execution_method()

    def _generate_it_execution_method(self) -> str:
        """Generate execution method for IT projects"""
        return """طريقة تنفيذ الأعمال:

الخدمات المطلوبة:
• تحليل وتصميم النظام حسب المتطلبات
• تطوير وبرمجة التطبيقات والواجهات
• إعداد قواعد البيانات وهيكلتها
• تكامل النظام مع الأنظمة القائمة
• إجراء الاختبارات الشاملة

المنهجية المتبعة:
• استخدام منهجية Agile للتطوير التكراري
• عقد اجتماعات دورية لمراجعة التقدم
• توثيق جميع مراحل العمل

المواد والأدوات:
• بيئات التطوير والاختبار المناسبة
• أدوات إدارة المشروع والتواصل
• منصات الاستضافة والخوادم المطلوبة

معايير الجودة:
• الالتزام بمعايير ISO/IEC 25010 لجودة البرمجيات
• تطبيق أفضل ممارسات الأمن السيبراني
• توفير وثائق فنية شاملة

الاختبارات المطلوبة:
• اختبارات الوحدات (Unit Testing)
• اختبارات التكامل (Integration Testing)
• اختبارات الأداء والحمل
• اختبارات الأمان والاختراق
• اختبارات القبول من المستخدمين"""

    def _generate_construction_execution_method(self) -> str:
        """Generate execution method for construction projects"""
        return """طريقة تنفيذ الأعمال:

الخدمات المطلوبة:
• إعداد الموقع وأعمال الحفر
• أعمال البناء والتشييد
• التشطيبات والأعمال النهائية
• التركيبات الكهربائية والميكانيكية

المواد المستخدمة:
• مواد البناء المطابقة للمواصفات السعودية
• استخدام مواد معتمدة من الجهات المختصة
• الالتزام بنسب المحتوى المحلي

القياسات والمواصفات:
• تطبيق كود البناء السعودي
• الالتزام بالمخططات الهندسية المعتمدة
• مراعاة معايير السلامة والأمان

الاختبارات المطلوبة:
• فحص التربة والأساسات
• اختبارات مقاومة الخرسانة
• فحص أنظمة السلامة
• الفحص النهائي والتسليم الابتدائي"""

    def _generate_consulting_execution_method(self) -> str:
        """Generate execution method for consulting projects"""
        return """طريقة تنفيذ الأعمال:

الخدمات الاستشارية المطلوبة:
• دراسة وتحليل الوضع الحالي
• إعداد التوصيات والحلول المقترحة
• وضع الخطط الاستراتيجية والتنفيذية
• تقديم الدعم الفني والإداري

منهجية العمل:
• إجراء المقابلات وورش العمل
• تحليل البيانات والمعلومات
• إعداد التقارير التفصيلية
• عرض النتائج والتوصيات

المخرجات المتوقعة:
• تقارير تحليلية شاملة
• خطط عمل قابلة للتنفيذ
• أدلة إرشادية وإجرائية
• عروض تقديمية للنتائج

معايير الجودة:
• الالتزام بأفضل الممارسات الدولية
• تطبيق معايير الاستشارات المهنية
• ضمان سرية المعلومات"""

    def _generate_general_execution_method(self) -> str:
        """Generate general execution method"""
        return """طريقة تنفيذ الأعمال:

الخدمات المطلوبة:
• تنفيذ جميع الأعمال حسب المواصفات المحددة
• توفير الموارد البشرية والمادية اللازمة
• التنسيق مع الجهة المستفيدة
• ضمان جودة التنفيذ

المواد والمعدات:
• استخدام مواد ومعدات مطابقة للمواصفات
• توفير جميع الأدوات اللازمة للتنفيذ
• الالتزام بمعايير السلامة

الاختبارات والفحوصات:
• إجراء الاختبارات اللازمة للتأكد من الجودة
• تقديم شهادات الفحص والاختبار
• اعتماد النتائج من الجهة المشرفة"""

    def _generate_evaluation_criteria(self) -> str:
        """Generate evaluation criteria with weights"""
        tech_weight = self.project_data.get("technical_weight", 60)
        financial_weight = self.project_data.get("financial_weight", 40)

        return f"""معايير تقييم العروض:

سيتم تقييم العروض المقدمة وفقاً للمعايير التالية:

1. التقييم الفني ({tech_weight}%):
   • الملاءمة الفنية للعرض مع المتطلبات: 40%
   • منهجية التنفيذ وخطة العمل: 20%
   • خبرات الفريق والمؤهلات: 20%
   • الخبرات السابقة في مشاريع مماثلة: 15%
   • الابتكار والقيمة المضافة: 5%

2. التقييم المالي ({financial_weight}%):
   • تنافسية السعر المقدم
   • وضوح التسعير والشفافية
   • القيمة مقابل المال

معادلة التقييم:
النقاط النهائية = (النقاط الفنية × {tech_weight/100}) + (النقاط المالية × {financial_weight/100})

ملاحظات:
• الحد الأدنى للنجاح في التقييم الفني: 70%
• يتم استبعاد العروض التي لا تحقق الحد الأدنى
• الترسية على صاحب أعلى نقاط نهائية"""

    def _generate_required_certificates(self) -> str:
        """Generate list of required certificates"""
        certificates = self.project_data.get("required_certificates", "")

        if certificates:
            return certificates

        return """السجلات والتراخيص النظامية المطلوبة:

يجب على المتقدمين تقديم الوثائق التالية سارية المفعول:

1. السجل التجاري ساري المفعول
2. شهادة الزكاة والدخل
3. شهادة التأمينات الاجتماعية
4. شهادة الغرفة التجارية
5. رخصة الاستثمار (للشركات الأجنبية)
6. شهادة السعودة ونطاقات
7. شهادة تصنيف المقاولين (حسب طبيعة المشروع)
8. التراخيص المهنية ذات العلاقة
9. شهادة تسجيل ضريبة القيمة المضافة

ملاحظات:
• جميع الشهادات يجب أن تكون سارية المفعول
• يجب تحميل نسخ واضحة على منصة اعتماد
• عدم استيفاء الوثائق يؤدي للاستبعاد"""

    def _generate_technical_specs(self) -> str:
        """Generate technical specifications"""
        specs = self.project_data.get("technical_specifications", "")
        project_type = self.project_data.get("project_type", "")

        if specs:
            return specs

        if project_type == "تقنية المعلومات":
            return """المواصفات الفنية:

متطلبات النظام:
• التوافق مع الأنظمة القائمة
• دعم اللغة العربية بشكل كامل
• واجهات مستخدم سهلة وبديهية
• قابلية التوسع والتطوير
• الأمان وحماية البيانات

المعايير التقنية:
• دعم المعايير القياسية (REST APIs, JSON, XML)
• التوافق مع المتصفحات الحديثة
• Responsive Design للأجهزة المختلفة
• معايير الأمن السيبراني NIST

متطلبات الأداء:
• زمن الاستجابة أقل من 3 ثواني
• دعم عدد متزامن من المستخدمين
• نسبة توفر 99.5% على الأقل"""

        return """المواصفات الفنية:

يجب أن تتوافق جميع الأعمال والمواد مع:
• المواصفات القياسية السعودية
• المعايير الدولية المعتمدة
• متطلبات الجهة المستفيدة
• أنظمة السلامة والأمان"""

    def _generate_quality_standards(self) -> str:
        """Generate quality standards"""
        standards = self.project_data.get("quality_standards", "")

        if standards:
            return standards

        return """معايير الجودة:

• الالتزام بنظام إدارة الجودة ISO 9001
• تطبيق معايير الجودة الخاصة بالقطاع
• توفير ضمانات الجودة للمخرجات
• إجراء مراجعات دورية للجودة
• تقديم تقارير الجودة والأداء
• معالجة الملاحظات خلال المدة المحددة"""

    def _generate_safety_requirements(self) -> str:
        """Generate safety requirements"""
        safety = self.project_data.get("safety_requirements", "")

        if safety:
            return safety

        return """متطلبات السلامة:

• الالتزام بأنظمة السلامة المهنية
• توفير معدات الوقاية الشخصية
• تدريب العاملين على إجراءات السلامة
• وضع خطة طوارئ معتمدة
• التأمين ضد المخاطر
• الإبلاغ الفوري عن الحوادث"""

    def _generate_deliverables(self) -> str:
        """Generate project deliverables"""
        deliverables = self.project_data.get("deliverables", "")

        if deliverables:
            return deliverables

        project_type = self.project_data.get("project_type", "")

        if project_type == "تقنية المعلومات":
            return """المخرجات المطلوبة:

• النظام/التطبيق كاملاً وجاهزاً للتشغيل
• الكود المصدري مع حقوق الملكية
• قواعد البيانات مع البيانات الأساسية
• الوثائق الفنية الشاملة
• أدلة المستخدم والمسؤول
• خطة الصيانة والدعم الفني
• التدريب للمستخدمين
• فترة دعم فني مجاني"""

        return """المخرجات المطلوبة:

• تسليم جميع مخرجات المشروع حسب المواصفات
• الوثائق والتقارير المطلوبة
• الأدلة والإرشادات
• شهادات الضمان والجودة
• التدريب ونقل المعرفة"""

    def _generate_objectives(self) -> str:
        """Generate project objectives"""
        objectives = self.project_data.get("project_objectives", "")

        if objectives:
            return objectives

        project_name = self.project_data.get("project_name", "المشروع")

        return f"""أهداف {project_name}:

• تحسين كفاءة العمليات وزيادة الإنتاجية
• توفير حلول متكاملة وفعالة
• تطبيق أفضل الممارسات والمعايير
• ضمان الاستدامة والتطوير المستمر
• تحقيق الأهداف الاستراتيجية للجهة"""

    def _generate_default_objectives(self, project_type: str) -> str:
        """Generate default objectives based on project type"""
        if project_type == "تقنية المعلومات":
            return """• أتمتة العمليات وتحسين الكفاءة التشغيلية
• توفير منصة رقمية متكاملة وآمنة
• تحسين تجربة المستخدم والعملاء
• دعم اتخاذ القرار بالبيانات والتقارير
• ضمان حماية وأمن المعلومات"""

        elif project_type == "البناء والتشييد":
            return """• إنشاء مرافق حديثة وفق أعلى المعايير
• ضمان السلامة الإنشائية والمتانة
• الالتزام بالجدول الزمني والميزانية
• تطبيق معايير الاستدامة البيئية"""

        return """• تحقيق أهداف المشروع بكفاءة وفعالية
• ضمان الجودة في جميع المخرجات
• الالتزام بالجدول الزمني المحدد
• تحقيق القيمة المضافة للجهة"""

    def _generate_default_deliverables(self, project_type: str) -> str:
        """Generate default deliverables based on project type"""
        if project_type == "تقنية المعلومات":
            return """• النظام/التطبيق مكتمل وجاهز للتشغيل
• الوثائق الفنية والأدلة الإرشادية
• التدريب للمستخدمين والفريق الفني
• الدعم الفني وفترة الضمان"""

        elif project_type == "الاستشارات":
            return """• التقارير التحليلية والدراسات
• الخطط الاستراتيجية والتنفيذية
• التوصيات وخطط التحسين
• ورش العمل والعروض التقديمية"""

        return """• جميع مخرجات المشروع حسب المواصفات
• التقارير والوثائق المطلوبة
• التدريب ونقل المعرفة
• الضمانات والدعم الفني"""

    def _generate_default_requirements(self, project_type: str) -> str:
        """Generate default requirements based on project type"""
        if project_type == "تقنية المعلومات":
            return """• خبرة مثبتة في تنفيذ مشاريع مماثلة
• فريق عمل متخصص ومؤهل
• القدرة على التكامل مع الأنظمة القائمة
• الالتزام بمعايير الأمن السيبراني
• توفير الدعم الفني والصيانة"""

        return """• الخبرة والكفاءة في مجال المشروع
• توفير الموارد البشرية والمادية
• الالتزام بالمواصفات والمعايير
• القدرة على الإنجاز في الوقت المحدد"""


# Utility function for quick content generation
def generate_rfp_content(placeholder_name: str, project_data: Dict[str, Any]) -> str:
    """Quick utility to generate content for a placeholder"""
    generator = RFPContentGenerator()
    return generator.generate_content(placeholder_name, project_data)