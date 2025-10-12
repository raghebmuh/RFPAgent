# RFP Word Document Generation Feature - Setup Guide

## Overview
This feature enables RFPAgent to generate editable Word documents (.docx) with preview and download capabilities. The implementation uses a dockerized MCP (Model Context Protocol) server for document generation.

## Architecture

```
User Query → Agent → MCP-Doc Server → Word Document (.docx)
                ↓
            Preview in Chat
                ↓
            Download Button
```

## Components Implemented

### 1. MCP-Doc Docker Service
**Location:** `deployment/mcp-doc/`

- **Dockerfile**: Python 3.11 with python-docx and FastMCP
- **server.py**: FastMCP server exposing document generation tools
- **requirements.txt**: python-docx==1.1.2, fastmcp==2.11.0

**Available Tools:**
- `create_rfp_document()` - Create new RFP with title and metadata
- `add_section()` - Add sections with headings and content
- `add_table()` - Add tables to documents
- `save_document()` - Save and return file path
- `get_document_preview()` - Get preview for chat display
- `list_documents()` - List all active documents
- `delete_document()` - Delete document

### 2. Docker Integration
**Modified:** `deployment/docker-compose.yaml`

Added `mcp-doc` service:
- Exposed on port 8080
- Volume mounted for document persistence: `mcp_documents`
- Connected to default network

### 3. Backend API

#### RFP Template System
**Location:** `application/templates/rfp_template.py`

- Standard 10-section RFP structure
- Customizable sections
- Project-type specific templates
- Content generation helpers

#### Document API Routes
**Location:** `application/api/user/documents/routes.py`

**Endpoints:**
- `GET /api/documents/download/<doc_id>` - Download .docx file
- `GET /api/documents/preview/<doc_id>` - Get document preview
- `GET /api/documents/list` - List user's documents
- `POST /api/documents/save` - Save document metadata
- `DELETE /api/documents/delete/<doc_id>` - Delete document

#### Database
- New collection: `user_documents` in MongoDB
- Stores: doc_id, title, file_path, sections, user, timestamps

### 4. Frontend Components

#### DocumentRenderer Component
**Location:** `frontend/src/components/DocumentRenderer.tsx`

Features:
- Document preview with section structure
- Download dropdown button (similar to MermaidRenderer)
- Loading states
- Dark mode support

#### ConversationBubble Integration
**Modified:** `frontend/src/conversation/ConversationBubble.tsx`

- Added document pattern detection: ` ```document ... ``` `
- Renders DocumentRenderer for document blocks
- Parallel to Mermaid diagram rendering

## Usage Workflow

### 1. Setup MCP-Doc Server

First, register the MCP-Doc server in RFPAgent:

1. Go to **Settings → Tools**
2. Click **"Add MCP Server"**
3. Configure:
   - **Name**: MCP-Doc Server
   - **Server URL**: `http://mcp-doc:8081` (for Docker) or `http://localhost:8081` (local)
   - **Transport**: HTTP
   - **Auth Type**: None

4. Click **"Test Connection"** - should discover 7 tools
5. Click **"Save"**

### 2. Generate RFP Document

User asks:
```
"Generate an RFP document for a mobile app development project"
```

Agent workflow:
1. Calls `create_rfp_document` with project details
2. Calls `add_section` multiple times for each RFP section
3. Calls `get_document_preview` to generate preview
4. Calls `save_document` to finalize
5. Returns markdown with document block:

```markdown
I've generated the RFP document for your mobile app project.

\```document
{
  "doc_id": "abc-123-def",
  "title": "RFP for Mobile App Development",
  "sections": [
    {"heading": "1. Executive Summary", "level": 1},
    {"heading": "2. Project Overview", "level": 1},
    ...
  ],
  "preview_text": "# RFP for Mobile App Development\n\nProject: Mobile App\nSections: 10\n\n## Document Structure:\n1. Executive Summary\n2. Project Overview\n..."
}
\```
```

### 3. Preview & Download

- User sees **DocumentRenderer** in chat with:
  - Document title
  - Section structure (10 sections listed)
  - Preview text
  - **Download** button

- Click **"Download as DOCX"** → editable Word document downloaded

## Document Format Example

The generated Word document includes:

```
[Title Page]
RFP for Mobile App Development

Project: Mobile App Development
Issued by: [Company Name]
Date: December 14, 2025

[Page Break]

1. Executive Summary
[Content about project overview and objectives]

2. Project Overview
[Detailed project description]

2.1 Project Objectives
[Specific goals and KPIs]

2.2 Project Scope
[In scope and out of scope items]

... [continues through all 10 sections]
```

## Configuration

### Environment Variables

