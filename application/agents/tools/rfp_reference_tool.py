"""
RFP Document Reference Tool
Tool for searching and retrieving RFP-related documents and best practices
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json

from application.agents.tools.base import Tool

logger = logging.getLogger(__name__)


@dataclass
class RFPReferenceResult:
    """Result from RFP reference search"""
    document_name: str
    section: str
    content: str
    relevance_score: float
    metadata: Dict[str, Any]


class RFPReferenceTool(Tool):
    """
    Tool for searching RFP knowledge base and retrieving relevant references
    Helps the RFP Agent find similar RFPs, best practices, and compliance requirements
    """

    def __init__(self, config=None):
        self.config = config or {}
        self.name = "rfp_reference_tool"
        self.description = "Search for RFP examples, best practices, and compliance requirements"

        # Knowledge base of RFP best practices (can be extended with database)
        self.knowledge_base = self._initialize_knowledge_base()

    def _initialize_knowledge_base(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Initialize the RFP knowledge base
        In production, this would connect to a database or vector store
        """
        return {
            "best_practices": [
                {
                    "category": "project_scope",
                    "title": "كتابة نطاق العمل الفعال",
                    "content": """عند كتابة نطاق العمل:
                    1. كن محدداً وواضحاً في الأهداف
                    2. تجنب الغموض والعبارات العامة
                    3. حدد المخرجات بشكل قابل للقياس
                    4. اذكر المعايير والمواصفات المطلوبة
                    5. تجنب ذكر علامات تجارية محددة""",
                    "tags": ["scope", "clarity", "requirements"]
                },
                {
                    "category": "evaluation",
                    "title": "معايير التقييم الموضوعية",
                    "content": """معايير التقييم يجب أن تكون:
                    - قابلة للقياس الكمي
                    - عادلة وشفافة
                    - مرتبطة بأهداف المشروع
                    - موزونة حسب الأهمية
                    - معلنة مسبقاً للمتنافسين""",
                    "tags": ["evaluation", "criteria", "transparency"]
                },
                {
                    "category": "timeline",
                    "title": "وضع جدول زمني واقعي",
                    "content": """الجدول الزمني الفعال:
                    - يراعي تعقيد المشروع
                    - يتضمن فترات مراجعة واعتماد
                    - يحدد مراحل واضحة
                    - يتضمن هامش للطوارئ
                    - قابل للمتابعة والقياس""",
                    "tags": ["timeline", "phases", "planning"]
                }
            ],
            "compliance_requirements": [
                {
                    "regulation": "نظام المنافسات والمشتريات الحكومية",
                    "article": "المادة 23",
                    "content": """يجب أن تتضمن وثائق المنافسة:
                    - وصف دقيق للأعمال المطلوبة
                    - الشروط والمواصفات التفصيلية
                    - معايير التقييم والترسية
                    - نماذج العقود والضمانات""",
                    "tags": ["legal", "requirements", "documentation"]
                },
                {
                    "regulation": "متطلبات المحتوى المحلي",
                    "article": "السياسة العامة",
                    "content": """يجب تحديد:
                    - النسبة المطلوبة للمحتوى المحلي
                    - آلية احتساب المحتوى المحلي
                    - الوثائق المطلوبة للإثبات
                    - الحوافز والأفضليات""",
                    "tags": ["local_content", "compliance", "requirements"]
                },
                {
                    "regulation": "معايير الأمن السيبراني",
                    "article": "الضوابط الأساسية",
                    "content": """للمشاريع التقنية يجب:
                    - تطبيق معايير الأمن السيبراني الوطنية
                    - حماية البيانات والخصوصية
                    - خطة استمرارية الأعمال
                    - إجراءات الاستجابة للحوادث""",
                    "tags": ["cybersecurity", "it", "compliance"]
                }
            ],
            "templates": [
                {
                    "type": "it_project",
                    "name": "نموذج RFP مشروع تقني",
                    "sections": [
                        "نطاق العمل التقني",
                        "المتطلبات الوظيفية",
                        "المتطلبات غير الوظيفية",
                        "معايير الأداء",
                        "الأمن والخصوصية"
                    ],
                    "tags": ["it", "software", "technology"]
                },
                {
                    "type": "construction",
                    "name": "نموذج RFP مشروع إنشائي",
                    "sections": [
                        "الأعمال المدنية",
                        "المواصفات الفنية",
                        "معايير السلامة",
                        "جدول الكميات",
                        "الرسومات والمخططات"
                    ],
                    "tags": ["construction", "building", "infrastructure"]
                },
                {
                    "type": "consulting",
                    "name": "نموذج RFP خدمات استشارية",
                    "sections": [
                        "نطاق الخدمات الاستشارية",
                        "المنهجية والأسلوب",
                        "فريق العمل والخبرات",
                        "المخرجات والتقارير",
                        "نقل المعرفة"
                    ],
                    "tags": ["consulting", "advisory", "services"]
                }
            ],
            "similar_rfps": [
                {
                    "title": "مشروع تطوير نظام إدارة الموارد البشرية",
                    "entity": "وزارة الموارد البشرية",
                    "project_type": "it",
                    "duration": "8 أشهر",
                    "key_features": [
                        "نظام متكامل للموارد البشرية",
                        "بوابة الخدمة الذاتية",
                        "التكامل مع الأنظمة الحكومية",
                        "التقارير والإحصائيات"
                    ],
                    "tags": ["hr", "erp", "government"]
                },
                {
                    "title": "مشروع بناء مركز البيانات",
                    "entity": "الهيئة السعودية للبيانات",
                    "project_type": "construction",
                    "duration": "18 شهر",
                    "key_features": [
                        "مركز بيانات Tier 3",
                        "أنظمة التبريد المتقدمة",
                        "أنظمة الطاقة الاحتياطية",
                        "معايير الأمان العالية"
                    ],
                    "tags": ["datacenter", "infrastructure", "technology"]
                }
            ]
        }

    def execute_action(self, action_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute the RFP reference tool action
        """
        if action_name != "search":
            return {
                "success": False,
                "error": f"Unknown action: {action_name}"
            }

        query = kwargs.get("query", "")
        search_type = kwargs.get("search_type", "similar_rfp")
        project_type = kwargs.get("project_type", "all")
        limit = kwargs.get("limit", 5)

        logger.info(f"Searching RFP references: query='{query}', type={search_type}")

        try:
            results = []

            if search_type == "best_practices":
                results = self._search_best_practices(query, project_type, limit)
            elif search_type == "compliance":
                results = self._search_compliance(query, project_type, limit)
            elif search_type == "templates":
                results = self._search_templates(query, project_type, limit)
            else:  # similar_rfp
                results = self._search_similar_rfps(query, project_type, limit)

            return {
                "success": True,
                "results": results,
                "count": len(results),
                "query": query,
                "search_type": search_type
            }

        except Exception as e:
            logger.error(f"Error in RFP reference search: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": []
            }

    def _search_best_practices(self, query: str, project_type: str, limit: int) -> List[Dict]:
        """Search best practices knowledge base"""
        results = []
        query_lower = query.lower()

        for practice in self.knowledge_base["best_practices"]:
            # Simple relevance scoring (can be enhanced with vector search)
            score = self._calculate_relevance(query_lower, practice)

            if score > 0:
                results.append({
                    "type": "best_practice",
                    "title": practice["title"],
                    "content": practice["content"],
                    "category": practice["category"],
                    "relevance_score": score
                })

        # Sort by relevance and limit
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:limit]

    def _search_compliance(self, query: str, project_type: str, limit: int) -> List[Dict]:
        """Search compliance requirements"""
        results = []
        query_lower = query.lower()

        for requirement in self.knowledge_base["compliance_requirements"]:
            score = self._calculate_relevance(query_lower, requirement)

            if score > 0:
                results.append({
                    "type": "compliance",
                    "regulation": requirement["regulation"],
                    "article": requirement["article"],
                    "content": requirement["content"],
                    "relevance_score": score
                })

        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:limit]

    def _search_templates(self, query: str, project_type: str, limit: int) -> List[Dict]:
        """Search RFP templates"""
        results = []

        for template in self.knowledge_base["templates"]:
            # Filter by project type if specified
            if project_type != "all" and project_type not in template.get("tags", []):
                continue

            results.append({
                "type": "template",
                "name": template["name"],
                "template_type": template["type"],
                "sections": template["sections"],
                "tags": template.get("tags", [])
            })

        return results[:limit]

    def _search_similar_rfps(self, query: str, project_type: str, limit: int) -> List[Dict]:
        """Search for similar RFP examples"""
        results = []
        query_lower = query.lower()

        for rfp in self.knowledge_base["similar_rfps"]:
            # Filter by project type
            if project_type != "all" and rfp["project_type"] != project_type:
                continue

            score = self._calculate_relevance(query_lower, rfp)

            if score > 0:
                results.append({
                    "type": "similar_rfp",
                    "title": rfp["title"],
                    "entity": rfp["entity"],
                    "project_type": rfp["project_type"],
                    "duration": rfp["duration"],
                    "key_features": rfp["key_features"],
                    "relevance_score": score
                })

        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:limit]

    def _calculate_relevance(self, query: str, document: Dict) -> float:
        """
        Calculate relevance score between query and document
        Simple keyword matching - can be enhanced with embeddings
        """
        score = 0.0
        query_words = query.split()

        # Check all text fields in document
        text_content = ""
        for key, value in document.items():
            if isinstance(value, str):
                text_content += " " + value.lower()
            elif isinstance(value, list):
                text_content += " " + " ".join(str(v).lower() for v in value)

        # Count matching words
        for word in query_words:
            if word in text_content:
                score += 1.0

        # Boost score if query matches tags
        if "tags" in document:
            for tag in document["tags"]:
                if tag.lower() in query:
                    score += 2.0

        # Normalize score
        return score / (len(query_words) + 1)

    def get_actions_metadata(self):
        """
        Returns a list of JSON objects describing the actions supported by the tool.
        """
        return [
            {
                "name": "search",
                "description": "Search RFP knowledge base for examples, best practices, and compliance requirements",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for RFP references"
                        },
                        "search_type": {
                            "type": "string",
                            "description": "Type of search: 'similar_rfp', 'best_practices', 'compliance', 'templates'",
                            "default": "similar_rfp"
                        },
                        "project_type": {
                            "type": "string",
                            "description": "Project type to filter results: 'it', 'construction', 'consulting', 'all'",
                            "default": "all"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        ]

    def get_config_requirements(self):
        """
        Returns a dictionary describing the configuration requirements for the tool.
        """
        return {
            "knowledge_base_path": {
                "type": "string",
                "description": "Path to the RFP knowledge base (optional)",
                "required": False
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of search results to return",
                "default": 10,
                "required": False
            }
        }


# Tool factory function
def create_rfp_reference_tool() -> RFPReferenceTool:
    """Factory function to create RFP reference tool"""
    return RFPReferenceTool(
        name="rfp_reference_tool",
        description="Search RFP knowledge base for examples, best practices, and compliance requirements"
    )