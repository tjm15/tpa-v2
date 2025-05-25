import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.db_models.base import Base

class PrecedentKeyPolicy(Base):
    __tablename__ = "precedent_key_policies"

    precedent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("precedent_cases.id", ondelete="CASCADE"),
        primary_key=True,
    )
    policy_code = Column(String, primary_key=True)
    policy_id = Column(UUID(as_uuid=True), nullable=True)
