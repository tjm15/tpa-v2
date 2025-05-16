// frontend/src/lib/types/models.ts

// --- Core Enums and General Types ---
export type PolicyStatus = 'Draft' | 'Adopted' | 'Consultation' | 'Under Review' | 'Archived';
export type PolicyType = 'Strategic' | 'Development Management (DM)' | 'Supplementary Planning Document (SPD)' | 'National (NPPF)' | 'Guidance Note';
export type RelationshipType = 'SUPPORTS' | 'CONFLICTS_WITH' | 'REFERENCES' | 'REFERENCED_BY' | 'OVERLAPS_WITH' | 'SUPERSEDES';
export type ImpactType = 'Enables' | 'Restricts' | 'Conditions Development' | 'No Direct Impact';
export type GoalStatus = 'On Track' | 'Partial' | 'Failing' | 'Not Started' | 'Achieved' | 'Superseded';
export type GoalType = 'Legal' | 'Policy' | 'Monitoring' | 'Political' | 'Aspirational';
export type SoundnessStatus = '🟢 Sound' | '🟡 Minor Issues' | '🔴 Major Issues' | '⚪ Not Assessed';
export type DocumentNodeType = 'DocumentRoot' | 'Chapter' | 'SubChapter' | 'PolicySection' | 'MapSection' | 'Appendix' | 'GlossaryItem' | 'ReportSection';
export type ApplicationStatus = 'Received' | 'Validated' | 'Under Assessment' | 'Pending Decision' | 'Approved' | 'Refused' | 'Withdrawn' | 'Appealed';
export type ApplicationType = 'Full' | 'Outline' | 'Reserved Matters' | 'Listed Building Consent' | 'Advertisement Consent' | 'Lawful Development Certificate' | 'Prior Approval';
export type PrecedentDecisionOutcome = 'Allowed' | 'Dismissed' | 'Split Decision' | 'Withdrawn';

// --- Shared Entities ---

export interface Constraint { // More detailed than ConstraintOverlayData
	id: string;
	name: string; // e.g., "Flood Zone 3", "Conservation Area"
	type: string; // e.g., "Flood Risk", "Heritage"
	severity?: 'High' | 'Medium' | 'Low' | 'Informational';
	sourceDocument?: string; // e.g., "Environment Agency Flood Map for Planning"
	geometry?: any; // GeoJSON for map display
	description?: string;
}

export interface Policy {
	id: string;
	reference: string; // e.g., H2, DM12
	title: string;
	wording: string; // Rich text or markdown
	status: PolicyStatus;
	type: PolicyType;
	version?: string;
	lastModified?: string;
	author?: string;
	authorNotes?: string;
	supportingText?: string;
	internalNotes?: string; // Officer justification, legal concerns
	linkedPolicies?: { policyId: string; policyReference: string; relationship: RelationshipType; summary?: string }[];
	affectedSiteCategories?: string[]; // e.g., "Residential", "Brownfield"
	strategicGoalAlignments?: { goalId: string; goalName: string; alignment: 'Supports' | 'Partially Aligns' | 'Undermines' | 'Neutral'; notes?: string }[];
	aiGuidance?: { type: string; message: string; source?: string }[];
	documentId: string; // ID of the PlanDocument this policy belongs to
	keywords?: string[];
    requirementsSummary?: string; // e.g., "minimum 30% affordable" - for DM Reasoning Mode
}

export interface Site {
	id: string;
	name?: string; // Can be an address or a descriptive name like "Greenfield North"
	address?: string;
	uprn?: string;
	lpaCode?: string; // Local Planning Authority Code
	coordinates?: { lat: number; lon: number } | any; // GeoJSON point or polygon for boundary
	areaHa?: number;
	parish?: string;
	// Plan-Making Specific Fields
	planMakingStatus?: 'Considered' | 'Draft Allocation' | 'Adopted Allocation' | 'Rejected' | 'Promoted' | 'Previously Allocated';
	submissionDate?: string; // For call for sites
	source?: 'SHLAA' | 'Call For Sites' | 'Strategic Proposal' | 'Officer Generated' | 'Planning Application';
	proposedUsePlanMaking?: string;
	planningHistorySummary?: string[];
	// DM & Shared Fields
	constraints?: Constraint[];
	applicablePolicies?: Policy[]; // Could be a list of full policy objects or just IDs/references
    policyRequirementsSummary?: { policyId: string; policyRef: string; requirement: string, relevance?: string }[]; // For DM
	// Plan-Making Specific Assessments
	allocationJustification?: string;
	aiDraftJustification?: string;
	strategicGoalContributions?: { goalId: string; goalName: string; alignment: 'Supports' | 'Partially Aligns' | 'Undermines'; notes?: string }[];
	deliverabilityAssessment?: { name: string; score: number; confidence?: number; rationale?: string }[];
	soundnessChecksPlanMaking?: { criterion: string; status: SoundnessStatus; rationale?: string }[];
}

