from typing import List, Optional
from pydantic import BaseModel
from app.models.shared import ApplicationType, ApplicationStatus
from app.models.constraints import Constraint
from app.models.policies import Policy
from app.models.precedent_cases import PrecedentCase
from app.models.officer_reports import OfficerReport

class ReasoningStep(BaseModel):
    step: int
    description: str
    policyReferences: Optional[List[str]] = None

class TradeOffAnalysis(BaseModel):
    competingGoals: List[dict]  # each with keys goalA, goalB, tension
    aiNarrative: Optional[str] = None
    plannerWeightings: Optional[dict] = None

class PlanningApplication(BaseModel):
    id: str
    referenceNumber: str
    address: str
    siteId: Optional[str] = None
    siteDescription: Optional[str] = None
    proposalDetails: str
    applicationType: ApplicationType
    status: ApplicationStatus
    receivedDate: str
    validatedDate: Optional[str] = None
    decisionDate: Optional[str] = None
    decision: Optional[str] = None
    applicantName: Optional[str] = None
    agentName: Optional[str] = None
    caseOfficer: Optional[str] = None

    constraints: Optional[List[Constraint]] = None
    relevantPolicies: Optional[List[Policy]] = None

    reasoningSteps: Optional[List[ReasoningStep]] = None
    tradeOffAnalysis: Optional[TradeOffAnalysis] = None

    linkedPrecedents: Optional[List[PrecedentCase]] = None
    officerReport: Optional[OfficerReport] = None
