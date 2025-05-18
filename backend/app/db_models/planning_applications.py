import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db_models.base import Base
from app.models.shared import ApplicationType, ApplicationStatus

class PlanningApplication(Base):
    __tablename__ = "planning_applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference_number = Column(String, nullable=False)
    address = Column(String, nullable=False)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id"), nullable=True)
    site_description = Column(Text, nullable=True)
    proposal_details = Column(Text, nullable=False)
    application_type = Column(Enum(ApplicationType), nullable=False)
    status = Column(Enum(ApplicationStatus), nullable=False)
    received_date = Column(DateTime, nullable=False)
    validated_date = Column(DateTime, nullable=True)
    decision_date = Column(DateTime, nullable=True)
    decision = Column(String, nullable=True)
    applicant_name = Column(String, nullable=True)
    agent_name = Column(String, nullable=True)
    case_officer = Column(String, nullable=True)

    # optionally store DM-specific arrays as JSON
    constraints = Column(JSON, nullable=True)
    relevant_policies = Column(JSON, nullable=True)
    reasoning_steps = Column(JSON, nullable=True)
    trade_off_analysis = Column(JSON, nullable=True)

    # relationships
    officer_report = relationship("OfficerReport", back_populates="application")
    precedents = relationship("PrecedentCase", back_populates="application")
