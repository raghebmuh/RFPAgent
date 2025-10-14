"""
MCP-Doc Server: FastMCP server for Word document generation
Provides tools for creating, editing, and managing .docx files with Arabic RFP template support
"""

import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.shared import OxmlElement, qn
from fastmcp import FastMCP

# Add application templates to path
sys.path.insert(0, '/app/application/templates')
try:
    from rfp_template_ar import RFPTemplateKSA, Section as RFPSection, TableSpec
except ImportError:
    RFPTemplateKSA = None
    RFPSection = None
    TableSpec = None
    print("Warning: Arabic RFP template not available")

# Initialize FastMCP server
mcp = FastMCP("MCP-Doc Server")

# Document storage
DOCUMENTS_DIR = Path("/app/documents")
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

# In-memory document store (doc_id -> Document object)
active_documents: Dict[str, Document] = {}
document_metadata: Dict[str, dict] = {}


def set_rtl_paragraph(paragraph):
    """Set paragraph direction to RTL (Right-to-Left) for Arabic text."""
    pPr = paragraph._element.get_or_add_pPr()
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    pPr.append(bidi)
    return paragraph


def set_arabic_font(run, font_name="Sakkal Majalla", font_size=16):
    """Set Arabic font for a text run."""
    run.font.name = font_name
    run.font.size = Pt(font_size)
    # Set font for complex scripts (Arabic, Hebrew, etc.)
    run._element.rPr.rFonts.set(qn('w:cs'), font_name)
    return run


@mcp.tool()
def create_rfp_document(
    title: str,
    project_name: str,
    company_name: Optional[str] = None,
    date: Optional[str] = None
) -> dict:
    """
    Create a new RFP (Request for Proposal) Word document with standard structure.

    Args:
        title: The title of the RFP document
        project_name: Name of the project for which RFP is being created
        company_name: Optional company name issuing the RFP
        date: Optional date (defaults to current date)

    Returns:
        dict with doc_id, title, and initial structure
    """
    doc_id = str(uuid.uuid4())
    doc = Document()

    # Set up document properties
    core_properties = doc.core_properties
    core_properties.title = title
    core_properties.subject = f"RFP for {project_name}"
    core_properties.author = company_name or "RFPAgent"

    # Add title
    title_paragraph = doc.add_heading(title, level=0)
    title_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Add document info
    info_paragraph = doc.add_paragraph()
    info_paragraph.add_run(f"Project: {project_name}").bold = True
    if company_name:
        doc.add_paragraph(f"Issued by: {company_name}")
    doc.add_paragraph(f"Date: {date or datetime.now().strftime('%B %d, %Y')}")

    # Add page break
    doc.add_page_break()

    # Store document
    active_documents[doc_id] = doc
    document_metadata[doc_id] = {
        "doc_id": doc_id,
        "title": title,
        "project_name": project_name,
        "created_at": datetime.now().isoformat(),
        "sections": []
    }

    return {
        "success": True,
        "doc_id": doc_id,
        "title": title,
        "message": f"RFP document '{title}' created successfully"
    }


