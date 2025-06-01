// frontend/src/lib/stores/mainDataStore.ts
import { writable, get } from 'svelte/store';
import type {
	Policy, Site, Scenario, Goal, PlanDocument, Constraint,
	PlanningApplication, PrecedentCase, OfficerReport, SiteAssessmentResponse, DocumentNode
} from '$types/models';
import {
	getMockPolicies, getMockSites, getMockScenarios, getMockGoals, getMockDocuments,
    getMockConstraints, getMockPlanningApplications, getMockPrecedentCases
    // getMockSiteAssessment // Keep or adapt
} from '$services/mockData'; // mockData.ts will need these new functions

// --- Plan-Making Data ---
export const policies = writable<Policy[]>([]);
export const sites = writable<Site[]>([]); // Shared sites, can be filtered by context
export const scenarios = writable<Scenario[]>([]);
export const goals = writable<Goal[]>([]);
export const planDocuments = writable<PlanDocument[]>([]);
export const constraints = writable<Constraint[]>([]); // Shared constraints

// --- Development Management Data ---
export const planningApplications = writable<PlanningApplication[]>([]);
export const precedentCases = writable<PrecedentCase[]>([]);
// Officer reports might be part of PlanningApplication or stored separately
// export const officerReports = writable<OfficerReport[]>([]);

// --- Potentially still useful for a specific, focused task or DM site assessment summary ---
export const activeSiteAssessment = writable<SiteAssessmentResponse | null>(null);


export function loadInitialData() {
	// Plan-Making Data
	policies.set(getMockPolicies());
	sites.set(getMockSites()); // Mock sites should be flexible enough for both contexts
	scenarios.set(getMockScenarios());
	goals.set(getMockGoals());
	planDocuments.set(getMockDocuments());
	constraints.set(getMockConstraints());

	// DM Data
	planningApplications.set(getMockPlanningApplications());
	precedentCases.set(getMockPrecedentCases());

    // Example for activeSiteAssessment (e.g., from dmMockData.ts)
    // import { getDmMockAssessment } from '$services/dmMockData';
    // activeSiteAssessment.set(getDmMockAssessment());
}

// --- Utility Functions ---
export function getPolicyById(id: string): Policy | undefined { return get(policies).find((p: Policy) => p.id === id); }
export function findPolicy(id: string): Policy | undefined { return get(policies).find((p: Policy) => p.id === id); }
export function findSite(id: string): Site | undefined { return get(sites).find(s => s.id === id); }
export function findConstraint(id: string): Constraint | undefined { return get(constraints).find(c => c.id === id); }
export function findApplication(id: string): PlanningApplication | undefined { return get(planningApplications).find(app => app.id === id); }

// Find a DocumentNode by id in a PlanDocument
export function findDocumentNode(document: PlanDocument, nodeId: string): DocumentNode | null {
    function search(node: DocumentNode): DocumentNode | null {
        if (node.id === nodeId) return node;
        if (node.children) {
            for (const child of node.children) {
                const found = search(child);
                if (found) return found;
            }
        }
        return null;
    }
    return document.rootNode ? search(document.rootNode) : null;
}

// Functions from your existing stores that might be merged or adapted:
// from planStore.ts: setPlanAssessment, usePlanAssessment
// from dmStore.ts: setDmAssessment, useDmAssessment
// from appStore.ts: setStoreAssessment, useAssessment

// These could now operate on 'activeSiteAssessment' or specific DM application objects.
export function setActiveSiteAssessment(data: SiteAssessmentResponse) {
  activeSiteAssessment.set(data);
}
export function useActiveSiteAssessment() {
  return get(activeSiteAssessment);
}

// Consider if the old store files (planStore.ts, dmStore.ts, appStore.ts) should now be deleted.
// If their specific SiteAssessmentResponse logic is handled by `activeSiteAssessment` and `models.ts`
// has evolved, they might be redundant.
// For example, planStore.ts is effectively replaced by mainDataStore.ts.
// dmStore.ts functionality might be tied to the DM Site Assessment mode and use `activeSiteAssessment`.
// appStore.ts is likely replaced by `uiStateStore.ts` and `mainDataStore.ts`.