No additional environment variables needed. The MCP-Doc server runs standalone.

### Volume Mounts

Documents are stored in Docker volume: `mcp_documents`
- Backend can access via shared volume
- Persists across container restarts

## Testing

### 1. Start Services

```bash
cd deployment
docker-compose up --build
```

### 2. Register MCP Server

Follow "Setup MCP-Doc Server" steps above.

### 3. Test Generation

Ask agent:
```
"Create an RFP document for a cloud infrastructure migration project with a budget of $500K"
```

Expected behavior:
1. Agent shows "thinking" with tool calls
2. Preview appears in chat with document structure
3. Download button is functional
4. Downloaded .docx is editable in Microsoft Word/LibreOffice

### 4. Test Download

- Click "Download as DOCX"
- File downloads as `RFP_for_Cloud_Infrastructure_Migration_abc12345.docx`
- Open in Word - all sections are editable
- Formatting is preserved

## Troubleshooting

### MCP Server Not Connecting

**Issue**: Agent can't discover MCP-Doc tools

**Solution**:
```bash
# Check if mcp-doc container is running
docker ps | grep mcp-doc

# Check logs
docker logs rfp-agent-mcp-doc-1

# Verify network connectivity
docker exec rfp-agent-backend-1 ping mcp-doc
```

### Document Not Generating

**Issue**: Agent returns error when trying to create document

**Solution**:
1. Check MCP server logs:
   ```bash
   docker logs -f rfp-agent-mcp-doc-1
   ```

2. Verify tool configuration in Settings → Tools
3. Ensure `user_documents` collection exists in MongoDB

### Download Fails

**Issue**: Download button doesn't work

**Solution**:
1. Check browser console for errors
2. Verify file exists:
   ```bash
   docker exec rfp-agent-mcp-doc-1 ls -la /app/documents
   ```
3. Check backend API logs for /api/documents/download errors

### Preview Not Showing

**Issue**: Document block doesn't render in chat

**Solution**:
1. Verify agent returns proper markdown format:
   ```markdown
   \```document
   {"doc_id": "...", "title": "...", ...}
   \```
   ```

2. Check browser console for React rendering errors
3. Ensure DocumentRenderer component imported correctly

## Future Enhancements

### Planned Features
1. **PDF Export**: Add PDF conversion option
2. **Template Customization**: UI for custom RFP templates
3. **Collaborative Editing**: Multiple users editing same RFP
4. **Version History**: Track document revisions
5. **Direct Editing**: Edit document content in chat before download

### Extending Document Types
To add new document types (e.g., proposals, contracts):

1. Add new template in `application/templates/`
2. Add corresponding tools in `deployment/mcp-doc/server.py`
3. Update DocumentRenderer to handle new formats

## API Reference

### MCP Tools

#### create_rfp_document
```python
{
  "title": str,
  "project_name": str,
  "company_name": Optional[str],
  "date": Optional[str]
}
Returns: {"doc_id": str, "title": str, "message": str}
```

#### add_section
```python
{
  "doc_id": str,
  "heading": str,
  "content": str,
  "level": int  # 1-4
}
Returns: {"success": bool, "section_added": str}
```

#### save_document
```python
{
  "doc_id": str
}
Returns: {"file_name": str, "file_path": str}
```

### REST API

#### Download Document
```
GET /api/documents/download/<doc_id>
Headers: Authorization: Bearer <token>
Returns: application/vnd.openxmlformats-officedocument.wordprocessingml.document
```

#### Get Preview
```
GET /api/documents/preview/<doc_id>
Headers: Authorization: Bearer <token>
Returns: {
  "doc_id": str,
  "title": str,
  "sections": [],
  "preview_text": str
}
```

## Files Modified/Created

### New Files
1. `deployment/mcp-doc/Dockerfile`
2. `deployment/mcp-doc/server.py`
3. `deployment/mcp-doc/requirements.txt`
4. `application/templates/__init__.py`
5. `application/templates/rfp_template.py`
6. `application/api/user/documents/__init__.py`
7. `application/api/user/documents/routes.py`
8. `frontend/src/components/DocumentRenderer.tsx`

### Modified Files
1. `deployment/docker-compose.yaml` - Added mcp-doc service
2. `application/requirements.txt` - Added python-docx
3. `application/api/user/base.py` - Added user_documents_collection
4. `application/api/user/routes.py` - Registered documents namespace
5. `frontend/src/components/types/index.ts` - Added DocumentRendererProps
6. `frontend/src/conversation/ConversationBubble.tsx` - Added document rendering support

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f mcp-doc backend`
2. Verify MCP server is registered and active in Settings
3. Test with simple example: "Generate a basic RFP document"

## License

Same as RFPAgent project license.
