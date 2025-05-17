# app/models/policy_models.py
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, UUID4
import uuid
from datetime import datetime
from .common_models import (
    PolicyStatusEnum, PolicyTypeEnum, RelationshipTypeEnum, BaseUUIDModel
)

class LinkedPolicy(BaseModel):
    policyId: UUID4
    policyReference: str
    relationship: RelationshipTypeEnum
    summary: Optional[str] = None

class StrategicGoalAlignmentPolicy(BaseModel):
    goalId: UUID4
    goalName: str
    alignment: str # TODO: Make enum: 'Supports' | 'Partially Aligns' | 'Undermines' | 'Neutral'
    notes: Optional[str] = None

class AIGuidance(BaseModel):
    type: str
    message: str
    source: Optional[str] = None

# --- Policy Model ---
class PolicyBase(BaseModel):
    reference: str = Field(..., examples=["H2", "DM12"])
    title: str
    wording: str # Rich text or markdown
    status: PolicyStatusEnum
    type: PolicyTypeEnum
    version: Optional[str] = None
    author: Optional[str] = None
    authorNotes: Optional[str] = None
    supportingText: Optional[str] = None
    internalNotes: Optional[str] = None # Officer justification, legal concerns
    linkedPolicies: Optional[List[LinkedPolicy]] = Field(default_factory=list)
    affectedSiteCategories: Optional[List[str]] = Field(default_factory=list, examples=[["Residential", "Brownfield"]])
    strategicGoalAlignments: Optional[List[StrategicGoalAlignmentPolicy]] = Field(default_factory=list)
    aiGuidance: Optional[List[AIGuidance]] = Field(default_factory=list)
    documentId: UUID4 # ID of the PlanDocument this policy belongs to
    keywords: Optional[List[str]] = Field(default_factory=list)
    requirementsSummary: Optional[str] = Field(None, examples=["minimum 30% affordable"])

class PolicyCreate(PolicyBase):
    pass

class PolicyUpdate(PolicyBase):
    reference: Optional[str] = None
    title: Optional[str] = None
    wording: Optional[str] = None
    status: Optional[PolicyStatusEnum] = None
    type: Optional[PolicyTypeEnum] = None
    documentId: Optional[UUID4] = None
    # All fields are optional for PATCH

class Policy(PolicyBase, BaseUUIDModel):
    lastModified: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
