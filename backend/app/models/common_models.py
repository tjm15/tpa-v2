# app/models/common_models.py
from enum import Enum
from typing import Optional, List, Any, Dict, Union, Generic, TypeVar
from pydantic import BaseModel, Field, UUID4
import uuid
from datetime import datetime

# --- Enums from TypeScript models ---
class PolicyStatusEnum(str, Enum):
    DRAFT = 'Draft'
    ADOPTED = 'Adopted'
    CONSULTATION = 'Consultation'
    UNDER_REVIEW = 'Under Review'
    ARCHIVED = 'Archived'

class PolicyTypeEnum(str, Enum):
    STRATEGIC = 'Strategic'
    DEVELOPMENT_MANAGEMENT_DM = 'Development Management (DM)'
    SUPPLEMENTARY_PLANNING_DOCUMENT_SPD = 'Supplementary Planning Document (SPD)'
    NATIONAL_NPPF = 'National (NPPF)'
    GUIDANCE_NOTE = 'Guidance Note'

class RelationshipTypeEnum(str, Enum):
    SUPPORTS = 'SUPPORTS'
    CONFLICTS_WITH = 'CONFLICTS_WITH'
    REFERENCES = 'REFERENCES'
    REFERENCED_BY = 'REFERENCED_BY'
    OVERLAPS_WITH = 'OVERLAPS_WITH'
    SUPERSEDES = 'SUPERSEDES'

class ImpactTypeEnum(str, Enum):
    ENABLES = 'Enables'
    RESTRICTS = 'Restricts'
    CONDITIONS_DEVELOPMENT = 'Conditions Development'
    NO_DIRECT_IMPACT = 'No Direct Impact'

class GoalStatusEnum(str, Enum):
    ON_TRACK = 'On Track'
    PARTIAL = 'Partial'
    FAILING = 'Failing'
    NOT_STARTED = 'Not Started'
    ACHIEVED = 'Achieved'
    SUPERSEDED = 'Superseded'

class GoalTypeEnum(str, Enum):
    LEGAL = 'Legal'
    POLICY = 'Policy'
    MONITORING = 'Monitoring'
    POLITICAL = 'Political'
    ASPIRATIONAL = 'Aspirational'

class SoundnessStatusEnum(str, Enum):
    SOUND = '🟢 Sound'
    MINOR_ISSUES = '🟡 Minor Issues'
    MAJOR_ISSUES = '🔴 Major Issues'
    NOT_ASSESSED = '⚪ Not Assessed'

class DocumentNodeTypeEnum(str, Enum):
    DOCUMENT_ROOT = 'DocumentRoot'
    CHAPTER = 'Chapter'
    SUB_CHAPTER = 'SubChapter'
    POLICY_SECTION = 'PolicySection'
    MAP_SECTION = 'MapSection'
    APPENDIX = 'Appendix'
    GLOSSARY_ITEM = 'GlossaryItem'
    REPORT_SECTION = 'ReportSection'

class ApplicationStatusEnum(str, Enum):
    RECEIVED = 'Received'
    VALIDATED = 'Validated'
    UNDER_ASSESSMENT = 'Under Assessment'
    PENDING_DECISION = 'Pending Decision'
    APPROVED = 'Approved'
    REFUSED = 'Refused'
    WITHDRAWN = 'Withdrawn'
    APPEALED = 'Appealed'

class ApplicationTypeEnum(str, Enum):
    FULL = 'Full'
    OUTLINE = 'Outline'
    RESERVED_MATTERS = 'Reserved Matters'
    LISTED_BUILDING_CONSENT = 'Listed Building Consent'
    ADVERTISEMENT_CONSENT = 'Advertisement Consent'
    LAWFUL_DEVELOPMENT_CERTIFICATE = 'Lawful Development Certificate'
    PRIOR_APPROVAL = 'Prior Approval'

class PrecedentDecisionOutcomeEnum(str, Enum):
    ALLOWED = 'Allowed'
    DISMISSED = 'Dismissed'
    SPLIT_DECISION = 'Split Decision'
    WITHDRAWN = 'Withdrawn'

class ConstraintSeverityEnum(str, Enum):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'
    INFORMATIONAL = 'Informational'

class PlanMakingStatusEnum(str, Enum):
    CONSIDERED = 'Considered'
    DRAFT_ALLOCATION = 'Draft Allocation'
    ADOPTED_ALLOCATION = 'Adopted Allocation'
    REJECTED = 'Rejected'
    PROMOTED = 'Promoted'
    PREVIOUSLY_ALLOCATED = 'Previously Allocated'

class SiteSourceEnum(str, Enum):
    SHLAA = 'SHLAA'
    CALL_FOR_SITES = 'Call For Sites'
    STRATEGIC_PROPOSAL = 'Strategic Proposal'
    OFFICER_GENERATED = 'Officer Generated'
    PLANNING_APPLICATION = 'Planning Application'

class PlanDocumentTypeEnum(str, Enum):
    LOCAL_PLAN = 'Local Plan'
    SUSTAINABILITY_APPRAISAL = 'Sustainability Appraisal'
    DESIGN_CODE = 'Design Code'
    PROPOSALS_MAP = 'Proposals Map'
    SPD = 'SPD'
    EVIDENCE_BASE_DOCUMENT = 'Evidence Base Document'

class PlanDocumentStatusEnum(str, Enum):
    DRAFT = 'Draft'
    CONSULTATION = 'Consultation'
    SUBMITTED = 'Submitted'
    ADOPTED = 'Adopted'

class OfficerReportStatusEnum(str, Enum):
    DRAFT = 'Draft'
    REVIEW = 'Review'
    FINAL = 'Final'


# --- Common Reusable Schemas ---
class BaseUUIDModel(BaseModel):
    """Base model with UUID id field."""
    id: UUID4 = Field(default_factory=uuid.uuid4)

    class Config:
        from_attributes = True # Formerly orm_mode

class GeoJSONGeometry(BaseModel):
    """
    Represents a GeoJSON geometry object.
    For a more complete definition, you could import/reference full GeoJSON schemas.
    Example: https://geojson.org/schema/Geometry.json
    """
    type: str
    coordinates: Any # Can be nested lists of numbers, depends on the type

class LatLon(BaseModel):
    lat: float
    lon: float

SiteCoordinates = Union[LatLon, GeoJSONGeometry]

DataType = TypeVar('DataType')

class PaginatedResponse(Generic[DataType], BaseModel):
    items: List[DataType]
    total: int
    page: int
    limit: int
    totalPages: int

