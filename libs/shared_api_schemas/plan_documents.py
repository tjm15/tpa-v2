from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class DocumentNode(BaseModel):
    id: str
    documentId: str
    parentId: Optional[str] = None
    title: str
    reference: Optional[str] = None
    content: Optional[str] = None
    orderNo: Optional[int] = None
    lastModified: Optional[datetime] = None
    author: Optional[str] = None

class PlanDocument(BaseModel):
    id: str
    filename: str
    name: str
    version: Optional[str] = None
    documentStatus: Optional[str] = None
    lpaCode: Optional[str] = None
    createdAt: datetime
