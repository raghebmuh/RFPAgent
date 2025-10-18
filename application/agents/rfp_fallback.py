"""
RFP Fallback Handler - Works without file dependencies
"""

import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class RFPFallbackHandler:
    """
    Handles RFP generation when template files are not available
    """

    @staticmethod
    def generate_rfp_from_data(data: Dict[str, Any]) -> str:
        """
        Generate RFP document content as text when DOCX template is not available
        """

        # Extract data with Arabic keys
        project_name = data.get("project_name", data.get("اسم المنافسة", ""))
        tender_number = data.get("tender_number", data.get("رقم المنافسة", ""))
        location = data.get("location", data.get("مكان التنفيذ", ""))
        submission_date = data.get("submission_date", data.get("موعد التسليم", ""))
        start_date = data.get("start_date", data.get("موعد البداية", ""))
        project_scope = data.get("project_scope", data.get("وصف النشاط", ""))

        rfp_content = f"""
كراسة الشروط والمواصفات
========================

1. معلومات المنافسة
-------------------
• اسم المنافسة: {project_name}
• رقم المنافسة: {tender_number}
• مكان التنفيذ: {location}
• موعد البداية: {start_date}
• موعد التسليم: {submission_date}

2. نطاق العمل
--------------
{project_scope}

3. المتطلبات الأساسية
---------------------
• خبرة سابقة في مشاريع مماثلة
• فريق عمل متخصص
• القدرة على الإنجاز في الوقت المحدد
• الالتزام بمعايير الجودة

4. الشروط والأحكام
------------------
• يجب تقديم العروض قبل الموعد المحدد
• يلتزم المتعاقد بجميع الأنظمة واللوائح
• تطبق أحكام نظام المنافسات والمشتريات الحكومية
• يجب توفير ضمان أولي بنسبة 2% من قيمة العرض

5. معايير التقييم
-----------------
• التقييم الفني: 60%
• التقييم المالي: 40%
• الخبرات السابقة والمؤهلات
• منهجية التنفيذ

6. المستندات المطلوبة
---------------------
• السجل التجاري ساري المفعول
• شهادة الزكاة والدخل
• شهادة التأمينات الاجتماعية
• شهادة الغرفة التجارية
• العرض الفني والمالي

7. التواصل
----------
للاستفسارات، يرجى التواصل عبر:
• البريد الإلكتروني: rfp@organization.gov.sa
• الهاتف: 011-XXX-XXXX

---
تم إنشاء هذه الوثيقة آلياً بواسطة نظام RFPAgent
"""

        return rfp_content

    @staticmethod
    def process_rfp_request(message: str) -> Dict[str, Any]:
        """
        Process RFP request when main agent fails
        """
        try:
            # Extract data from message
            data = {}

            # Simple extraction logic
            lines = message.split('\n')
            for line in lines:
                if ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()

                        # Map Arabic keys to English
                        key_mapping = {
                            "اسم المنافسة": "project_name",
                            "رقم المنافسة": "tender_number",
                            "موعد التسليم": "submission_date",
                            "موعد البداية": "start_date",
                            "مكان التنفيذ": "location",
                            "وصف النشاط": "project_scope",
                            "وصف الشغط": "project_scope"
                        }

                        english_key = key_mapping.get(key, key)
                        data[english_key] = value

            # Generate RFP content
            rfp_content = RFPFallbackHandler.generate_rfp_from_data(data)

            return {
                "success": True,
                "content": rfp_content,
                "data": data,
                "message": "تم إنشاء مسودة وثيقة RFP بنجاح"
            }

        except Exception as e:
            logger.error(f"Error in RFP fallback handler: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "حدث خطأ في معالجة الطلب"
            }