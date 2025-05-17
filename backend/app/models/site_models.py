# app/models/site_models.py
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field, UUID4
import uuid
from datetime import datetime
from .common_models import (
    PlanMakingStatusEnum, SiteSourceEnum, SoundnessStatusEnum,
    SiteCoordinates, BaseUUIDModel
)
# Need to import Constraint and Policy schemas if they are to be fully nested
# For now, using forward references or List[UUID4] for simplicity in this stub
from .constraint_models import Constraint # Assuming full object for now
from .policy_models import Policy # Assuming full object for now


class PolicyRequirementSummarySite(BaseModel):
    policyId: str
    policyRef: str
    requirement: str
    relevance: Optional[str] = None

class StrategicGoalContributionSite(BaseModel):
    goalId: str
    goalName: str
    alignment: str # TODO: Enum: 'Supports' | 'Partially Aligns' | 'Undermines'
    notes: Optional[str] = None

class DeliverabilityAssessmentSite(BaseModel):
    name: str
    score: int
    confidence: Optional[int] = None
    rationale: Optional[str] = None

class SoundnessCheckPlanMakingSite(BaseModel):
    criterion: str
    status: SoundnessStatusEnum
    rationale: Optional[str] = None

# --- Site Model ---
class SiteBase(BaseModel):
    name: Optional[str] = Field(None, examples=["Greenfield North"])
    address: Optional[str] = None
    uprn: Optional[str] = None
    lpaCode: Optional[str] = None
    coordinates: Optional[SiteCoordinates] = None
    areaHa: Optional[float] = None
    parish: Optional[str] = None
    # Plan-Making Specific Fields
    planMakingStatus: Optional[PlanMakingStatusEnum] = None
    submissionDate: Optional[datetime] = None # For call for sites
    source: Optional[SiteSourceEnum] = None
    proposedUsePlanMaking: Optional[str] = None
    planningHistorySummary: Optional[List[str]] = Field(default_factory=list)
    # DM & Shared Fields
    constraints: Optional[List[Constraint]] = Field(default_factory=list) # Or List[UUID4]
    applicablePolicies: Optional[List[Policy]] = Field(default_factory=list) # Or List[UUID4]
    policyRequirementsSummary: Optional[List[PolicyRequirementSummarySite]] = Field(default_factory=list) # For DM
    # Plan-Making Specific Assessments
    allocationJustification: Optional[str] = None
    aiDraftJustification: Optional[str] = None
    strategicGoalContributions: Optional[List[StrategicGoalContributionSite]] = Field(default_factory=list)
    deliverabilityAssessment: Optional[List[DeliverabilityAssessmentSite]] = Field(default_factory=list)
    soundnessChecksPlanMaking: Optional[List[SoundnessCheckPlanMakingSite]] = Field(default_factory=list)

class SiteCreate(SiteBase):
    name: str # Making name required for creation example

class SiteUpdate(SiteBase):
    # All fields are optional for PATCH
    pass

class Site(SiteBase, BaseUUIDModel):
    pass

    class Config:
        from_attributes = True