@mcp.tool()
def create_arabic_rfp_document(
    title: str,
    project_name: str,
    entity_name: Optional[str] = None,
    tender_no: Optional[str] = None,
    date: Optional[str] = None
) -> dict:
    """
    Create a comprehensive Arabic RFP (كراسة الشروط والمواصفات) document with full KSA structure.

    This function generates a complete Arabic RFP document following the Saudi Arabian Etimad platform
    structure with 11 standard sections, proper RTL formatting, and Arabic typography.

    Args:
        title: The title of the RFP document (Arabic)
        project_name: Name of the project (Arabic)
        entity_name: Optional government entity name (Arabic)
        tender_no: Optional tender/RFP number
        date: Optional date (defaults to current date in Arabic)

    Returns:
        dict with doc_id, title, and full document structure
    """
    doc_id = str(uuid.uuid4())
    doc = Document()

    # Set up document properties
    core_properties = doc.core_properties
    core_properties.title = title
    core_properties.subject = f"كراسة الشروط والمواصفات - {project_name}"
    core_properties.author = entity_name or "RFPAgent"

    # Generate full RFP structure using template
    if RFPTemplateKSA:
        context = {
            "entity_name": entity_name or "[اسم الجهة]",
            "project_name": project_name,
            "tender_no": tender_no or "[رقم الكراسة]",
            "date": date or datetime.now().strftime('%Y/%m/%d')
        }

        rfp_doc = RFPTemplateKSA.generate(context)

        # Add title page with RTL support
        title_paragraph = doc.add_heading(title, level=0)
        title_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_rtl_paragraph(title_paragraph)
        for run in title_paragraph.runs:
            set_arabic_font(run, font_size=24)

        # Add document info with RTL support
        info_paragraph = doc.add_paragraph()
        set_rtl_paragraph(info_paragraph)
        run = info_paragraph.add_run(f"اسم المشروع: {project_name}")
        run.bold = True
        set_arabic_font(run, font_size=16)

        if entity_name:
            entity_para = doc.add_paragraph(f"الجهة: {entity_name}")
            set_rtl_paragraph(entity_para)
            for run in entity_para.runs:
                set_arabic_font(run)

        if tender_no:
            tender_para = doc.add_paragraph(f"رقم الكراسة: {tender_no}")
            set_rtl_paragraph(tender_para)
            for run in tender_para.runs:
                set_arabic_font(run)

        date_para = doc.add_paragraph(f"التاريخ: {date or datetime.now().strftime('%Y/%m/%d')}")
        set_rtl_paragraph(date_para)
        for run in date_para.runs:
            set_arabic_font(run)

        # Add page break
        doc.add_page_break()

        # Add all sections from template
        sections_added = []
        for section in rfp_doc.sections:
            # Add section heading
            heading_level = min(section.level, 3)  # Limit to level 3
            heading_para = doc.add_heading(section.title, level=heading_level)
            set_rtl_paragraph(heading_para)
            for run in heading_para.runs:
                set_arabic_font(run, font_size=18 if heading_level == 1 else 16)

            # Add articles as bullet points
            if section.articles:
                for article in section.articles:
                    para = doc.add_paragraph(article, style='List Bullet')
                    set_rtl_paragraph(para)
                    for run in para.runs:
                        set_arabic_font(run, font_size=14)

            # Add body content
            if section.body:
                body_para = doc.add_paragraph(section.body)
                set_rtl_paragraph(body_para)
                for run in body_para.runs:
                    set_arabic_font(run, font_size=14)
                doc.add_paragraph()  # Add spacing

            # Add tables
            for table_spec in section.tables:
                if table_spec.title:
                    table_title_para = doc.add_paragraph()
                    run = table_title_para.add_run(table_spec.title)
                    run.bold = True
                    set_rtl_paragraph(table_title_para)
                    set_arabic_font(run, font_size=14)

                # Create table
                rows = len(table_spec.rows) + 1  # +1 for header
                cols = len(table_spec.columns)
                if rows > 1 and cols > 0:
                    table = doc.add_table(rows=rows, cols=cols)
                    table.style = 'Light Grid Accent 1'

                    # Add header row
                    for j, col_name in enumerate(table_spec.columns):
                        cell = table.rows[0].cells[j]
                        cell.text = col_name
                        for paragraph in cell.paragraphs:
                            set_rtl_paragraph(paragraph)
                            for run in paragraph.runs:
                                run.font.bold = True
                                set_arabic_font(run, font_size=14)

                    # Add data rows
                    for i, row_data in enumerate(table_spec.rows, 1):
                        for j, cell_data in enumerate(row_data):
                            cell = table.rows[i].cells[j]
                            cell.text = str(cell_data) if cell_data else ""
                            for paragraph in cell.paragraphs:
                                set_rtl_paragraph(paragraph)
                                for run in paragraph.runs:
                                    set_arabic_font(run, font_size=13)

                if table_spec.note:
                    note_para = doc.add_paragraph(f"ملاحظة: {table_spec.note}")
                    set_rtl_paragraph(note_para)
                    for run in note_para.runs:
                        run.font.italic = True
                        set_arabic_font(run, font_size=12)

                doc.add_paragraph()  # Add spacing after table

            sections_added.append({
                "code": section.code,
                "title": section.title,
                "level": section.level
            })

        # Store document with full metadata
        active_documents[doc_id] = doc
        document_metadata[doc_id] = {
            "doc_id": doc_id,
            "title": title,
            "project_name": project_name,
            "entity_name": entity_name,
            "tender_no": tender_no,
            "created_at": datetime.now().isoformat(),
            "language": "ar",
            "rtl": True,
            "template": "KSA_Etimad",
            "sections": sections_added
        }

        return {
            "success": True,
            "doc_id": doc_id,
            "title": title,
            "language": "ar",
            "template": "KSA_Etimad",
            "sections_count": len(sections_added),
            "message": f"تم إنشاء كراسة الشروط والمواصفات الكاملة '{title}' بنجاح مع {len(sections_added)} قسم"
        }

    else:
        # Fallback to simple document if template not available
        title_paragraph = doc.add_heading(title, level=0)
        title_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_rtl_paragraph(title_paragraph)
        for run in title_paragraph.runs:
            set_arabic_font(run, font_size=20)

        info_paragraph = doc.add_paragraph()
        set_rtl_paragraph(info_paragraph)
        run = info_paragraph.add_run(f"اسم المشروع: {project_name}")
        run.bold = True
        set_arabic_font(run)

        if entity_name:
            entity_para = doc.add_paragraph(f"الجهة: {entity_name}")
            set_rtl_paragraph(entity_para)
            for run in entity_para.runs:
                set_arabic_font(run)

        if tender_no:
            tender_para = doc.add_paragraph(f"رقم الكراسة: {tender_no}")
            set_rtl_paragraph(tender_para)
            for run in tender_para.runs:
                set_arabic_font(run)

        date_para = doc.add_paragraph(f"التاريخ: {date or datetime.now().strftime('%Y/%m/%d')}")
        set_rtl_paragraph(date_para)
        for run in date_para.runs:
            set_arabic_font(run)

        doc.add_page_break()

        active_documents[doc_id] = doc
        document_metadata[doc_id] = {
            "doc_id": doc_id,
            "title": title,
            "project_name": project_name,
            "entity_name": entity_name,
            "tender_no": tender_no,
            "created_at": datetime.now().isoformat(),
            "language": "ar",
            "rtl": True,
            "sections": []
        }

        return {
            "success": True,
            "doc_id": doc_id,
            "title": title,
            "language": "ar",
            "message": f"تم إنشاء كراسة الشروط '{title}' بنجاح"
        }


