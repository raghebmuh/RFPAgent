# RFP Agent Feature Documentation

## Overview
The RFP Agent is a specialized AI agent designed to generate Saudi government-compliant Request for Proposal (RFP) documents through intelligent conversation. It collects project information from users, validates completeness, and generates professional RFP documents in Arabic with full RTL support.

## Features Implemented

### 1. Backend Components

#### Core Services
- **DocxPlaceholderService** (`application/services/docx_placeholder_service.py`)
  - Extracts placeholders from DOCX templates
  - Identifies dropdown fields
  - Validates data completeness

- **RFPContentGenerator** (`application/services/rfp_content_generator.py`)
  - Generates appropriate content for placeholders
  - Applies Saudi government RFP standards
  - Handles special formatting rules

- **DocxFillerService** (`application/services/docx_filler_service.py`)
  - Fills DOCX templates with data
  - Preserves original formatting
  - Supports Arabic RTL text

#### Agent Implementation
- **RFPAgent** (`application/agents/rfp_agent.py`)
  - Extends ReActAgent with RFP-specific functionality
  - Manages conversation flow
  - Tracks data collection progress
  - Validates and generates structured output

#### Tools
- **RFPReferenceTool** (`application/agents/tools/rfp_reference_tool.py`)
  - Searches RFP knowledge base
  - Provides best practices
  - Offers compliance guidance

#### Models
- **RFPPlaceholders** (`application/models/rfp_placeholders.py`)
  - Defines all expected placeholders
  - Provides validation rules
  - Generates questions for missing data

#### API Endpoints
Extended `application/api/user/documents/routes.py` with:
- `POST /api/documents/rfp/generate` - Generate RFP document
- `GET /api/documents/rfp/placeholders` - Get template placeholders
- `POST /api/documents/rfp/preview` - Preview RFP document
- `POST /api/documents/rfp/validate` - Validate RFP data

### 2. Frontend Components

#### UI Components
- **RFPProgressTracker** (`frontend/src/components/RFPProgressTracker.tsx`)
  - Visual progress indicator
  - Shows completed/missing fields
  - Displays completion percentage

- **RFPQuickInput** (`frontend/src/components/RFPQuickInput.tsx`)
  - Form-based data entry
  - Supports multiple input types
  - RTL Arabic support

### 3. Configuration & Scripts

- **Prompt Templates**
  - `application/prompts/rfp_agent_prompts.txt` - Arabic prompts
  - `application/prompts/rfp_react_prompt.txt` - English ReAct prompts

- **Setup Scripts**
  - `scripts/create_rfp_agent.py` - Creates RFP Agent via API
  - `scripts/test_rfp_workflow.py` - End-to-end testing

## How to Use

### 1. Install Dependencies
```bash
pip install -r application/requirements.txt
```
The following libraries were added for RFP support:
- python-docx==1.1.2 (already present)
- arabic-reshaper==3.0.0
- python-bidi==0.6.3

### 2. Create the RFP Agent

#### Option A: Using the Script
```bash
python scripts/create_rfp_agent.py --host http://localhost:5000 --token YOUR_TOKEN
```

#### Option B: Through the UI
1. Go to "Manage Agents" in the interface
2. Create a new agent with:
   - Name: وكيل طلب تقديم العروض
   - Type: ReAct
   - Add the RFP JSON schema
   - Enable rfp_reference_tool

### 3. Start a Conversation

1. Select the RFP Agent
2. Start a new chat
3. Provide project details in Arabic:
```
أريد إنشاء RFP لمشروع نظام إدارة المواعيد الإلكتروني لوزارة الصحة
```

4. Answer the agent's questions:
   - اسم الجهة: وزارة الصحة
   - رقم المنافسة: 2024-001
   - مدة التنفيذ: 6 أشهر
   - نوع المشروع: تقنية المعلومات
   - etc.

5. The agent will:
   - Show progress percentage
   - Ask for missing information
   - Validate data completeness
   - Generate the RFP document when ready

### 4. Generate & Download Document

Once all data is collected:
1. The agent generates the DOCX document
2. User receives a preview
3. Download button appears
4. Document is saved with all formatting preserved

