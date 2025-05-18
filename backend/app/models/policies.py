from typing import List, Optional
from pydantic import BaseModel
from app.models.shared import (
    PolicyStatus,
    PolicyType,
    RelationshipType,
)

class PolicyLink(BaseModel):
    policyId: str
    policyReference: str
    relationship: RelationshipType
    summary: Optional[str] = None

class StrategicGoalAlignment(BaseModel):
    goalId: str
    goalName: str
    alignment: str  # 'Supports' | 'Partially Aligns' | 'Undermines' | 'Neutral'
    notes: Optional[str] = None

class AIGuidance(BaseModel):
    type: str
    message: str
    source: Optional[str] = None

class Policy(BaseModel):
    id: str
    reference: str
    title: str
    wording: str
    status: PolicyStatus
    type: PolicyType
    version: Optional[str] = None
    lastModified: Optional[str] = None
    author: Optional[str] = None
    authorNotes: Optional[str] = None
    supportingText: Optional[str] = None
    internalNotes: Optional[str] = None
    linkedPolicies: Optional[List[PolicyLink]] = None
    affectedSiteCategories: Optional[List[str]] = None
    strategicGoalAlignments: Optional[List[StrategicGoalAlignment]] = None
    aiGuidance: Optional[List[AIGuidance]] = None
    documentId: str
    keywords: Optional[List[str]] = None
    requirementsSummary: Optional[str] = None
