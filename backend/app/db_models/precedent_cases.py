import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy.orm import relationship
from app.db_models.base import Base
from app.models.shared import PrecedentDecisionOutcome

class PrecedentCase(Base):
    __tablename__ = "precedent_cases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey("planning_applications.id", ondelete="CASCADE"),
        nullable=True,
    )
    case_reference = Column(String, nullable=False)
    address = Column(String, nullable=False)
    decision_type = Column(String, nullable=False)
    decision_date = Column(DateTime, nullable=False)
    outcome = Column(Enum(PrecedentDecisionOutcome), nullable=False)
    key_policies_cited = Column(JSON, nullable=False)  # list of strings
    inspector_reasoning_summary = Column(Text, nullable=True)
    decision_extract_link = Column(String, nullable=True)
    relevance_summary = Column(Text, nullable=True)
    similarity_criteria = Column(JSON, nullable=True)  # {site, policyOverlap}

    application = relationship("PlanningApplication", back_populates="precedents")
