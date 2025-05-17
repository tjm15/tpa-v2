# app/models/planning_application_models.py
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, UUID4
import uuid
from datetime import datetime
from .common_models import (
    ApplicationStatusEnum, ApplicationTypeEnum, BaseUUIDModel
)
from .constraint_models import Constraint # Full model or ID
from .policy_models import Policy # Full model or ID
from .precedent_models import PrecedentCase # Full model or ID
from .officer_report_models import OfficerReport # Full model or ID

class ReasoningStep(BaseModel):
    step: int
    description: str
    policyReferences: Optional[List[str]] = Field(default_factory=list) # Policy references or IDs

class CompetingGoal(BaseModel):
    goalA: str
    goalB: str
    tension: str

class TradeOffAnalysis(BaseModel):
    competingGoals: Optional[List[CompetingGoal]] = Field(default_factory=list)
    aiNarrative: Optional[str] = None
    plannerWeightings: Optional[Dict[str, float]] = Field(default_factory=dict) # {goalOrPolicyId: weight}

# --- PlanningApplication Model ---
class PlanningApplicationBase(BaseModel):
    referenceNumber: str = Field(..., examples=["APP-001", "25/00123/FUL"])
    address: str
    siteId: Optional[UUID4] = None # Link to a Site entity if applicable
    siteDescription: Optional[str] = None # If not a predefined site
    proposalDetails: str
    applicationType: ApplicationTypeEnum
    status: ApplicationStatusEnum
    receivedDate: datetime
    validatedDate: Optional[datetime] = None
    decisionDate: Optional[datetime] = None
    decision: Optional[str] = Field(None, examples=['Approved', 'Refused', 'Approved with Conditions']) # TODO: Enum
    applicantName: Optional[str] = None
    agentName: Optional[str] = None
    caseOfficer: Optional[str] = None
    # Fields for DM Site Assessment Mode
    constraints: Optional[List[Constraint]] = Field(default_factory=list) # Overlapping constraints
    relevantPolicies: Optional[List[Policy]] = Field(default_factory=list) # Ranked list of applicable policies
    # Fields for DM Reasoning Mode
    reasoningSteps: Optional[List[ReasoningStep]] = Field(default_factory=list)
    tradeOffAnalysis: Optional[TradeOffAnalysis] = None
    # Fields for DM Precedent Review Mode
    linkedPrecedents: Optional[List[PrecedentCase]] = Field(default_factory=list) # Or List[UUID4]
    # Fields for DM Report Generation Mode
    officerReport: Optional[OfficerReport] = None # Or UUID4

class PlanningApplicationCreate(PlanningApplicationBase):
    pass

class PlanningApplicationUpdate(PlanningApplicationBase):
    referenceNumber: Optional[str] = None
    address: Optional[str] = None
    proposalDetails: Optional[str] = None
    applicationType: Optional[ApplicationTypeEnum] = None
    status: Optional[ApplicationStatusEnum] = None
    receivedDate: Optional[datetime] = None
    # All fields are optional for PATCH

class PlanningApplication(PlanningApplicationBase, BaseUUIDModel):
    pass

    class Config:
        from_attributes = True
