from typing import Any, List, Optional, Dict
from datetime import date, datetime
from pydantic import BaseModel

class Site(BaseModel):
    id: str
    name: Optional[str] = None
    address: Optional[str] = None
    uprn: Optional[str] = None
    lpaCode: Optional[str] = None
    geom: Optional[Dict[str, Any]] = None  # Geometry data as dict
    areaHa: Optional[float] = None
    planMakingStatus: Optional[List[str]] = None  # Changed to array
    submissionDate: Optional[date] = None
    source: Optional[str] = None
    deliverabilityAssessment: Optional[Dict[str, Any]] = None
    soundnessChecks: Optional[Dict[str, Any]] = None
    createdAt: datetime
