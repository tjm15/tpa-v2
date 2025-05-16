import { writable, get } from 'svelte/store';
import type { SiteAssessmentResponse } from '$types/models';

export const dmAssessmentStore = writable<SiteAssessmentResponse | null>(null);

export function setDmAssessment(data: SiteAssessmentResponse) {
  dmAssessmentStore.set(data);
}

export function useDmAssessment() {
  return get(dmAssessmentStore);
}
