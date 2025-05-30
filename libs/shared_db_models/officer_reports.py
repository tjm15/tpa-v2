import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
from libs.shared_db_models.base import Base

class OfficerReport(Base):
    __tablename__ = "officer_reports"

    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey("planning_applications.id", ondelete="CASCADE"),
        primary_key=True,
    )
    ai_context_id = Column(
        UUID(as_uuid=True),
        ForeignKey("application_ai_context.application_id"),
        nullable=True,
    )
    version = Column(String, nullable=False)
    status = Column(ARRAY(String), nullable=True)  # dynamic tags
    recommendation = Column(Text, nullable=True)
    provenance = Column(JSONB, nullable=True)  # e.g. { retrieval_log_id, write_log_id }
    created_by = Column(String, nullable=True)
    last_edited_by = Column(String, nullable=True)
    last_modified = Column(TIMESTAMP, default=datetime.utcnow)

    application = relationship("PlanningApplication", back_populates="officer_report")
