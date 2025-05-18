import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db_models.base import Base

class Constraint(Base):
    __tablename__ = "constraints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    severity = Column(String, nullable=True)
    source_document = Column(String, nullable=True)
    geometry = Column(JSONB, nullable=True)
    description = Column(Text, nullable=True)