@mcp.tool()
def add_section(
    doc_id: str,
    heading: str,
    content: str,
    level: int = 1
) -> dict:
    """
    Add a section with heading and content to the document.

    Args:
        doc_id: Document ID from create_rfp_document
        heading: Section heading text
        content: Section content (supports paragraphs separated by newlines)
        level: Heading level (1-4, default 1)

    Returns:
        dict with success status
    """
    if doc_id not in active_documents:
        return {"success": False, "error": f"Document {doc_id} not found"}

    doc = active_documents[doc_id]
    metadata = document_metadata.get(doc_id, {})
    is_rtl = metadata.get("rtl", False)

    # Add heading
    heading_para = doc.add_heading(heading, level=level)
    if is_rtl:
        set_rtl_paragraph(heading_para)
        for run in heading_para.runs:
            set_arabic_font(run, font_size=18 if level == 1 else 16)

    # Add content paragraphs
    paragraphs = content.strip().split('\n\n')
    for para_text in paragraphs:
        if para_text.strip():
            # Check if it's a bullet point
            if para_text.strip().startswith('-') or para_text.strip().startswith('•'):
                # Remove bullet marker and add as list item
                text = para_text.strip().lstrip('-•').strip()
                para = doc.add_paragraph(text, style='List Bullet')
            elif para_text.strip()[0].isdigit() and '.' in para_text.strip()[:3]:
                # Numbered list
                text = para_text.strip().split('.', 1)[1].strip()
                para = doc.add_paragraph(text, style='List Number')
            else:
                para = doc.add_paragraph(para_text.strip())

            # Apply RTL formatting if needed
            if is_rtl:
                set_rtl_paragraph(para)
                for run in para.runs:
                    set_arabic_font(run)

    # Update metadata
    if doc_id in document_metadata:
        document_metadata[doc_id]["sections"].append({
            "heading": heading,
            "level": level,
            "content_length": len(content)
        })

    return {
        "success": True,
        "doc_id": doc_id,
        "section_added": heading,
        "message": f"Section '{heading}' added successfully"
    }


@mcp.tool()
def add_table(
    doc_id: str,
    rows: int,
    cols: int,
    data: Optional[List[List[str]]] = None,
    header_row: bool = True
) -> dict:
    """
    Add a table to the document.

    Args:
        doc_id: Document ID
        rows: Number of rows
        cols: Number of columns
        data: Optional 2D list of cell data
        header_row: Whether first row is a header

    Returns:
        dict with success status
    """
    if doc_id not in active_documents:
        return {"success": False, "error": f"Document {doc_id} not found"}

    doc = active_documents[doc_id]
    metadata = document_metadata.get(doc_id, {})
    is_rtl = metadata.get("rtl", False)

    table = doc.add_table(rows=rows, cols=cols)
    table.style = 'Light Grid Accent 1'

    # Fill in data if provided
    if data:
        for i, row_data in enumerate(data[:rows]):
            for j, cell_data in enumerate(row_data[:cols]):
                cell = table.rows[i].cells[j]
                cell.text = str(cell_data)

                # Apply RTL and Arabic font to table cells
                if is_rtl:
                    for paragraph in cell.paragraphs:
                        set_rtl_paragraph(paragraph)
                        for run in paragraph.runs:
                            set_arabic_font(run, font_size=14)

                # Bold header row
                if header_row and i == 0:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.font.bold = True

    return {
        "success": True,
        "doc_id": doc_id,
        "message": f"Table ({rows}x{cols}) added successfully"
    }


