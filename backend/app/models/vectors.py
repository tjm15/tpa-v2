from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class PolicyVector(BaseModel):
    id: str
    sourceChunkId: str
    embedding: Optional[List[float]] = None  # pgvector: list of floats
    policyRef: Optional[str] = None
    keyThemes: Optional[List[str]] = None
    crossReferences: Optional[List[str]] = None
    geographicMentions: Optional[List[str]] = None
    tokens: Optional[int] = None
    modelVersion: Optional[str] = None
    createdAt: datetime

class ApplicationVector(BaseModel):
    id: str
    sourceChunkId: str
    applicationId: Optional[str] = None
    embedding: Optional[List[float]] = None  # pgvector: list of floats
    documentType: Optional[str] = None
    sectionTitle: Optional[str] = None
    tokens: Optional[int] = None
    modelVersion: Optional[str] = None
    createdAt: datetime

class PrecedentVector(BaseModel):
    id: str
    sourceCaseId: Optional[str] = None
    embedding: Optional[List[float]] = None  # pgvector: list of floats
    summary: Optional[str] = None
    keyPolicies: Optional[List[str]] = None
    siteContext: Optional[str] = None
    modelVersion: Optional[str] = None
    createdAt: datetime
