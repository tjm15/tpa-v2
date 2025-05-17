# app/models/document_models.py
from typing import Optional, List, ForwardRef
from pydantic import BaseModel, Field, UUID4
import uuid
from datetime import datetime
from .common_models import (
    DocumentNodeTypeEnum, PlanDocumentTypeEnum, PlanDocumentStatusEnum, BaseUUIDModel
)

# ForwardRef for recursive DocumentNode
DocumentNodeRef = ForwardRef('DocumentNode')

class LinkedEntity(BaseModel):
    type: str
    id: str # Could be UUID if always linking to UUID entities
    name: str

class DocumentNodeBase(BaseModel):
    title: str
    type: DocumentNodeTypeEnum
    reference: Optional[str] = None
    content: Optional[str] = None # Markdown or rich text
    children: Optional[List[DocumentNodeRef]] = Field(default_factory=list)
    unresolvedIssues: Optional[List[str]] = Field(default_factory=list)
    linkedEntities: Optional[List[LinkedEntity]] = Field(default_factory=list)
    author: Optional[str] = None

class DocumentNodeCreate(DocumentNodeBase):
    # Children would typically be managed via separate calls or specific logic
    # when creating/updating a node, not usually part of the direct create payload
    # unless creating a whole subtree.
    children: Optional[List['DocumentNodeCreate']] = Field(default_factory=list) # Allow creating with children

class DocumentNodeUpdate(DocumentNodeBase):
    title: Optional[str] = None
    type: Optional[DocumentNodeTypeEnum] = None
    # All fields are optional for PATCH
    children: Optional[List['DocumentNodeUpdate']] = Field(default_factory=list) # Allow updating with children

class DocumentNode(DocumentNodeBase, BaseUUIDModel):
    lastModified: datetime = Field(default_factory=datetime.utcnow)
    children: List['DocumentNode'] = Field(default_factory=list) # Override for response model

    class Config:
        from_attributes = True

# Update forward references for DocumentNode
DocumentNode.model_rebuild()
DocumentNodeCreate.model_rebuild()
DocumentNodeUpdate.model_rebuild()


class PlanDocumentBase(BaseModel):
    name: str
    type: PlanDocumentTypeEnum
    rootNode: DocumentNode # For GET, this would be the full node. For create, might be simpler.
    version: Optional[str] = None
    documentStatus: Optional[PlanDocumentStatusEnum] = None

class PlanDocumentCreate(PlanDocumentBase):
    # rootNode might be simplified for creation, e.g., just a title and type,
    # with content added via node endpoints. Or allow creating a basic root.
    rootNode: DocumentNodeCreate

class PlanDocumentUpdate(PlanDocumentBase):
    name: Optional[str] = None
    type: Optional[PlanDocumentTypeEnum] = None
    rootNode: Optional[DocumentNodeUpdate] = None # Allow updating root node
    # All fields are optional for PATCH

class PlanDocument(PlanDocumentBase, BaseUUIDModel):
    pass

    class Config:
        from_attributes = True
