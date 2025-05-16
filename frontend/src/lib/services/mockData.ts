// frontend/src/lib/services/mockData.ts
import type {
	Policy, Site, Scenario, Goal, PlanDocument, Constraint,
	PlanningApplication, PrecedentCase, OfficerReport, DocumentNode, SiteAssessmentResponse
} from '$types/models';
import { get } from 'svelte/store';
import { sites, policies, planningApplications } from '$lib/stores/mainDataStore';

// --- Counters for unique IDs ---
let policyIdCounter = 1;
let siteIdCounter = 1;
let scenarioIdCounter = 1;
let goalIdCounter = 1;
let documentIdCounter = 1;
let documentNodeIdCounter = 1;
let constraintIdCounter = 1;
let appIDC = { val: 1 };
let precedentIdCounter = 1;
let reportSectionIdCounter = 1;

const generateId = (prefix: string, counter: { val: number }) => `${prefix}-${counter.val++}`;
const policyIDC = { val: 1 }; // Pass objects to allow modification within functions
const siteIDC = { val: 1 };
const constraintIDC = { val: 1 };
// ... and so on for all counters

// --- Mock Data Functions (Expanded) ---

export function getMockPolicies(): Policy[] {
	// ... (as defined in previous step, ensure documentId links to a PlanDocument)
    // Example:
    return [
		{
			id: generateId('pol', policyIDC),
			reference: 'H1',
			title: 'Delivering a Sustainable Mix of Homes',
			wording: 'Proposals for new housing development will be supported where they provide a mix of dwelling types and sizes to meet identified local needs. A minimum of 30% affordable housing will be required on sites of 10 or more dwellings.',
			status: 'Adopted',
			type: 'Strategic',
			documentId: 'lp2025', // Assumes a PlanDocument with this ID exists
			supportingText: 'This policy aims to ensure that new housing developments contribute to a balanced housing market.',
			internalNotes: 'Affordable housing threshold reviewed in 2023. Link to SHMA.',
            strategicGoalAlignments: [{goalId: 'goal-1', goalName: 'Housing Delivery Target', alignment: 'Supports'}],
            requirementsSummary: 'Min 30% affordable housing on sites >= 10 dwellings.'
		},
		{
			id: generateId('pol', policyIDC),
			reference: 'DM12',
			title: 'Design Quality and Local Character',
			wording: 'All new development must demonstrate high quality design and positively contribute to local character and distinctiveness. Proposals should respect the scale, massing, and materials of the surrounding area.',
			status: 'Draft',
			type: 'Development Management (DM)',
			documentId: 'lp2025',
            linkedPolicies: [{policyId: `pol-1`, policyReference: 'H1', relationship: 'SUPPORTS', summary: 'Ensures housing is well-designed.'}],
            requirementsSummary: 'High quality design, respect local character.'
		},
        // Add more policies relevant to DM as well
	];
}

export function getMockSites(): Site[] {
    // ... (as defined in previous step, ensure data for both Plan-Making and DM contexts)
    // Example for a site that might also be an application site:
    return [
        {
			id: generateId('site', siteIDC),
			name: 'Greenfield North',
            address: 'Land North of Old Mill Lane, Northwood',
            uprn: '10001234567',
            lpaCode: 'E07000001',
            coordinates: { lat: 51.5, lon: -0.15 },
            areaHa: 10.5,
            parish: 'Northwood Parish',
			planMakingStatus: 'Draft Allocation',
			source: 'SHLAA',
			proposedUsePlanMaking: 'Residential (approx 150 dwellings)',
            constraints: [ {id: 'con-1', name: 'Partially in AONB buffer zone', type: 'Landscape'}, {id: 'con-2', name: 'Flood Zone 1', type: 'Flood Risk'} ],
            applicablePolicies: [/* full Policy objects or references */],
            policyRequirementsSummary: [{policyId: 'pol-1', policyRef: 'H1', requirement: '30% affordable housing', relevance: "Applies due to site size."}],
            strategicGoalContributions: [{goalId: 'goal-1', goalName: 'Housing Delivery Target', alignment: 'Supports'}],
            deliverabilityAssessment: [{name: 'Access', score: 7, rationale: 'Requires new access road.'}],
            soundnessChecksPlanMaking: [{criterion: 'NPPF Sustainable Development', status: '🟡 Minor Issues', rationale: 'Greenfield site, impact on landscape.'}]
		},
    ];
}

export function getMockConstraints(): Constraint[] {
    return [
        { id: generateId('con', constraintIDC), name: 'Flood Zone 3', type: 'Flood Risk', severity: 'High', description: 'High probability of flooding.'},
        { id: generateId('con', constraintIDC), name: 'Conservation Area', type: 'Heritage', severity: 'High', description: 'Statutory designation, special character to preserve/enhance.'},
        { id: generateId('con', constraintIDC), name: 'Green Belt', type: 'Spatial Strategy', severity: 'High', description: 'Strong protection against inappropriate development.'},
        { id: generateId('con', constraintIDC), name: 'Tree Preservation Order (TPO 123)', type: 'Amenity', severity: 'Medium', description: 'Specific group of trees protected.'},
    ];
}

