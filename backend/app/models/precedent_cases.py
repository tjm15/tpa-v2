from typing import List, Optional
from pydantic import BaseModel
from app.models.shared import PrecedentDecisionOutcome

class SimilarityCriteria(BaseModel):
    site: Optional[str] = None
    policyOverlap: Optional[List[str]] = None

class PrecedentCase(BaseModel):
    id: str
    caseReference: str
    address: str
    decisionType: str  # 'LPA Decision' | 'Appeal Decision'
    decisionDate: str
    outcome: PrecedentDecisionOutcome
    keyPoliciesCited: List[str]
    inspectorReasoningSummary: Optional[str] = None
    decisionExtractLink: Optional[str] = None
    relevanceSummary: Optional[str] = None
    similarityCriteria: Optional[SimilarityCriteria] = None
