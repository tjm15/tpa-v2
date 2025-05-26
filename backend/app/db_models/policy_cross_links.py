import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.db_models.base import Base

class PolicyCrossLink(Base):
    __tablename__ = "policy_cross_links"

    source_policy_code = Column(String, primary_key=True)  # original code
    target_policy_code = Column(String, primary_key=True)
    source_policy_id = Column(
        UUID(as_uuid=True),
        ForeignKey("policies.id", ondelete="CASCADE"),
        nullable=True,
    )
    target_policy_id = Column(
        UUID(as_uuid=True),
        ForeignKey("policies.id", ondelete="CASCADE"),
        nullable=True,
    )
