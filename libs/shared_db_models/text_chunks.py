import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from libs.shared_db_models.base import Base

class ExtractedTextChunk(Base):
    __tablename__ = "extracted_text_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id = Column(
        UUID(as_uuid=True),
        ForeignKey("source_files.id", ondelete="CASCADE"),
        nullable=False,
    )
    page_number = Column(Integer, nullable=True)
    chunk_order = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # relationships
    source_file = relationship("SourceFile", back_populates="text_chunks")
    policy_vectors = relationship("PolicyVector", back_populates="source_chunk")
    application_vectors = relationship("ApplicationVector", back_populates="source_chunk")
