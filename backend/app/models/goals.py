from typing import List, Optional
from pydantic import BaseModel
from app.models.shared import GoalStatus, GoalType

class Goal(BaseModel):
    id: str
    name: str
    category: str
    description: Optional[str] = None
    targetMetric: str
    targetValue: Optional[float] = None
    currentValue: Optional[float] = None
    unit: Optional[str] = None
    source: Optional[str] = None
    status: GoalStatus
    type: GoalType
    contributingPolicyIds: Optional[List[str]] = None
    contributingSiteIds: Optional[List[str]] = None
    relatedGoalIds: Optional[List[str]] = None
    risks: Optional[List[str]] = None
    notes: Optional[str] = None
