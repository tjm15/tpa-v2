# knowledge_base/policy_manager.py
from typing import List, Dict, Optional, Any
from uuid import UUID

from sqlalchemy import or_
from ..db_manager import DatabaseManager
from libs.shared_db_models.policies import Policy
from libs.shared_db_models.plan_documents import PlanDocument
from libs.shared_db_models.text_chunks import ExtractedTextChunk
from libs.shared_db_models.vectors import PolicyVector
from sqlalchemy.orm import Session


class PolicyManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        print(f"INFO: PolicyManager initialized (uses database for policy storage).")

    def search_policies(self, themes: Optional[List[str]]=None, keywords: Optional[List[str]]=None, 
                        semantic_query: Optional[str]=None, policy_ids: Optional[List[str]]=None, 
                        document_sources: Optional[List[str]]=None, limit: int=5) -> List[Dict[str, Any]]:
        session: Session = self.db_manager.session
        query = session.query(ExtractedTextChunk)

        if keywords:
            keyword_filters = [ExtractedTextChunk.chunk_text.ilike(f"%{kw}%") for kw in keywords]
            query = query.filter(or_(*keyword_filters))
        
        if policy_ids:
            query = query.filter(ExtractedTextChunk.section.in_(policy_ids))

        # Semantic search placeholder
        results = query.limit(limit).all()
        return [
            {
                'policy_clause_id': str(chunk.id),
                'policy_id_tag': chunk.section,
                'text_snippet': chunk.chunk_text,
            }
            for chunk in results
        ]

    def get_policy_details_by_id_tag(self, policy_id_tag: str) -> Optional[Dict[str, Any]]:
        session: Session = self.db_manager.session
        chunk = session.query(ExtractedTextChunk).filter(ExtractedTextChunk.section == policy_id_tag).first()
        if chunk:
            return {
                'policy_clause_id': str(chunk.id),
                'policy_id_tag': chunk.section,
                'text_snippet': chunk.chunk_text,
            }
        return None

    def get_policy_full_text_by_id_tag(self, policy_id_tag: str) -> Optional[str]:
        session: Session = self.db_manager.session
        chunk = session.query(ExtractedTextChunk).filter(ExtractedTextChunk.section == policy_id_tag).first()
        return str(chunk.chunk_text) if chunk else None
