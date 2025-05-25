import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from app.db_models.base import Base

class RetrievalLog(Base):
    __tablename__ = "retrieval_logs"

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
    query = Column(Text, nullable=True)
    filters = Column(JSONB, nullable=True)
    matched_chunk_ids = Column(ARRAY(String), nullable=True)  # Store as string array for now
    retrieval_target = Column(String, nullable=True)  # e.g. 'policy_vectors'
    agent_context = Column(JSONB, nullable=True)

class WriteLog(Base):
    __tablename__ = "write_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
    output_type = Column(String, nullable=False)
    source_entity = Column(String, nullable=True)
    source_id = Column(UUID(as_uuid=True), nullable=True)
    input_snapshot = Column(JSONB, nullable=True)
    model_version = Column(String, nullable=True)
    output_text = Column(Text, nullable=True)
    author = Column(String, nullable=True, default='LLM')
    confidence = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)

class AIEnrichment(Base):
    __tablename__ = "ai_enrichment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_table = Column(String, nullable=False)
    target_id = Column(UUID(as_uuid=True), nullable=False)
    enrichment_type = Column(String, nullable=False)
    enriched_fields = Column(JSONB, nullable=False)
    model_version = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
