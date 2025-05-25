from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel

class PrecedentCase(BaseModel):
    id: str
    applicationId: Optional[str] = None
    caseReference: str
    address: Optional[str] = None
    decisionDate: Optional[date] = None
    outcome: Optional[List[str]] = None  # Changed to array
    createdAt: datetime

class PrecedentKeyPolicy(BaseModel):
    precedentId: str
    policyCode: str
    policyId: Optional[str] = None
