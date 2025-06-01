// frontend/src/lib/stores/uiStateStore.ts
import { writable } from 'svelte/store';
import type { ActiveWorkspace, ActiveMode } from '$types/models';

export const activeWorkspace = writable<ActiveWorkspace>('dashboard'); // Default to a new dashboard
export const activeMode = writable<ActiveMode>(null);

// Selections for Plan-Making
export const selectedPolicyId = writable<string | null>(null);
export const selectedPlanSiteId = writable<string | null>(null); // Renamed to avoid clash
export const selectedScenarioId = writable<string | null>(null);
export const selectedGoalId = writable<string | null>(null);
export const selectedDocumentNodeId = writable<string | null>(null);
export const selectedDocumentId = writable<string | null>(null);

// Selections for Development Management
export const selectedApplicationId = writable<string | null>(null);
export const selectedDmSiteId = writable<string | null>(null); // For ad-hoc site queries in DM
export const selectedPrecedentId = writable<string | null>(null);
export const selectedReportSectionId = writable<string | null>(null);


export function setActiveWorkspace(workspace: ActiveWorkspace, defaultMode?: ActiveMode) {
	activeWorkspace.set(workspace);
	activeMode.set(defaultMode || null); // Set a default mode for the workspace or null
	// Clear all selections when changing workspace
	selectedPolicyId.set(null);
	selectedPlanSiteId.set(null);
	selectedScenarioId.set(null);
	selectedGoalId.set(null);
	selectedDocumentNodeId.set(null);
	selectedDocumentId.set(null);
	selectedApplicationId.set(null);
	selectedDmSiteId.set(null);
	selectedPrecedentId.set(null);
	selectedReportSectionId.set(null);
}

export function setActiveModeInCurrentWorkspace(mode: ActiveMode) {
    activeMode.set(mode);
    // Optionally clear mode-specific selections
    // e.g., if switching from 'policy' to 'site-allocation', clear selectedPolicyId
}