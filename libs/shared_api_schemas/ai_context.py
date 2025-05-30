from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel

class ApplicationAIContext(BaseModel):
    applicationId: str
    retrievalLogId: Optional[str] = None
    reasoningSteps: Optional[Dict[str, Any]] = None
    competingGoals: Optional[Dict[str, Any]] = None
    narrative: Optional[str] = None
    modelVersion: Optional[str] = None
    createdAt: datetime

class ApplicationMaterialRef(BaseModel):
    applicationId: str
    materialType: str  # 'policy','constraint','precedent'
    materialCode: str  # e.g. "H1", free-text if unresolved
    materialId: Optional[str] = None  # nullable FK when resolved

class RetrievalLog(BaseModel):
    logId: str
    timestamp: datetime
    query: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
    matchedChunkIds: Optional[List[str]] = None
    retrievalTarget: Optional[str] = None  # e.g. 'policy_vectors'
    agentContext: Optional[Dict[str, Any]] = None

class WriteLog(BaseModel):
    id: str
    timestamp: datetime
    outputType: str
    sourceEntity: Optional[str] = None
    sourceId: Optional[str] = None
    inputSnapshot: Optional[Dict[str, Any]] = None
    modelVersion: Optional[str] = None
    outputText: Optional[str] = None
    author: Optional[str] = 'LLM'
    confidence: Optional[float] = None
    notes: Optional[str] = None

class AIEnrichment(BaseModel):
    id: str
    targetTable: str
    targetId: str
    enrichmentType: str
    enrichedFields: Dict[str, Any]
    modelVersion: Optional[str] = None
    createdAt: datetime
