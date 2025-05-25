from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class PolicyVector(BaseModel):
    id: str
    sourceChunkId: str
    embedding: Optional[str] = None  # Will store as string until pgvector is fully integrated
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
    embedding: Optional[str] = None  # Will store as string until pgvector is fully integrated
    documentType: Optional[str] = None
    sectionTitle: Optional[str] = None
    tokens: Optional[int] = None
    modelVersion: Optional[str] = None
    createdAt: datetime

class PrecedentVector(BaseModel):
    id: str
    sourceCaseId: Optional[str] = None
    embedding: Optional[str] = None  # Will store as string until pgvector is fully integrated
    summary: Optional[str] = None
    keyPolicies: Optional[List[str]] = None
    siteContext: Optional[str] = None
    modelVersion: Optional[str] = None
    createdAt: datetime
