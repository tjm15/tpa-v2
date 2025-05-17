# app/models/precedent_models.py
from typing import Optional, List
from pydantic import BaseModel, Field, UUID4, HttpUrl
import uuid
from datetime import datetime
from .common_models import PrecedentDecisionOutcomeEnum, BaseUUIDModel

class SimilarityCriteria(BaseModel):
    site: Optional[str] = Field(None, examples=["Similar geometry, brownfield"])
    policyOverlap: Optional[List[str]] = Field(default_factory=list)

# --- PrecedentCase Model ---
class PrecedentCaseBase(BaseModel):
    caseReference: str # Application number or appeal reference
    address: str
    decisionType: str # TODO: Enum: 'LPA Decision' | 'Appeal Decision'
    decisionDate: datetime
    outcome: PrecedentDecisionOutcomeEnum
    keyPoliciesCited: List[str] = Field(default_factory=list)
    inspectorReasoningSummary: Optional[str] = None # If appeal
    decisionExtractLink: Optional[HttpUrl] = None # Link to full report/decision notice
    relevanceSummary: Optional[str] = None
    similarityCriteria: Optional[SimilarityCriteria] = None

class PrecedentCaseCreate(PrecedentCaseBase):
    pass

class PrecedentCaseUpdate(PrecedentCaseBase):
    caseReference: Optional[str] = None
    address: Optional[str] = None
    decisionType: Optional[str] = None
    decisionDate: Optional[datetime] = None
    outcome: Optional[PrecedentDecisionOutcomeEnum] = None
    # All fields are optional for PATCH

class PrecedentCase(PrecedentCaseBase, BaseUUIDModel):
    pass

    class Config:
        from_attributes = True
