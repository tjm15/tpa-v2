import uuid
from datetime import datetime

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from libs.shared_db_models.base import Base

class Policy(Base):
    __tablename__ = "policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_id = Column(String, nullable=True)  # Now nullable
    policy_title = Column(String, nullable=False)
    tags = Column(ARRAY(String), nullable=True)  # e.g. ["strategic","SPD"]
    summary = Column(Text, nullable=False)
    cross_references = Column(ARRAY(String), nullable=True)  # codes of other policies
    geographic_mentions = Column(ARRAY(String), nullable=True)
    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("plan_documents.id", ondelete="SET NULL"),
        nullable=True,
    )
    lpa_code = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