@mcp.tool()
def save_document(doc_id: str) -> dict:
    """
    Save the document to disk and return file information.

    Args:
        doc_id: Document ID to save

    Returns:
        dict with file_path, file_name, and download information
    """
    if doc_id not in active_documents:
        return {"success": False, "error": f"Document {doc_id} not found"}

    doc = active_documents[doc_id]
    metadata = document_metadata.get(doc_id, {})

    # Generate filename
    title = metadata.get("title", "rfp_document")
    safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
    safe_title = safe_title.replace(' ', '_')
    file_name = f"{safe_title}_{doc_id[:8]}.docx"
    file_path = DOCUMENTS_DIR / file_name

    # Save document
    doc.save(str(file_path))

    # Update metadata
    metadata["file_path"] = str(file_path)
    metadata["file_name"] = file_name
    metadata["saved_at"] = datetime.now().isoformat()

    return {
        "success": True,
        "doc_id": doc_id,
        "file_name": file_name,
        "file_path": str(file_path),
        "message": f"Document saved as {file_name}"
    }


@mcp.tool()
def get_document_preview(doc_id: str) -> dict:
    """
    Get a preview of the document structure and content.

    Args:
        doc_id: Document ID

    Returns:
        dict with document preview information
    """
    if doc_id not in active_documents:
        return {"success": False, "error": f"Document {doc_id} not found"}

    doc = active_documents[doc_id]
    metadata = document_metadata.get(doc_id, {})

    # Extract structure
    preview = {
        "success": True,
        "doc_id": doc_id,
        "title": metadata.get("title", "Untitled"),
        "project_name": metadata.get("project_name", ""),
        "created_at": metadata.get("created_at", ""),
        "sections": metadata.get("sections", []),
        "section_count": len(metadata.get("sections", [])),
        "paragraph_count": len(doc.paragraphs),
        "table_count": len(doc.tables)
    }

    # Generate preview text
    preview_lines = [f"# {metadata.get('title', 'RFP Document')}"]
    preview_lines.append(f"\nProject: {metadata.get('project_name', 'N/A')}")
    preview_lines.append(f"Sections: {len(metadata.get('sections', []))}")
    preview_lines.append("\n## Document Structure:\n")

    for i, section in enumerate(metadata.get("sections", []), 1):
        indent = "  " * (section.get("level", 1) - 1)
        preview_lines.append(f"{indent}{i}. {section['heading']}")

    preview["preview_text"] = "\n".join(preview_lines)

    return preview


@mcp.tool()
def list_documents() -> dict:
    """
    List all active documents in memory.

    Returns:
        dict with list of active documents
    """
    documents = []
    for doc_id, metadata in document_metadata.items():
        documents.append({
            "doc_id": doc_id,
            "title": metadata.get("title", "Untitled"),
            "project_name": metadata.get("project_name", ""),
            "created_at": metadata.get("created_at", ""),
            "sections": len(metadata.get("sections", []))
        })

    return {
        "success": True,
        "count": len(documents),
        "documents": documents
    }


@mcp.tool()
def delete_document(doc_id: str) -> dict:
    """
    Delete a document from memory and disk.

    Args:
        doc_id: Document ID to delete

    Returns:
        dict with success status
    """
    if doc_id not in active_documents:
        return {"success": False, "error": f"Document {doc_id} not found"}

    # Remove from memory
    del active_documents[doc_id]

    metadata = document_metadata.pop(doc_id, {})

    # Delete file if exists
    file_path = metadata.get("file_path")
    if file_path and Path(file_path).exists():
        Path(file_path).unlink()

    return {
        "success": True,
        "doc_id": doc_id,
        "message": "Document deleted successfully"
    }


if __name__ == "__main__":
    # Run the FastMCP server with HTTP transport
    import uvicorn

    host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_SERVER_PORT", "8080"))

    print(f"Starting MCP-Doc Server on {host}:{port}")
    print(f"Documents will be saved to: {DOCUMENTS_DIR}")

    # Start FastMCP server
    mcp.run(transport="http", host=host, port=port)
