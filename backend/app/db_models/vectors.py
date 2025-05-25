import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from app.db_models.base import Base

class PolicyVector(Base):
    __tablename__ = "policy_vectors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_chunk_id = Column(
        UUID(as_uuid=True),
        ForeignKey("extracted_text_chunks.id", ondelete="CASCADE"),
        nullable=False,
    )
    embedding = Column(Text, nullable=True)  # Will be vector(768) when pgvector is available
    policy_ref = Column(String, nullable=True)  # e.g. "H1"
    key_themes = Column(ARRAY(String), nullable=True)
    cross_references = Column(ARRAY(String), nullable=True)
    geographic_mentions = Column(ARRAY(String), nullable=True)
    tokens = Column(Integer, nullable=True)
    model_version = Column(String, nullable=True)  # track embedding model
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # relationships
    source_chunk = relationship("ExtractedTextChunk", back_populates="policy_vectors")

class ApplicationVector(Base):
    __tablename__ = "application_vectors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_chunk_id = Column(
        UUID(as_uuid=True),
        ForeignKey("extracted_text_chunks.id", ondelete="CASCADE"),
        nullable=False,
    )
    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey("planning_applications.id", ondelete="SET NULL"),
        nullable=True,
    )
    embedding = Column(Text, nullable=True)  # Will be vector(768) when pgvector is available
    document_type = Column(String, nullable=True)
    section_title = Column(String, nullable=True)
    tokens = Column(Integer, nullable=True)
    model_version = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # relationships
    source_chunk = relationship("ExtractedTextChunk", back_populates="application_vectors")

class PrecedentVector(Base):
    __tablename__ = "precedent_vectors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_case_id = Column(
        UUID(as_uuid=True),
        ForeignKey("precedent_cases.id", ondelete="CASCADE"),
        nullable=True,
    )
    embedding = Column(Text, nullable=True)  # Will be vector(768) when pgvector is available
    summary = Column(Text, nullable=True)
    key_policies = Column(ARRAY(String), nullable=True)
    site_context = Column(String, nullable=True)
    model_version = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
