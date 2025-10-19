# RFP Agent JSON Response Schema

## Overview
This document contains the complete JSON schema used by the RFP Agent for validating and generating RFP documents. The schema includes 21 placeholders that match the actual Word template.

## JSON Schema

```json
{
  "type": "object",
  "properties": {
    "tender_name": {
      "type": "string",
      "description": "اسم المنافسة",
      "example": "تطوير نظام إدارة المواعيد الإلكتروني"
    },
    "tender_number": {
      "type": "string",
      "description": "رقم المنافسة",
      "example": "2024-001",
      "pattern": "^[0-9A-Za-z\\-]+$"
    },
    "tender_purpose": {
      "type": "string",
      "description": "الغرض من المنافسة",
      "minLength": 50
    },
    "tender_documents_fees": {
      "type": "string",
      "description": "رسوم وثائق المنافسة",
      "example": "1500 ريال سعودي"
    },
    "technical_organization_name": {
      "type": "string",
      "description": "اسم الجهة الفنية",
      "example": "وزارة الصحة"
    },
    "definition_department": {
      "type": "string",
      "description": "الإدارة المسؤولة",
      "example": "إدارة تقنية المعلومات"
    },
    "project_scope": {
      "type": "string",
      "description": "نطاق العمل",
      "minLength": 100
    },
    "work_execution_method": {
      "type": "string",
      "description": "طريقة تنفيذ الأعمال"
    },
    "work_program_phases": {
      "type": "string",
      "description": "مراحل البرنامج الزمني"
    },
    "work_program_payment_method": {
      "type": "string",
      "description": "طريقة الدفع"
    },
    "technical_inquiries_entity_name": {
      "type": "string",
      "description": "جهة الاستفسارات الفنية",
      "example": "إدارة المشاريع - وزارة الصحة"
    },
    "technical_inquiries_email": {
      "type": "string",
      "description": "البريد الإلكتروني للاستفسارات",
      "example": "rfp@organization.gov.sa",
      "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    },
    "technical_inquiries_alt_email": {
      "type": "string",
      "description": "البريد الإلكتروني البديل",
      "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    },
    "technical_inquiries_duration": {
      "type": "string",
      "description": "مدة الاستفسارات",
      "example": "5 أيام عمل"
    },
    "bids_review_proposals": {
      "type": "string",
      "description": "مراجعة العروض والمقترحات"
    },
    "purchase_reference": {
      "type": "string",
      "description": "المرجع الشرائي"
    },
    "supplier_samples_delivery_address": {
      "type": "string",
      "description": "عنوان تسليم العينات",
      "example": "المبنى الرئيسي، شارع الملك فهد، الرياض"
    },
    "samples_delivery_building": {
      "type": "string",
      "description": "المبنى",
      "example": "المبنى A"
    },
    "samples_delivery_floor": {
      "type": "string",
      "description": "الطابق",
      "example": "الطابق الثالث"
    },
    "samples_delivery_room_or_department": {
      "type": "string",
      "description": "الغرفة أو القسم",
      "example": "قسم المشتريات - غرفة 301"
    },
    "samples_delivery_time": {
      "type": "string",
      "description": "وقت تسليم العينات",
      "example": "من 9:00 صباحاً إلى 2:00 مساءً"
    }
  },
  "required": [
    "tender_name",
    "tender_number",
    "tender_purpose",
    "technical_organization_name",
    "project_scope",
    "work_execution_method",
    "work_program_phases",
    "work_program_payment_method",
    "technical_inquiries_entity_name",
    "technical_inquiries_email"
  ],
  "additionalProperties": false
}
```

## Required Fields (10 fields)
1. **tender_name** - اسم المنافسة
2. **tender_number** - رقم المنافسة
3. **tender_purpose** - الغرض من المنافسة
4. **technical_organization_name** - اسم الجهة الفنية
5. **project_scope** - نطاق العمل
6. **work_execution_method** - طريقة تنفيذ الأعمال
7. **work_program_phases** - مراحل البرنامج الزمني
8. **work_program_payment_method** - طريقة الدفع
9. **technical_inquiries_entity_name** - جهة الاستفسارات الفنية
10. **technical_inquiries_email** - البريد الإلكتروني للاستفسارات

