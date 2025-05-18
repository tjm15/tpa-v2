from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from app.models.shared import SoundnessStatus

class SummaryMetrics(BaseModel):
    totalHomes: Optional[int] = None
    jobsEnabled: Optional[int] = None
    infrastructureNeed: Optional[int] = None
    riskFlags: Optional[int] = None
    tradeOffIndex: Optional[float] = None

class ModifiedPolicy(BaseModel):
    policyId: str
    changes: Dict[str, Any]

class SoundnessCheck(BaseModel):
    criterion: str
    status: SoundnessStatus
    rationale: Optional[str] = None

class Scenario(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    baselineScenarioId: Optional[str] = None
    tags: Optional[List[str]] = None
    summaryMetrics: Optional[SummaryMetrics] = None
    includedSiteIds: Optional[List[str]] = None
    excludedSiteIds: Optional[List[str]] = None
    activePolicyIds: Optional[List[str]] = None
    modifiedPolicies: Optional[List[ModifiedPolicy]] = None
    goalPerformance: Optional[List[Dict[str, Any]]] = None
    soundnessFlags: Optional[List[SoundnessCheck]] = None
    aiCommentary: Optional[str] = None
    createdAt: Optional[str] = None
    lastModified: Optional[str] = None
