# app/models/scenario_models.py
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, UUID4
import uuid
from datetime import datetime
from .common_models import GoalStatusEnum, SoundnessStatusEnum, BaseUUIDModel
from .policy_models import PolicyUpdate # For modifiedPolicies

class ScenarioSummaryMetrics(BaseModel):
    totalHomes: Optional[int] = None
    jobsEnabled: Optional[int] = None
    infrastructureNeed: Optional[int] = None
    riskFlags: Optional[int] = None
    tradeOffIndex: Optional[float] = None

class ModifiedPolicyScenario(BaseModel):
    policyId: UUID4
    changes: PolicyUpdate # Using the PolicyUpdate model where all fields are optional

class GoalPerformanceScenario(BaseModel):
    goalId: UUID4
    status: GoalStatusEnum
    value: Union[int, str]

class SoundnessFlagScenario(BaseModel):
    criterion: str
    status: SoundnessStatusEnum
    rationale: Optional[str] = None

# --- Scenario Model ---
class ScenarioBase(BaseModel):
    name: str
    description: Optional[str] = None
    baselineScenarioId: Optional[UUID4] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    summaryMetrics: Optional[ScenarioSummaryMetrics] = None
    includedSiteIds: Optional[List[UUID4]] = Field(default_factory=list)
    excludedSiteIds: Optional[List[UUID4]] = Field(default_factory=list)
    activePolicyIds: Optional[List[UUID4]] = Field(default_factory=list)
    modifiedPolicies: Optional[List[ModifiedPolicyScenario]] = Field(default_factory=list)
    goalPerformance: Optional[List[GoalPerformanceScenario]] = Field(default_factory=list)
    soundnessFlags: Optional[List[SoundnessFlagScenario]] = Field(default_factory=list)
    aiCommentary: Optional[str] = None

class ScenarioCreate(ScenarioBase):
    pass

class ScenarioUpdate(ScenarioBase):
    name: Optional[str] = None
    # All fields are optional for PATCH

class Scenario(ScenarioBase, BaseUUIDModel):
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    lastModified: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