export function getMockPlanningApplications(): PlanningApplication[] {
    const site1 = get(sites).find((s: Site) => s.id === 'site-1');
    return [
        {
            id: generateId('app', appIDC),
            referenceNumber: '25/00123/FUL',
            address: site1?.address || 'Land North of Old Mill Lane, Northwood',
            siteId: site1?.id,
            proposalDetails: 'Erection of 145 dwellings with associated access, landscaping and infrastructure.',
            applicationType: 'Full',
            status: 'Under Assessment',
            receivedDate: '2025-01-15',
            validatedDate: '2025-01-22',
            caseOfficer: 'Jane Doe',
            constraints: site1?.constraints, // From the site or assessed separately
            relevantPolicies: [
                get(policies).find((p: Policy) => p.reference === 'H1')!,
                get(policies).find((p: Policy) => p.reference === 'DM12')!
            ],
            reasoningSteps: [
                { step: 1, description: "Assess compliance with housing mix policy H1.", policyReferences: ['H1']},
                { step: 2, description: "Evaluate design against DM12 criteria.", policyReferences: ['DM12']},
            ],
            tradeOffAnalysis: {
                competingGoals: [{goalA: "Housing Delivery", goalB: "Landscape Impact (AONB buffer)", tension: "Balancing need for homes with landscape protection."}],
                aiNarrative: "The proposal contributes significantly to housing targets but requires careful mitigation for AONB proximity."
            }
        },
        {
            id: generateId('app', appIDC),
            referenceNumber: '25/00200/OUT',
            address: 'Brownfield Site, Central Town',
            proposalDetails: 'Outline application for mixed-use development (up to 50 dwellings and 500sqm commercial).',
            applicationType: 'Outline',
            status: 'Received',
            receivedDate: '2025-03-10',
            caseOfficer: 'John Smith',
        },
    ];
}

export function getMockPrecedentCases(): PrecedentCase[] {
    return [
        {
            id: generateId('prec', { val: precedentIdCounter }),
            caseReference: 'APP/X1234/W/23/987654',
            address: 'Similar Site, Adjoining LPA',
            decisionType: 'Appeal Decision',
            decisionDate: '2024-06-15',
            outcome: 'Allowed',
            keyPoliciesCited: ['Similar Local Policy A', 'NPPF Paragraph Y'],
            inspectorReasoningSummary: 'Inspector found housing need outweighed landscape harm in this specific instance due to mitigation.',
            relevanceSummary: 'Relevant due to similar scale and landscape considerations.'
        }
    ];
}

export function getMockGoals(): Goal[] {
    return [
        {
            id: 'goal-1',
            name: 'Housing Delivery Target',
            category: 'Policy',
            description: 'Deliver at least 150 new homes by 2026.',
            targetMetric: 'homes',
            targetValue: 150,
            currentValue: 150,
            status: 'On Track',
            type: 'Policy',
        }
    ];
}

export function getMockDocuments(): PlanDocument[] {
    return [
        {
            id: 'lp2025',
            name: 'Local Plan 2025',
            type: 'Local Plan',
            rootNode: {
                id: 'root-1',
                title: 'Root',
                type: 'DocumentRoot',
                children: []
            },
            version: '1.0',
            documentStatus: 'Adopted',
        }
    ];
}

export function getMockScenarios(): Scenario[] {
    return [
        {
            id: 'scen-1',
            name: 'Baseline Scenario',
            description: 'All currently allocated sites and adopted policies.',
            activePolicyIds: ['pol-1', 'pol-2'],
            includedSiteIds: ['site-1'],
            summaryMetrics: { totalHomes: 150, jobsEnabled: 20, riskFlags: 1 },
            goalPerformance: [
                { goalId: 'goal-1', status: 'On Track', value: 150 }
            ],
            createdAt: '2025-01-01T00:00:00Z',
        },
        {
            id: 'scen-2',
            name: 'Growth Scenario',
            description: 'Includes all baseline sites plus additional brownfield allocations.',
            activePolicyIds: ['pol-1', 'pol-2'],
            includedSiteIds: ['site-1'],
            summaryMetrics: { totalHomes: 200, jobsEnabled: 40, riskFlags: 2 },
            goalPerformance: [
                { goalId: 'goal-1', status: 'On Track', value: 200 }
            ],
            createdAt: '2025-02-01T00:00:00Z',
        }
    ];
}

// Adapt existing getMockAssessment or dmMockData functions
// This function can now be more robust by pulling from the new mock entities.
export function getSiteAssessmentForDmMode(applicationId: string): SiteAssessmentResponse | null {
    const app = get(planningApplications).find(a => a.id === applicationId);
    if (!app) return null;

    const siteDetails = app.siteId ? get(sites).find(s => s.id === app.siteId) : { id: app.address, name: app.address }; // Simplified site node

    return {
        site: siteDetails || {id: app.id, name: app.address},
        constraints_affecting_site: app.constraints || [],
        applicable_policies: app.relevantPolicies || [],
        ai_reasoning_output: { summary: `Initial AI assessment for ${app.referenceNumber}: ${app.proposalDetails}` },
        trade_off_matrix: app.tradeOffAnalysis // Or a simplified version
    };
}

// Remove or comment out the old getMockAssessment if it's fully replaced.
// Also, the content of dmMockData.ts should be merged here, and the file itself can be deleted.