## API Usage Examples

### Generate RFP Document
```javascript
const response = await fetch('/api/documents/rfp/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    entity_name: "وزارة الصحة",
    project_name: "نظام إدارة المواعيد",
    tender_number: "2024-001",
    project_scope: "تطوير نظام متكامل...",
    project_type: "تقنية المعلومات",
    duration_months: 6,
    placeholders: {
      // Additional placeholder data
    }
  })
});
```

### Get Placeholders
```javascript
const response = await fetch('/api/documents/rfp/placeholders', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

### Validate Data
```javascript
const response = await fetch('/api/documents/rfp/validate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    placeholders: {
      entity_name: "وزارة الصحة",
      project_name: "نظام إدارة المواعيد"
      // Partial data for validation
    }
  })
});
```

## Template Structure

The RFP template (`inputs/templates/rfp_template_with_placeholders.docx`) contains:

### Key Placeholders
- `{{entity_name}}` - Government entity name
- `{{project_name}}` - Project/tender name
- `{{tender_number}}` - Tender reference number
- `{{project_scope}}` - Detailed scope of work
- `{{work_program_phases}}` - Implementation phases
- `{{work_program_payment_method}}` - Payment schedule
- `{{work_execution_method}}` - Work methodology

### Dropdown Fields
- Project type selection
- Payment method selection
- Training requirement (Yes/No)
- Duration selection

## Testing

Run the end-to-end test suite:
```bash
python scripts/test_rfp_workflow.py
```

This tests:
1. Placeholder extraction
2. Content generation
3. Document filling
4. Data validation
5. Agent integration

## Architecture

```
RFP Agent Flow:
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│    User     │────▶│  RFP Agent   │────▶│ Placeholder     │
│  (Arabic)   │◀────│   (ReAct)    │◀────│   Service       │
└─────────────┘     └──────────────┘     └─────────────────┘
                            │                      │
                            ▼                      ▼
                    ┌──────────────┐     ┌─────────────────┐
                    │   Content    │     │  DOCX Filler    │
                    │  Generator   │────▶│    Service      │
                    └──────────────┘     └─────────────────┘
                                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │  Generated RFP  │
                                         │   Document      │
                                         └─────────────────┘
```

## Compliance Features

### Saudi Government Standards
- Arabic language with Najd dialect
- RTL text support throughout
- No brand/trademark mentions in scope
- Local content requirements
- Etimad platform compatibility

### Document Sections
1. المقدمة (Introduction)
2. الأحكام العامة (General Terms)
3. إعداد العروض (Proposal Preparation)
4. تسليم العروض (Proposal Submission)
5. تقييم العروض (Proposal Evaluation)
6. متطلبات التعاقد (Contract Requirements)
7. نطاق العمل (Scope of Work)
8. المواصفات (Specifications)
9. المحتوى المحلي (Local Content)
10. الشروط الخاصة (Special Conditions)
11. الملحقات (Attachments)

## Future Enhancements

1. **Template Management**
   - Multiple template support
   - Template versioning
   - Custom template upload

2. **Advanced Features**
   - Multi-language support
   - PDF export option
   - Digital signature integration
   - Etimad platform API integration

3. **AI Improvements**
   - Better context understanding
   - Industry-specific knowledge
   - Historical RFP analysis
   - Auto-suggestion for missing data

4. **Collaboration**
   - Multi-user editing
   - Review workflows
   - Comments and annotations
   - Version control

## Troubleshooting

### Common Issues

1. **Arabic text not displaying correctly**
   - Ensure arabic-reshaper and python-bidi are installed
   - Check that the DOCX template has RTL paragraph settings

2. **Placeholders not being replaced**
   - Verify placeholder format: `{{placeholder_name}}`
   - Check that placeholder names match exactly
   - Ensure data is provided for required fields

3. **Document generation fails**
   - Check template file exists in `inputs/templates/`
   - Verify output directory permissions
   - Review logs for specific errors

## Support

For issues or questions:
1. Check the test script output
2. Review API response errors
3. Check application logs
4. Verify all dependencies are installed

## License

This feature is part of the RFPAgent application and follows the project's licensing terms.