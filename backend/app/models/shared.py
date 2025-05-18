from enum import Enum

class PolicyStatus(str, Enum):
    Draft = 'Draft'
    Adopted = 'Adopted'
    Consultation = 'Consultation'
    UnderReview = 'Under Review'
    Archived = 'Archived'

class PolicyType(str, Enum):
    Strategic = 'Strategic'
    DevelopmentManagement = 'Development Management (DM)'
    SupplementaryPlanningDocumentSPD = 'Supplementary Planning Document (SPD)'
    National = 'National (NPPF)'
    GuidanceNote = 'Guidance Note'

class RelationshipType(str, Enum):
    SUPPORTS = 'SUPPORTS'
    CONFLICTS_WITH = 'CONFLICTS_WITH'
    REFERENCES = 'REFERENCES'
    REFERENCED_BY = 'REFERENCED_BY'
    OVERLAPS_WITH = 'OVERLAPS_WITH'
    SUPERSEDES = 'SUPERSEDES'

class ImpactType(str, Enum):
    Enables = 'Enables'
    Restricts = 'Restricts'
    ConditionsDevelopment = 'Conditions Development'
    NoDirectImpact = 'No Direct Impact'

class GoalStatus(str, Enum):
    OnTrack = 'On Track'
    Partial = 'Partial'
    Failing = 'Failing'
    NotStarted = 'Not Started'
    Achieved = 'Achieved'
    Superseded = 'Superseded'

class GoalType(str, Enum):
    Legal = 'Legal'
    Policy = 'Policy'
    Monitoring = 'Monitoring'
    Political = 'Political'
    Aspirational = 'Aspirational'

class SoundnessStatus(str, Enum):
    Sound = '🟢 Sound'
    MinorIssues = '🟡 Minor Issues'
    MajorIssues = '🔴 Major Issues'
    NotAssessed = '⚪ Not Assessed'

class DocumentNodeTypeEnum(str, Enum):
    DocumentRoot = 'DocumentRoot'
    Chapter = 'Chapter'
    SubChapter = 'SubChapter'
    PolicySection = 'PolicySection'
    MapSection = 'MapSection'
    Appendix = 'Appendix'
    GlossaryItem = 'GlossaryItem'
    ReportSection = 'ReportSection'

class ApplicationStatus(str, Enum):
    Received = 'Received'
    Validated = 'Validated'
    UnderAssessment = 'Under Assessment'
    PendingDecision = 'Pending Decision'
    Approved = 'Approved'
    Refused = 'Refused'
    Withdrawn = 'Withdrawn'
    Appealed = 'Appealed'

class ApplicationType(str, Enum):
    Full = 'Full'
    Outline = 'Outline'
    ReservedMatters = 'Reserved Matters'
    ListedBuildingConsent = 'Listed Building Consent'
    AdvertisementConsent = 'Advertisement Consent'
    LawfulDevelopmentCertificate = 'Lawful Development Certificate'
    PriorApproval = 'Prior Approval'

class PrecedentDecisionOutcome(str, Enum):
    Allowed = 'Allowed'
    Dismissed = 'Dismissed'
    SplitDecision = 'Split Decision'
    Withdrawn = 'Withdrawn'