## Optional Fields (11 fields)
1. **tender_documents_fees** - رسوم وثائق المنافسة
2. **definition_department** - الإدارة المسؤولة
3. **technical_inquiries_alt_email** - البريد الإلكتروني البديل
4. **technical_inquiries_duration** - مدة الاستفسارات
5. **bids_review_proposals** - مراجعة العروض والمقترحات
6. **purchase_reference** - المرجع الشرائي
7. **supplier_samples_delivery_address** - عنوان تسليم العينات
8. **samples_delivery_building** - المبنى
9. **samples_delivery_floor** - الطابق
10. **samples_delivery_room_or_department** - الغرفة أو القسم
11. **samples_delivery_time** - وقت تسليم العينات

## Field Details

### Basic Tender Information
| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| tender_name | string | ✅ Yes | - | اسم المنافسة أو المشروع |
| tender_number | string | ✅ Yes | Pattern: `^[0-9A-Za-z\-]+$` | رقم المنافسة (أرقام وحروف وشرطات فقط) |
| tender_purpose | string | ✅ Yes | Min Length: 50 | الغرض من المنافسة (50 حرف على الأقل) |
| tender_documents_fees | string | ❌ No | - | رسوم وثائق المنافسة |

### Organization Information
| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| technical_organization_name | string | ✅ Yes | - | اسم الجهة الحكومية أو المنظمة |
| definition_department | string | ❌ No | - | الإدارة أو القسم المسؤول |

### Project Details
| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| project_scope | string | ✅ Yes | Min Length: 100 | نطاق العمل التفصيلي (100 حرف على الأقل) |
| work_execution_method | string | ✅ Yes | - | طريقة تنفيذ الأعمال والخدمات |
| work_program_phases | string | ✅ Yes | - | مراحل التنفيذ والجدول الزمني |
| work_program_payment_method | string | ✅ Yes | - | طريقة الدفع ونسب الدفعات |

### Technical Inquiries
| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| technical_inquiries_entity_name | string | ✅ Yes | - | الجهة المسؤولة عن الاستفسارات |
| technical_inquiries_email | string | ✅ Yes | Email Pattern | البريد الإلكتروني الرئيسي |
| technical_inquiries_alt_email | string | ❌ No | Email Pattern | البريد الإلكتروني البديل |
| technical_inquiries_duration | string | ❌ No | - | المدة المتاحة للاستفسارات |

### Additional Information
| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| bids_review_proposals | string | ❌ No | - | معايير مراجعة العروض |
| purchase_reference | string | ❌ No | - | المرجع الشرائي أو رقم أمر الشراء |

### Samples Delivery (if applicable)
| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| supplier_samples_delivery_address | string | ❌ No | - | العنوان الكامل لتسليم العينات |
| samples_delivery_building | string | ❌ No | - | رقم أو اسم المبنى |
| samples_delivery_floor | string | ❌ No | - | الطابق |
| samples_delivery_room_or_department | string | ❌ No | - | رقم الغرفة أو القسم |
| samples_delivery_time | string | ❌ No | - | أوقات استلام العينات |

## Sample Valid JSON Response

