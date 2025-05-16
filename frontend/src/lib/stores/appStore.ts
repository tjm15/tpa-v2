// src/lib/stores/appStore.ts
import { writable, get } from 'svelte/store';
import type { SiteAssessmentResponse } from '$types/models';

const assessment = writable<SiteAssessmentResponse | null>(null);

export function setStoreAssessment(data: SiteAssessmentResponse) {
  assessment.set(data);
}

export function useAssessment() {
  return get(assessment);
}
