import uuid
from datetime import datetime

from sqlalchemy import Column, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON
from app.db_models.base import Base
from app.models.shared import PolicyStatus, PolicyType

class Policy(Base):
    __tablename__ = "policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference = Column(String, nullable=False)
    title = Column(String, nullable=False)
    wording = Column(Text, nullable=False)
    status = Column(Enum(PolicyStatus), nullable=False)
    type = Column(Enum(PolicyType), nullable=False)
    version = Column(String, nullable=True)
    last_modified = Column(DateTime, default=datetime.utcnow)
    author = Column(String, nullable=True)
    author_notes = Column(Text, nullable=True)
    supporting_text = Column(Text, nullable=True)
    internal_notes = Column(Text, nullable=True)
    affected_site_categories = Column(ARRAY(String), nullable=True)
    keywords = Column(ARRAY(String), nullable=True)
    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("plan_documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    requirements_summary = Column(String, nullable=True)
    linked_policies = Column(JSON, nullable=True)  # List of {policyId, policyReference, relationship, summary}
    strategic_goal_alignments = Column(JSON, nullable=True)  # List of {goalId, goalName, alignment, notes}
    ai_guidance = Column(JSON, nullable=True)  # List of {type, message, source}