```json
{
  "tender_name": "نظام إدارة المواعيد الإلكتروني",
  "tender_number": "2024-001",
  "tender_purpose": "تطوير نظام متكامل لإدارة المواعيد الطبية في جميع المستشفيات التابعة للوزارة",
  "tender_documents_fees": "1500 ريال سعودي",
  "technical_organization_name": "وزارة الصحة",
  "definition_department": "إدارة تقنية المعلومات",
  "project_scope": "نطاق العمل يشمل تطوير نظام متكامل لإدارة المواعيد الطبية مع المتطلبات التالية:\n- تطوير نظام ويب متكامل لإدارة المواعيد\n- تطبيقات موبايل للمرضى (iOS و Android)\n- لوحة تحكم إدارية شاملة\n- ربط النظام مع الأنظمة الصحية الحالية\n- توفير التدريب والدعم الفني المستمر",
  "work_execution_method": "سيتم تنفيذ المشروع باستخدام منهجية Agile مع تسليم المراحل بشكل تدريجي.\nالمتعاقد سيقوم بتوفير جميع الموارد البشرية والتقنية اللازمة.\nسيتم استخدام أحدث التقنيات والمعايير العالمية.\nالاختبارات ستشمل اختبارات الوحدة والتكامل والأداء والأمان.",
  "work_program_phases": "المرحلة الأولى: التحليل والتصميم - مدة شهرين\nالمرحلة الثانية: التطوير الأساسي - مدة 3 أشهر\nالمرحلة الثالثة: الاختبار والتحسين - مدة شهر واحد\nالمرحلة الرابعة: النشر والتدريب - مدة شهر واحد",
  "work_program_payment_method": "الدفعة الأولى: 30% عند توقيع العقد\nالدفعة الثانية: 40% عند الانتهاء من مرحلة التطوير\nالدفعة الثالثة: 20% عند اجتياز الاختبارات\nالدفعة النهائية: 10% بعد التسليم النهائي والتدريب",
  "technical_inquiries_entity_name": "إدارة المشاريع - وزارة الصحة",
  "technical_inquiries_email": "rfp@moh.gov.sa",
  "technical_inquiries_alt_email": "projects@moh.gov.sa",
  "technical_inquiries_duration": "5 أيام عمل",
  "bids_review_proposals": "سيتم تقييم العروض بناءً على المعايير الفنية والمالية المحددة",
  "purchase_reference": "PO-2024-001",
  "supplier_samples_delivery_address": "المبنى الرئيسي، شارع الملك فهد، الرياض",
  "samples_delivery_building": "المبنى A",
  "samples_delivery_floor": "الطابق الثالث",
  "samples_delivery_room_or_department": "قسم المشتريات - غرفة 301",
  "samples_delivery_time": "من 9:00 صباحاً إلى 2:00 مساءً"
}
```

## Usage Notes

1. **Required Fields**: The agent will ensure all 10 required fields are collected before generating the document.

2. **Validation**:
   - Email fields must match standard email format
   - Tender number can only contain letters, numbers, and hyphens
   - Project scope and tender purpose have minimum length requirements

3. **Multi-line Text**: Fields like `project_scope`, `work_execution_method`, `work_program_phases`, and `work_program_payment_method` support multi-line text with line breaks (`\n`).

4. **Default Values**: Optional fields that are not provided will be filled with appropriate defaults in the document generation process.

5. **Arabic Text**: All text fields support Arabic content and will be properly formatted in the generated document.

## API Integration

To programmatically submit RFP data:

```javascript
// Example API call
const rfpData = {
  "tender_name": "مشروع تطوير النظام",
  "tender_number": "2024-002",
  // ... other required fields
};

fetch('http://localhost:7091/api/agents/rfp/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(rfpData)
})
.then(response => response.json())
.then(data => {
  console.log('Document ID:', data.doc_id);
  console.log('Download URL:', data.download_url);
});
```

## Document Generation Flow

1. **Data Collection**: Agent collects all required fields from user
2. **Validation**: Data is validated against the JSON schema
3. **Content Generation**: Special fields get enhanced content generated
4. **Template Filling**: Word template placeholders are replaced with data
5. **Document Save**: Generated document is saved and assigned a unique ID
6. **Download Link**: User receives a download link for the completed RFP

## Files Location

- **Template**: `inputs/templates/rfp_template_with_placeholders.docx`
- **Generated Documents**: `outputs/rfp_documents/`
- **Schema Definition**: `application/models/rfp_template_placeholders.py`