"""
RFP Template System
Provides standard RFP structure and content generation
"""

from typing import Dict, List, Optional


class RFPTemplate:
    """Standard RFP template with customizable sections"""

    DEFAULT_SECTIONS = [
        {
            "heading": "1. Executive Summary",
            "level": 1,
            "description": "Overview of the project and key requirements",
            "prompt_guidance": "Provide a high-level summary of the project objectives, scope, and expected outcomes."
        },
        {
            "heading": "2. Project Overview",
            "level": 1,
            "description": "Detailed project description and background",
            "prompt_guidance": "Describe the project background, business context, and strategic importance."
        },
        {
            "heading": "2.1 Project Objectives",
            "level": 2,
            "description": "Specific goals and objectives",
            "prompt_guidance": "List the specific, measurable objectives this project aims to achieve."
        },
        {
            "heading": "2.2 Project Scope",
            "level": 2,
            "description": "What is included and excluded",
            "prompt_guidance": "Define clearly what is within scope and what is explicitly out of scope."
        },
        {
            "heading": "3. Technical Requirements",
            "level": 1,
            "description": "Technical specifications and requirements",
            "prompt_guidance": "Detail the technical requirements, platforms, technologies, and standards to be used."
        },
        {
            "heading": "3.1 Functional Requirements",
            "level": 2,
            "description": "Required functionalities and features",
            "prompt_guidance": "List all required features and functionalities in detail."
        },
        {
            "heading": "3.2 Non-Functional Requirements",
            "level": 2,
            "description": "Performance, security, scalability requirements",
            "prompt_guidance": "Specify performance benchmarks, security standards, scalability needs, etc."
        },
        {
            "heading": "4. Deliverables",
            "level": 1,
            "description": "Expected deliverables and outputs",
            "prompt_guidance": "List all deliverables, documentation, and outputs expected from the vendor."
        },
        {
            "heading": "5. Timeline and Milestones",
            "level": 1,
            "description": "Project timeline and key milestones",
            "prompt_guidance": "Define the project timeline, key milestones, and delivery dates."
        },
        {
            "heading": "6. Budget and Payment Terms",
            "level": 1,
            "description": "Budget constraints and payment structure",
            "prompt_guidance": "Specify budget range, payment terms, and billing structure."
        },
        {
            "heading": "7. Vendor Qualifications",
            "level": 1,
            "description": "Required vendor qualifications and experience",
            "prompt_guidance": "Detail the qualifications, certifications, and experience required from vendors."
        },
        {
            "heading": "8. Evaluation Criteria",
            "level": 1,
            "description": "How proposals will be evaluated",
            "prompt_guidance": "Explain the criteria and weighting for evaluating proposals."
        },
        {
            "heading": "9. Submission Requirements",
            "level": 1,
            "description": "How and when to submit proposals",
            "prompt_guidance": "Specify submission deadline, format, required documents, and contact information."
        },
        {
            "heading": "10. Terms and Conditions",
            "level": 1,
            "description": "Legal terms and conditions",
            "prompt_guidance": "Include standard terms, confidentiality requirements, and legal provisions."
        }
    ]

    @staticmethod
    def get_default_sections() -> List[Dict]:
        """
        Get the default RFP section structure.

        Returns:
            List of section dictionaries
        """
        return RFPTemplate.DEFAULT_SECTIONS.copy()

    @staticmethod
    def generate_section_content(
        section_heading: str,
        project_context: Optional[Dict] = None
    ) -> str:
        """
        Generate placeholder/template content for a section based on its heading.

        Args:
            section_heading: The section heading
            project_context: Optional context about the project

        Returns:
            Template content for the section
        """
        project_context = project_context or {}

        # Map section headings to template content
        content_templates = {
            "Executive Summary": (
                f"This Request for Proposal (RFP) is issued by {project_context.get('company_name', '[Company Name]')} "
                f"for {project_context.get('project_name', '[Project Name]')}. "
                "This document outlines the requirements, expectations, and evaluation criteria for selecting a qualified vendor.\n\n"
                "Key highlights:\n"
                "- Project objective and scope\n"
                "- Expected deliverables and timeline\n"
                "- Budget considerations\n"
                "- Selection criteria"
            ),
            "Project Overview": (
                f"Project Name: {project_context.get('project_name', '[Project Name]')}\n\n"
                "Background:\n"
                "[Provide context about why this project is needed, the problems it will solve, and its strategic importance]\n\n"
                "Current Situation:\n"
                "[Describe the current state and challenges that necessitate this project]"
            ),
            "Project Objectives": (
                "The primary objectives of this project are:\n\n"
                "1. [Primary Objective 1]\n"
                "2. [Primary Objective 2]\n"
                "3. [Primary Objective 3]\n\n"
                "Success will be measured by: [Define success metrics]"
            ),
            "Project Scope": (
                "In Scope:\n"
                "- [Item 1]\n"
                "- [Item 2]\n"
                "- [Item 3]\n\n"
                "Out of Scope:\n"
                "- [Excluded item 1]\n"
                "- [Excluded item 2]"
            ),
            "Technical Requirements": (
                "The following technical requirements must be met:\n\n"
                "Platform/Technology:\n"
                "- [Specify required platforms, programming languages, frameworks]\n\n"
                "Integration Requirements:\n"
                "- [List systems that need to integrate]\n\n"
                "Compliance:\n"
                "- [Specify regulatory or compliance requirements]"
            ),
            "Functional Requirements": (
                "Required Features:\n"
                "1. [Feature 1]: [Detailed description]\n"
                "2. [Feature 2]: [Detailed description]\n"
                "3. [Feature 3]: [Detailed description]"
            ),
            "Non-Functional Requirements": (
                "Performance:\n"
                "- Response time: [Specify requirements]\n"
                "- Concurrent users: [Specify capacity]\n\n"
                "Security:\n"
                "- Authentication: [Specify methods]\n"
                "- Data encryption: [Specify requirements]\n\n"
                "Scalability:\n"
                "- [Describe scalability requirements]"
            ),
            "Deliverables": (
                "The vendor must provide the following deliverables:\n\n"
                "1. [Deliverable 1] - [Description and format]\n"
                "2. [Deliverable 2] - [Description and format]\n"
                "3. Documentation - Complete technical and user documentation\n"
                "4. Source code - With appropriate licensing\n"
                "5. Training materials - For end users and administrators"
            ),
            "Timeline and Milestones": (
                "Project Duration: [Specify duration]\n\n"
                "Key Milestones:\n"
                "- Kick-off Meeting: [Date]\n"
                "- Design Phase Completion: [Date]\n"
                "- Development Phase Completion: [Date]\n"
                "- Testing and QA: [Date]\n"
                "- Final Delivery: [Date]\n\n"
                "RFP Response Deadline: [Date]\n"
                "Vendor Selection: [Date]\n"
                "Project Start Date: [Date]"
            ),
            "Budget and Payment Terms": (
                f"Budget Range: {project_context.get('budget_range', '[Specify range]')}\n\n"
                "Payment Structure:\n"
                "- Initial payment: [Percentage] upon contract signing\n"
                "- Milestone payments: [Specify milestones and percentages]\n"
                "- Final payment: [Percentage] upon project completion and acceptance\n\n"
                "Invoicing:\n"
                "- [Specify invoicing requirements and payment terms]"
            ),
            "Vendor Qualifications": (
                "Required Qualifications:\n"
                "- Minimum [X] years of experience in [relevant field]\n"
                "- Proven track record with similar projects\n"
                "- Relevant certifications: [List required certifications]\n"
                "- Team size and composition: [Specify requirements]\n"
                "- References: Minimum [X] client references\n\n"
                "Preferred Qualifications:\n"
                "- [Additional desired qualifications]"
            ),
            "Evaluation Criteria": (
                "Proposals will be evaluated based on the following criteria:\n\n"
                "1. Technical Approach and Methodology (30%)\n"
                "2. Experience and Qualifications (25%)\n"
                "3. Cost and Value (20%)\n"
                "4. Project Timeline (15%)\n"
                "5. References and Past Performance (10%)\n\n"
                "The selection will be based on the best value, not necessarily the lowest cost."
            ),
            "Submission Requirements": (
                "Proposal Submission:\n"
                f"Deadline: {project_context.get('submission_deadline', '[Specify date and time]')}\n\n"
                "Required Documents:\n"
                "1. Cover letter and executive summary\n"
                "2. Detailed technical proposal\n"
                "3. Project timeline and milestones\n"
                "4. Cost proposal with breakdown\n"
                "5. Company profile and team resumes\n"
                "6. Client references (minimum 3)\n"
                "7. Relevant certifications and licenses\n\n"
                "Submission Method: [Specify email or portal]\n"
                f"Contact Person: {project_context.get('contact_person', '[Name]')}\n"
                f"Contact Email: {project_context.get('contact_email', '[Email]')}"
            ),
            "Terms and Conditions": (
                "General Terms:\n"
                "- All information provided in this RFP is confidential\n"
                "- The issuing organization reserves the right to reject any or all proposals\n"
                "- Costs incurred in preparing proposals are the responsibility of the vendor\n"
                "- The selected vendor will be required to sign a formal contract\n\n"
                "Confidentiality:\n"
                "- All parties must maintain confidentiality of sensitive information\n"
                "- Non-disclosure agreements may be required\n\n"
                "Intellectual Property:\n"
                "- [Specify IP ownership and licensing terms]"
            )
        }

        # Extract the key part of the heading (remove numbering)
        heading_key = section_heading.split('. ', 1)[-1].strip()

        return content_templates.get(heading_key, "[Content to be provided]")

    @staticmethod
    def customize_sections(
        sections: Optional[List[str]] = None,
        project_type: Optional[str] = None
    ) -> List[Dict]:
        """
        Customize sections based on project type or specific requirements.

        Args:
            sections: Optional list of section names to include
            project_type: Optional project type for specialized templates

        Returns:
            Customized list of sections
        """
        all_sections = RFPTemplate.get_default_sections()

        if sections:
            # Filter to include only requested sections
            filtered = []
            for section in all_sections:
                heading_key = section["heading"].split('. ', 1)[-1].strip()
                if heading_key in sections or section["heading"] in sections:
                    filtered.append(section)
            return filtered

        # Project type specific customizations
        if project_type:
            project_type = project_type.lower()

            if "software" in project_type or "app" in project_type:
                # Add software-specific sections
                all_sections.insert(5, {
                    "heading": "3.3 Technology Stack",
                    "level": 2,
                    "description": "Required and preferred technologies",
                    "prompt_guidance": "Specify programming languages, frameworks, databases, and tools to be used."
                })

            elif "construction" in project_type or "infrastructure" in project_type:
                # Add construction-specific sections
                all_sections.insert(8, {
                    "heading": "5.1 Safety Requirements",
                    "level": 2,
                    "description": "Safety protocols and compliance",
                    "prompt_guidance": "Detail safety requirements and regulatory compliance needs."
                })

        return all_sections
