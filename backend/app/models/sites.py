from typing import Any, List, Optional, Union
from pydantic import BaseModel
from app.models.constraints import Constraint
from app.models.policies import Policy
from app.models.shared import SoundnessStatus

class SiteCoordinates(BaseModel):
    lat: float
    lon: float

class PolicyRequirementSummary(BaseModel):
    policyId: str
    policyRef: str
    requirement: str
    relevance: Optional[str] = None

class StrategicGoalContribution(BaseModel):
    goalId: str
    goalName: str
    alignment: str  # 'Supports' | 'Partially Aligns' | 'Undermines'
    notes: Optional[str] = None

class DeliverabilityAssessment(BaseModel):
    name: str
    score: float
    confidence: Optional[float] = None
    rationale: Optional[str] = None

class SoundnessCheck(BaseModel):
    criterion: str
    status: SoundnessStatus
    rationale: Optional[str] = None

class Site(BaseModel):
    id: str
    name: Optional[str] = None
    address: Optional[str] = None
    uprn: Optional[str] = None
    lpaCode: Optional[str] = None
    coordinates: Optional[Union[SiteCoordinates, dict]] = None
    areaHa: Optional[float] = None
    parish: Optional[str] = None
    planMakingStatus: Optional[str] = None
    submissionDate: Optional[str] = None
    source: Optional[str] = None
    proposedUsePlanMaking: Optional[str] = None
    planningHistorySummary: Optional[List[str]] = None
    constraints: Optional[List[Constraint]] = None
    applicablePolicies: Optional[List[Policy]] = None
    policyRequirementsSummary: Optional[List[PolicyRequirementSummary]] = None
    allocationJustification: Optional[str] = None
    aiDraftJustification: Optional[str] = None
    strategicGoalContributions: Optional[List[StrategicGoalContribution]] = None
    deliverabilityAssessment: Optional[List[DeliverabilityAssessment]] = None
    soundnessChecksPlanMaking: Optional[List[SoundnessCheck]] = None
