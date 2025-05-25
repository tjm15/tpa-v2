import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db_models.base import Base

class ApplicationAIContext(Base):
    __tablename__ = "application_ai_context"

    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey("planning_applications.id", ondelete="CASCADE"),
        primary_key=True,
    )
    retrieval_log_id = Column(
        UUID(as_uuid=True),
        ForeignKey("retrieval_logs.log_id"),
        nullable=True,
    )
    reasoning_steps = Column(JSONB, nullable=True)  # structured trace with step & metadata
    competing_goals = Column(JSONB, nullable=True)
    narrative = Column(Text, nullable=True)
    model_version = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class ApplicationMaterialRef(Base):
    __tablename__ = "application_material_refs"

    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey("planning_applications.id", ondelete="CASCADE"),
        primary_key=True,
    )
    material_type = Column(String, primary_key=True)  # 'policy','constraint','precedent'
    material_code = Column(String, primary_key=True)  # e.g. "H1", free-text if unresolved
    material_id = Column(UUID(as_uuid=True), nullable=True)  # nullable FK when resolved
