# app/models/goal_models.py
from typing import Optional, List
from pydantic import BaseModel, Field, UUID4
import uuid
from .common_models import GoalStatusEnum, GoalTypeEnum, BaseUUIDModel

# --- Goal Model ---
class GoalBase(BaseUUIDModel):
    name: str
    category: str
    description: Optional[str] = None
    targetMetric: str
    targetValue: Optional[float] = None # Changed to float for flexibility
    currentValue: Optional[float] = None # Changed to float
    unit: Optional[str] = None
    source: Optional[str] = None
    status: GoalStatusEnum
    type: GoalTypeEnum
    contributingPolicyIds: Optional[List[UUID4]] = Field(default_factory=list)
    contributingSiteIds: Optional[List[UUID4]] = Field(default_factory=list)
    relatedGoalIds: Optional[List[UUID4]] = Field(default_factory=list)
    risks: Optional[List[str]] = Field(default_factory=list)
    notes: Optional[str] = None

class GoalCreate(GoalBase):
    pass

class GoalUpdate(GoalBase):
    name: Optional[str] = None
    category: Optional[str] = None
    targetMetric: Optional[str] = None
    status: Optional[GoalStatusEnum] = None
    type: Optional[GoalTypeEnum] = None
    # All fields are optional for PATCH

class Goal(GoalBase):
    name: str  # Match base type
    category: str  # Match base type
    targetMetric: str  # Match base type
    status: GoalStatusEnum  # Match base type
    type: GoalTypeEnum  # Match base type

    class Config(BaseUUIDModel.Config):
        pass
