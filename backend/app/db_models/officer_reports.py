import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db_models.base import Base

class OfficerReport(Base):
    __tablename__ = "officer_reports"

    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey("planning_applications.id", ondelete="CASCADE"),
        primary_key=True,
    )
    version = Column(String, nullable=False)
    sections = Column(JSON, nullable=False)   # list of section dicts
    recommendation = Column(Text, nullable=True)
    supporting_evidence = Column(JSON, nullable=True)  # list of {name, url_or_id}
    conflict_summary = Column(Text, nullable=True)
    compliance_flags = Column(JSON, nullable=True)     # list of {flag, met}
    last_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String, nullable=False)

    application = relationship("PlanningApplication", back_populates="officer_report")
