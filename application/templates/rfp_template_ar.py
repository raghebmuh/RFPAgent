"""
RFP Template System (Arabic / KSA Etimad-style)
Provides standard Arabic RFP (كراسة الشروط والمواصفات) structure, tables, and content scaffolds
aligned with common sections used by Saudi government entities (Etimad platform forms).

Notes:
- Headings, subheadings, and table schemas mirror typical sections: المقدمة، الأحكام العامة، إعداد العروض،
  تسليم العروض، تقييم العروض، متطلبات التعاقد، نطاق العمل، المواصفات، المحتوى المحلي، الشروط الخاصة، الملحقات.
- Typography guidance is provided (e.g., Sakkal Majalla 16pt) but actual styling depends on the exporter layer.
- This module returns structured data you can render to DOCX/PDF/HTML as you prefer.
- RTL text is preserved in data. Your renderer should set paragraph direction = RTL and language = ar-SA.

Example usage:
    from rfp_template_ar import RFPTemplateKSA
    ctx = {"entity_name": "المركز الوطني لتنمية الغطاء النباتي ومكافحة التصحر",
           "project_name": "تطبيق أتمتة خدمات تقنية المعلومات (المرحلة الأولى)",
           "tender_no": "9301471"}
    doc = RFPTemplateKSA.generate(ctx)
    md  = RFPTemplateKSA.render_markdown(doc)  # or render to DOCX with your pipeline
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


# -------------------------------
# Typography & layout preferences
# -------------------------------
STYLE = {
    "font_family": "Sakkal Majalla",  # recommended per many KSA RFPs
    "font_size_pt": 16,
    "heading_scale": {1: 1.25, 2: 1.1, 3: 1.0},
    "rtl": True,
    "page_margins_cm": {
        "top": 2.0,
        "bottom": 2.0,
        "left": 2.0,
        "right": 2.0,
    },
}


# -------------------------------
# Data structures
# -------------------------------
@dataclass
class TableSpec:
    title: str
    columns: List[str]
    rows: List[List[Any]] = field(default_factory=list)
    note: str = ""


@dataclass
class Section:
    code: str
    title: str
    level: int = 1
    articles: List[str] = field(default_factory=list)
    body: str = ""
    tables: List[TableSpec] = field(default_factory=list)
    children: List["Section"] = field(default_factory=list)


@dataclass
class Document:
    meta: Dict[str, Any]
    style: Dict[str, Any]
    sections: List[Section]


class RFPTemplateKSA:
    """Arabic Etimad-style RFP template builder."""

    # ---------------------------------
    # Default table schemas (placeholders)
    # ---------------------------------
    TABLES = {
        "key_dates": TableSpec(
            title="المواعيد المتعلقة بالمنافسة",
            columns=["المرحلة", "التاريخ", "الوقت", "ملاحظات"],
            rows=[],
            note="قم بتعبئة المواعيد حسب المنصة، مع مراعاة تمديدات المنصة عند الأعطال التقنية.",
        ),
        "certificates": TableSpec(
            title="السجلات والتراخيص النظامية",
            columns=["الوثيقة", "مطلوبة؟", "رقم/مرجع", "الصلاحية"],
            rows=[
                ["السجل التجاري", "مطلوبة", "", "سارية"],
                ["تصنيف المقاولين", "مطلوبة", "", "سارية"],
                ["شهادة الزكاة", "مطلوبة", "", "سارية"],
                ["شهادة الضريبة", "مطلوبة", "", "سارية"],
                ["التأمينات الاجتماعية", "مطلوبة", "", "سارية"],
                ["شهادة اشتراك الغرفة التجارية", "مطلوبة", "", "سارية"],
                ["رخصة الاستثمار", "مطلوبة", "", "سارية"],
                ["شهادة السعودة", "مطلوبة", "", "سارية"],
                ["رخصة البلدية", "مطلوبة", "", "سارية"],
            ],
        ),
        "submission_files": TableSpec(
            title="وثائق العرض الفني والمالي",
            columns=["نوع الوثيقة", "الوصف", "إلزامي/اختياري"],
            rows=[
                ["العرض الفني", "منهجية التنفيذ + خطة العمل + الفريق + السيرة الذاتية", "إلزامي"],
                ["العرض المالي", "نموذج الأسعار وجداول الكميات", "إلزامي"],
                ["ضمان ابتدائي", "وفق النسبة المحددة إن وجدت", "إن وجد"],
                ["الجدول الزمني", "برنامج عمل تفصيلي", "إلزامي"],
                ["مراجع سابقة", "شواهد سابقة في نفس المجال", "اختياري/مرغوب"],
            ],
        ),
        "payment_schedule": TableSpec(
            title="جدول الدفعات",
            columns=["المرحلة/المخرج", "النسبة %", "قيمة الدفعة", "شروط/مستندات الصرف"],
            rows=[],
        ),
        "boq": TableSpec(
            title="جدول الكميات والأسعار",
            columns=["رقم البند", "الوصف", "الوحدة", "الكمية", "سعر الوحدة", "الإجمالي"],
            rows=[],
            note="يتم تحميل/تعبئة الجدول في منصة اعتماد. تأكد من مطابقة التسعير للعرض المالي في المنصة.",
        ),
        "eval": TableSpec(
            title="معايير تقييم العروض",
            columns=["المعيار", "الوزن", "الوصف", "آلية التقييم"],
            rows=[
                ["الملاءمة الفنية", "40%", "مدى توافق العرض مع المتطلبات الفنية", "مطابقة/تجاوز المتطلبات"],
                ["منهجية التنفيذ", "20%", "وضوح المنهجية والخطة الزمنية", "تحكيم لجنة فنية"],
                ["القدرات والخبرات", "20%", "خبرات الفريق والمراجع السابقة", "مراجعة السير الذاتية والمشاريع"],
                ["السعر", "20%", "التنافسية والوضوح", "المعادلة المالية المعتمدة"],
            ],
        ),
    }

    # ---------------------------------
    # Section tree builder
    # ---------------------------------
    @staticmethod
    def _build_sections(ctx: Dict[str, Any]) -> List[Section]:
        entity = ctx.get("entity_name", "[اسم الجهة]")
        project = ctx.get("project_name", "[اسم المنافسة]")
        tender_no = ctx.get("tender_no", "[رقم الكراسة]")
        contact = ctx.get("contact", {"dept": "[اسم الإدارة]", "email": "[البريد الإلكتروني]", "phone": "[الهاتف]"})

        مقدمة = Section(
            code="S1",
            title="القسم الأول: المقدمة",
            articles=[
                "1- تعريفات",
                f"2- تعريف عن المنافسة : {project}",
                "3- قيمة وثائق المنافسة",
                "4- المواعيد المتعلقة بالمنافسة",
                "5- أهلية مقدمي العروض",
                "6- السجلات والتراخيص النظامية",
                "7- ممثل الجهة",
                "8- مكان التسليم",
                "9- نظام المنافسة",
            ],
            body=(
                f"الجهة الحكومية: {entity}\n"
                f"رقم الكراسة/المنافسة: {tender_no}\n"
                "توضح هذه الكراسة نطاق المشروع ومتطلبات تقديم العروض وأطر التقييم والتعاقد."
            ),
            tables=[
                RFPTemplateKSA._clone_table("key_dates"),
                RFPTemplateKSA._clone_table("certificates"),
            ],
        )

        احكام_عامة = Section(
            code="S2",
            title="القسم الثاني: الأحكام العامة",
            articles=[
                "10- المساواة والشفافية",
                "11- تعارض المصالح",
                "12- السلوكيات والأخلاقيات",
                "13- السرية وإفشاء المعلومات",
                "14- ملكية وثائق المنافسة",
                "15- حقوق الملكية الفكرية",
                "16- المحتوى المحلي",
                "17- أنظمة وأحكام الاستيراد",
                "18- تجزئة المنافسة",
                "19- الاستبعاد من المنافسة",
                "20- إلغاء المنافسة وأثره",
                "21- التفاوض مع أصحاب العروض",
                "22- التضامن",
                "23- التعاقد من الباطن",
                "24- التأهيل اللاحق",
                "25- عدم الالتزام بالتعاقد",
                "26- الموافقة على الشروط",
            ],
            body=(
                "تلتزم الجهة بمبادئ المساواة والشفافية وتعارض المصالح وفق الأنظمة."
                " يجب على المتنافسين الالتزام بالسرية وحقوق الملكية وتطبيق متطلبات المحتوى المحلي."
            ),
        )

        اعداد_العروض = Section(
            code="S3",
            title="القسم الثالث: إعداد العروض",
            articles=[
                "27- تأكيد المشاركة بالمنافسة",
                "28- لغة العرض",
                "29- العملة المعتمدة",
                "30- صلاحية العروض",
                "31- تكلفة إعداد العروض",
                "32- الإخطارات والمراسلات",
                "33- ضمان المعلومات",
                "34- الأسئلة والاستفسارات",
                "35- الحصول على كافة المعلومات وزيارة موقع الأعمال",
                "36- وثائق العرض الفني",
                "37- وثائق العرض المالي",
                "38- كتابة الأسعار",
                "39- جدول الدفعات",
                "40- الضرائب والرسوم",
                "41- الأحكام العامة للضمانات",
                "42- الضمان الابتدائي",
                "43- مصادرة الضمانات",
                "44- العروض البديلة",
                "45- متطلبات تنسيق العروض",
            ],
            body=(
                "يُعد العرض باللغة العربية وبالعملة المعتمدة. يلتزم المتنافس بمدة صلاحية العرض"
                " وبتحميل الملفات بصيغة PDF مرتبة ومفهرسة (يفضل ملف واحد لكل من العرض الفني والمالي)."
            ),
            tables=[
                RFPTemplateKSA._clone_table("submission_files"),
                RFPTemplateKSA._clone_table("payment_schedule"),
            ],
        )

        تسليم_العروض = Section(
            code="S4",
            title="القسم الرابع: تسليم العروض",
            articles=[
                "46- تقديم العروض",
                "47- التسليم المتأخر",
                "48- تمديد فترة تلقي العروض وتأجيل فتحه",
                "49- الانسحاب",
                "50- فتح العروض",
            ],
            body=(
                "تُقدم العروض عبر منصة اعتماد. في حال تعطل المنصة يتم التسليم ورقياً حسب توجيهات الجهة"
                " مع توثيق ذلك."
            ),
        )

        تقييم_العروض = Section(
            code="S5",
            title="القسم الخامس: تقييم العروض",
            articles=[
                "51- سرية تقييم العروض",
                "52- معايير تقييم العروض",
                "53- تصحيح العروض",
                "54- فحص العروض",
                "55- الإعلان عن نتائج المنافسة",
                "56- فترة التوقف",
            ],
            body=(
                "تلتزم لجنة الفحص بالسرية، ويتم التقييم وفق معايير معلنة. في حال وجود أخطاء حسابية"
                " تجري التصحيحات وفق الأصول، ويتم إعلان النتائج عبر المنصة."
            ),
            tables=[RFPTemplateKSA._clone_table("eval")],
        )

        متطلبات_التعاقد = Section(
            code="S6",
            title="القسم السادس: متطلبات التعاقد",
            articles=["57- إخطار الترسية", "58- الضمان النهائي", "59- توقيع العقد"],
            body=(
                "بعد الترسية يُطلب تقديم الضمان النهائي ضمن المدة المحددة، ثم توقيع العقد وفق الشروط العامة والخاصة."
            ),
        )

        نطاق_العمل = Section(
            code="S7",
            title="القسم السابع: نطاق العمل المفصل",
            articles=["60- نطاق عمل المشروع", "61- برنامج العمل", "62- مكان تنفيذ الأعمال", "63- جدول الكميات والأسعار"],
            body=(
                "يتضمن هذا القسم وصفاً تفصيلياً لنطاق الأعمال والمخرجات المتوقعة وخطة التنفيذ ومكان التنفيذ."
            ),
            tables=[RFPTemplateKSA._clone_table("boq")],
        )

        المواصفات = Section(
            code="S8",
            title="القسم الثامن: المواصفات",
            articles=[
                "64- العمالة",
                "65- المواد",
                "66- المعدات",
                "67- كيفية تنفيذ الأعمال والخدمات",
                "68- مواصفات الجودة",
                "69- مواصفات السلامة",
            ],
            body=(
                "يلتزم المنفذ بمتطلبات السلامة والجودة والاشتراطات الفنية التفصيلية للعمالة والمواد والمعدات وآليات التنفيذ."
            ),
        )

        المحتوى_المحلي = Section(
            code="S9",
            title="القسم التاسع: متطلبات المحتوى المحلي",
            body=(
                "على المتنافسين الالتزام بمتطلبات المحتوى المحلي وفق السياسات المعتمدة، وتقديم خطط تعزيز المحتوى المحلي."
            ),
        )

        الشروط_الخاصة = Section(
            code="S10",
            title="القسم العاشر: الشروط الخاصة",
            body="تُدرج هنا أي شروط خاصة بالمشروع أو بالموقع أو بالتوريد أو بالخدمات السحابية/الاتصالية…",
        )

        الملحقات = Section(
            code="S11",
            title="القسم الحادي عشر: الملحقات",
            body=(
                "تُرفق النماذج والجداول والرسومات والمعايير المرجعية وأي مستندات توضيحية إضافية."
            ),
        )

        return [
            مقدمة,
            احكام_عامة,
            اعداد_العروض,
            تسليم_العروض,
            تقييم_العروض,
            متطلبات_التعاقد,
            نطاق_العمل,
            المواصفات,
            المحتوى_المحلي,
            الشروط_الخاصة,
            الملحقات,
        ]

    # ---------------------------------
    # Public API
    # ---------------------------------
    @staticmethod
    def generate(project_context: Optional[Dict[str, Any]] = None) -> Document:
        """Builds the Arabic RFP document skeleton with default tables and guidance."""
        ctx = project_context or {}
        meta = {
            "language": "ar",
            "entity_name": ctx.get("entity_name", "[اسم الجهة]"),
            "project_name": ctx.get("project_name", "[اسم المنافسة]"),
            "tender_no": ctx.get("tender_no", "[رقم الكراسة]"),
            "classification": ctx.get("classification", "تقنية المعلومات"),
        }
        sections = RFPTemplateKSA._build_sections(ctx)
        return Document(meta=meta, style=STYLE, sections=sections)

    @staticmethod
    def render_markdown(doc: Document) -> str:
        """Render the document structure to Markdown (RTL-friendly text)."""
        lines: List[str] = []
        m = doc.meta
        lines.append(f"# كراسة الشروط والمواصفات – {m.get('project_name')}\n")
        lines.append(f"**الجهة**: {m.get('entity_name')}  ")
        lines.append(f"**رقم الكراسة**: {m.get('tender_no')}  ")
        lines.append("")
        for s in doc.sections:
            h = "#" * s.level
            lines.append(f"{h} {s.title}")
            if s.articles:
                lines.append("\n".join([f"- {a}" for a in s.articles]))
            if s.body:
                lines.append(f"\n{s.body}\n")
            for t in s.tables:
                if not t.columns:
                    continue
                lines.append(f"\n**{t.title}**\n")
                # simple pipe table
                header = "|" + "|".join(t.columns) + "|"
                sep = "|" + "|".join(["---"] * len(t.columns)) + "|"
                lines.append(header)
                lines.append(sep)
                if t.rows:
                    for r in t.rows:
                        row = [str(x) if x is not None else "" for x in r]
                        lines.append("|" + "|".join(row) + "|")
                if t.note:
                    lines.append(f"\n> ملاحظة: {t.note}\n")
        return "\n".join(lines)

    # ---------------------------------
    # Helpers
    # ---------------------------------
    @staticmethod
    def _clone_table(key: str) -> TableSpec:
        base = RFPTemplateKSA.TABLES[key]
        return TableSpec(title=base.title, columns=list(base.columns), rows=[list(r) for r in base.rows], note=base.note)


# Optional: quick demo if run directly
if __name__ == "__main__":
    ctx = {
        "entity_name": "المركز الوطني لتنمية الغطاء النباتي ومكافحة التصحر",
        "project_name": "تطبيق أتمتة خدمات تقنية المعلومات للمركز (المرحلة الأولى)",
        "tender_no": "9301471",
    }
    d = RFPTemplateKSA.generate(ctx)
    print(RFPTemplateKSA.render_markdown(d))
