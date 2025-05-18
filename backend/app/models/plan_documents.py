from typing import List, Optional
from pydantic import BaseModel
from app.models.shared import DocumentNodeTypeEnum as DocumentNodeType

class LinkedEntity(BaseModel):
    type: str
    id: str
    name: str

class DocumentNode(BaseModel):
    id: str
    title: str
    type: DocumentNodeType
    reference: Optional[str] = None
    content: Optional[str] = None
    children: Optional[List['DocumentNode']] = None
    unresolvedIssues: Optional[List[str]] = None
    linkedEntities: Optional[List[LinkedEntity]] = None
    lastModified: Optional[str] = None
    author: Optional[str] = None

DocumentNode.update_forward_refs()

class PlanDocument(BaseModel):
    id: str
    name: str
    type: str  # See your PlanDocumentType enum if you wish
    rootNode: DocumentNode
    version: Optional[str] = None
    documentStatus: Optional[str] = None
