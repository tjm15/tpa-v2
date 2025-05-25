import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db_models.base import Base

class PlanDocument(Base):
    __tablename__ = "plan_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    name = Column(String, nullable=False)
    version = Column(String, nullable=True)
    document_status = Column(String, nullable=True)
    lpa_code = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # relationship to nodes
    root_nodes = relationship("DocumentNode", back_populates="document")

class DocumentNode(Base):
    __tablename__ = "document_nodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("plan_documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    parent_id = Column(UUID(as_uuid=True), ForeignKey("document_nodes.id"), nullable=True)
    title = Column(String, nullable=False)
    reference = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    order_no = Column(Integer, nullable=True)  # renamed from 'order'
    last_modified = Column(TIMESTAMP, nullable=True)
    author = Column(String, nullable=True)

    document = relationship("PlanDocument", back_populates="root_nodes")
    children = relationship("DocumentNode", backref="parent", remote_side=[id])
