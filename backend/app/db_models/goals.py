import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, NUMERIC, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.db_models.base import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category = Column(ARRAY(String), nullable=True)  # Changed to ARRAY
    description = Column(Text, nullable=True)
    target_metric = Column(String, nullable=True)  # Made nullable
    target_value = Column(NUMERIC, nullable=True)
    current_value = Column(NUMERIC, nullable=True)
    unit = Column(String, nullable=True)
    source = Column(String, nullable=True)
    status = Column(ARRAY(String), nullable=True)  # Changed to ARRAY
    type = Column(ARRAY(String), nullable=True)  # Changed to ARRAY and renamed from 'type'
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
