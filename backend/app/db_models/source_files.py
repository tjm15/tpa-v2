import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db_models.base import Base

class SourceFile(Base):
    __tablename__ = "source_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    extension = Column(String, nullable=True)
    uploaded_at = Column(TIMESTAMP, default=datetime.utcnow)
    storage_path = Column(String, nullable=False)
    source_url = Column(String, nullable=True)
    sha256_hash = Column(String, nullable=True)
    lpa_code = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    # relationships
    text_chunks = relationship("ExtractedTextChunk", back_populates="source_file")