// --- Plan-Making Specific Types (from Specification.md) ---
export interface Scenario {
	id: string;
	name: string;
	description?: string;
	baselineScenarioId?: string;
	tags?: string[];
	summaryMetrics?: { totalHomes?: number; jobsEnabled?: number; infrastructureNeed?: number; riskFlags?: number; tradeOffIndex?: number };
	includedSiteIds?: string[];
	excludedSiteIds?: string[];
	activePolicyIds?: string[];
	modifiedPolicies?: { policyId: string; changes: Partial<Policy> }[];
	goalPerformance?: { goalId: string; status: GoalStatus; value: number | string }[];
	soundnessFlags?: { criterion: string; status: SoundnessStatus; rationale?: string }[];
	aiCommentary?: string;
	createdAt?: string;
	lastModified?: string;
}

export interface Goal {
	id: string;
	name: string;
	category: string;
	description?: string;
	targetMetric: string;
	targetValue?: number;
	currentValue?: number;
	unit?: string;
	source?: string;
	status: GoalStatus;
	type: GoalType;
	contributingPolicyIds?: string[];
	contributingSiteIds?: string[];
	relatedGoalIds?: string[];
	risks?: string[];
	notes?: string;
}

export interface DocumentNode {
	id: string;
	title: string;
	type: DocumentNodeType;
	reference?: string;
	content?: string;
	children?: DocumentNode[];
	unresolvedIssues?: string[];
	linkedEntities?: { type: string; id: string; name: string }[];
	lastModified?: string;
	author?: string;
}

export interface PlanDocument {
    id: string;
    name: string;
    type: 'Local Plan' | 'Sustainability Appraisal' | 'Design Code' | 'Proposals Map' | 'SPD' | 'Evidence Base Document';
    rootNode: DocumentNode;
    version?: string;
    documentStatus?: 'Draft' | 'Consultation' | 'Submitted' | 'Adopted';
}


// --- Development Management (DM) Specific Types (from DM Modes doc) ---
export interface PlanningApplication {
    id: string;
    referenceNumber: string; // e.g., APP-001
    address: string;
    siteId?: string; // Link to a Site entity if applicable
    siteDescription?: string; // If not a predefined site
    proposalDetails: string;
    applicationType: ApplicationType;
    status: ApplicationStatus;
    receivedDate: string;
    validatedDate?: string;
    decisionDate?: string;
    decision?: 'Approved' | 'Refused' | 'Approved with Conditions';
    applicantName?: string;
    agentName?: string;
    caseOfficer?: string;
    // Fields for DM Site Assessment Mode
    constraints?: Constraint[]; // Overlapping constraints for the application site
    relevantPolicies?: Policy[]; // Ranked list of applicable policies
    // Fields for DM Reasoning Mode
    reasoningSteps?: { step: number; description: string; policyReferences?: string[] }[];
    tradeOffAnalysis?: {
        competingGoals: { goalA: string; goalB: string; tension: string }[];
        aiNarrative?: string;
        plannerWeightings?: { [goalOrPolicyId: string]: number };
    };
    // Fields for DM Precedent Review Mode
    linkedPrecedents?: PrecedentCase[];
    // Fields for DM Report Generation Mode
    officerReport?: OfficerReport;
}

export interface PrecedentCase {
    id: string;
    caseReference: string; // Application number or appeal reference
    address: string;
    decisionType: 'LPA Decision' | 'Appeal Decision';
    decisionDate: string;
    outcome: PrecedentDecisionOutcome;
    keyPoliciesCited: string[];
    inspectorReasoningSummary?: string; // If appeal
    decisionExtractLink?: string; // Link to full report/decision notice
    relevanceSummary?: string;
    similarityCriteria?: {
        site?: string; // e.g., "Similar geometry, brownfield"
        policyOverlap?: string[];
    };
}

export interface OfficerReportSection {
    id: string;
    title: string; // e.g., "Introduction", "Site Context", "Policy Considerations"
    content: string; // Markdown or rich text, potentially auto-filled
    order: number;
}
export interface OfficerReport {
    applicationId: string;
    version: string;
    sections: OfficerReportSection[];
    recommendation?: string;
    supportingEvidenceLinks?: { name: string; url_or_id: string }[];
    conflictSummary?: string;
    complianceFlags?: { flag: string; met: boolean }[];
    lastModified: string;
    status: 'Draft' | 'Review' | 'Final';
}


// --- General UI State Types ---
export type PlanMakingMode = 'policy' | 'site-allocation' | 'scenario' | 'goal-tracker' | 'document';
export type DevelopmentManagementMode = 'dm-site-assessment' | 'dm-reasoning' | 'dm-precedent-review' | 'dm-report-generation';
export type ActiveWorkspace = 'plan-making' | 'development-management' | 'dashboard' | null;
export type ActiveMode = PlanMakingMode | DevelopmentManagementMode | null;


// --- Existing SiteAssessmentResponse (from appStore/dmStore) ---
// We need to decide if this is still a primary interaction object or if its data
// gets merged/transformed into the more detailed Site and PlanningApplication types.
// For now, let's keep it to acknowledge its current existence.
// It seems more aligned with the DM Site Assessment Mode's output.
export interface SiteAssessmentResponse {
  site: Partial<Site>; // Use partial Site for flexibility
  constraints_affecting_site: Constraint[]; // Use new Constraint type
  applicable_policies: Partial<Policy>[]; // Use partial Policy type
  ai_reasoning_output: { summary: string, details?: any };
  trade_off_matrix: any | null; // This is also in PlanningApplication.tradeOffAnalysis
}