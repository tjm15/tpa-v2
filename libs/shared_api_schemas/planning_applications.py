from typing import List, Optional, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel

class PlanningApplication(BaseModel):
    id: str
    referenceNumber: str
    siteId: Optional[str] = None
    status: Optional[List[str]] = None  # dynamic tags, not rigid enum
    proposalDetails: str
    receivedDate: date
    decisionDate: Optional[date] = None
    applicantName: Optional[str] = None
    agentName: Optional[str] = None
    caseOfficer: Optional[str] = None
    plannerWeightings: Optional[Dict[str, Any]] = None  # UI-fed overrides
    lpaCode: Optional[str] = None
    createdAt: datetime
