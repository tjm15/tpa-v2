from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class Policy(BaseModel):
    id: str
    policyId: str  # e.g. "H1", "DM3" 
    policyTitle: str
    tags: Optional[List[str]] = None  # e.g. ["strategic","SPD"]
    summary: str
    crossReferences: Optional[List[str]] = None  # codes of other policies
    geographicMentions: Optional[List[str]] = None
    documentId: Optional[str] = None
    lpaCode: Optional[str] = None
    createdAt: datetime

class PolicyCrossLink(BaseModel):
    sourcePolicyCode: str  # original code
    targetPolicyCode: str
    sourcePolicyId: Optional[str] = None
    targetPolicyId: Optional[str] = None
