# app/models/__init__.py
from .common_models import (
    PolicyStatusEnum, PolicyTypeEnum, RelationshipTypeEnum, ImpactTypeEnum,
    GoalStatusEnum, GoalTypeEnum, SoundnessStatusEnum, DocumentNodeTypeEnum,
    ApplicationStatusEnum, ApplicationTypeEnum, PrecedentDecisionOutcomeEnum,
    ConstraintSeverityEnum, PlanMakingStatusEnum, SiteSourceEnum,
    PlanDocumentTypeEnum, PlanDocumentStatusEnum, OfficerReportStatusEnum,
    GeoJSONGeometry, SiteCoordinates, BaseUUIDModel, PaginatedResponse
)
from .constraint_models import Constraint, ConstraintCreate, ConstraintUpdate
from .policy_models import Policy, PolicyCreate, PolicyUpdate, LinkedPolicy, StrategicGoalAlignmentPolicy, AIGuidance
from .site_models import Site, SiteCreate, SiteUpdate, PolicyRequirementSummarySite, StrategicGoalContributionSite, DeliverabilityAssessmentSite, SoundnessCheckPlanMakingSite
from .scenario_models import Scenario, ScenarioCreate, ScenarioUpdate, ScenarioSummaryMetrics, ModifiedPolicyScenario, GoalPerformanceScenario, SoundnessFlagScenario
from .goal_models import Goal, GoalCreate, GoalUpdate
from .document_models import DocumentNode, DocumentNodeCreate, DocumentNodeUpdate, PlanDocument, PlanDocumentCreate, PlanDocumentUpdate, LinkedEntity
from .planning_application_models import PlanningApplication, PlanningApplicationCreate, PlanningApplicationUpdate, ReasoningStep, CompetingGoal, TradeOffAnalysis
from .precedent_models import PrecedentCase, PrecedentCaseCreate, PrecedentCaseUpdate, SimilarityCriteria
from .officer_report_models import OfficerReportSection, OfficerReportSectionCreate, OfficerReportSectionUpdate, OfficerReport, OfficerReportCreate, OfficerReportUpdate, SupportingEvidenceLink, ComplianceFlag

# This helps in making Pydantic update forward refs for recursive models like DocumentNode
DocumentNode.model_rebuild()
PlanDocument.model_rebuild()

# You might want to define __all__ if you use `from .models import *` elsewhere
