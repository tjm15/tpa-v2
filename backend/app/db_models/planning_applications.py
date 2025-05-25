import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Date, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
from app.db_models.base import Base

class PlanningApplication(Base):
    __tablename__ = "planning_applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference_number = Column(String, nullable=False)
    site_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("sites.id", ondelete="SET NULL"), 
        nullable=True
    )
    status = Column(ARRAY(String), nullable=True)  # dynamic tags, not rigid enum
    proposal_details = Column(Text, nullable=False)
    received_date = Column(Date, nullable=False)
    decision_date = Column(Date, nullable=True)
    applicant_name = Column(String, nullable=True)
    agent_name = Column(String, nullable=True)
    case_officer = Column(String, nullable=True)
    planner_weightings = Column(JSONB, nullable=True)  # UI-fed overrides
    lpa_code = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # relationships
    officer_report = relationship("OfficerReport", back_populates="application")
    precedents = relationship("PrecedentCase", back_populates="application")
