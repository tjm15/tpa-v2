import uuid
from sqlalchemy import Column, String, Text, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db_models.base import Base
from app.models.shared import DocumentNodeTypeEnum as DocumentNodeType

class PlanDocument(Base):
    __tablename__ = "plan_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    version = Column(String, nullable=True)
    document_status = Column(String, nullable=True)
    unresolved_issues = Column(JSON, nullable=True)
    linked_entities = Column(JSON, nullable=True)
    last_modified = Column(String, nullable=True)
    author = Column(String, nullable=True)

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
    type = Column(Enum(DocumentNodeType), nullable=False)
    reference = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    order = Column(String, nullable=True)
    unresolved_issues = Column(JSON, nullable=True)
    linked_entities = Column(JSON, nullable=True)
    last_modified = Column(String, nullable=True)
    author = Column(String, nullable=True)

    document = relationship("PlanDocument", back_populates="root_nodes")
    children = relationship("DocumentNode", backref="parent", remote_side=[id])
