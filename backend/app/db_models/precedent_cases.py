import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Date, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from app.db_models.base import Base

class PrecedentCase(Base):
    __tablename__ = "precedent_cases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey("planning_applications.id", ondelete="SET NULL"),
        nullable=True,
    )
    case_reference = Column(String, nullable=False)
    address = Column(String, nullable=True)
    decision_date = Column(Date, nullable=True)
    outcome = Column(ARRAY(String), nullable=True)  # Changed to ARRAY
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    application = relationship("PlanningApplication", back_populates="precedents")
