import { writable, get } from 'svelte/store';
import type { SiteAssessmentResponse } from '$types/models';

export const planDraftStore = writable<SiteAssessmentResponse | null>(null);

export function setPlanAssessment(data: SiteAssessmentResponse) {
  planDraftStore.set(data);
}

export function usePlanAssessment() {
  return get(planDraftStore);
}
