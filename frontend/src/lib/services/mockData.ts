// src/lib/services/mockData.ts
import type { SiteAssessmentResponse } from '$types/models';

export function getMockAssessment(): SiteAssessmentResponse {
  return {
    site: { id: 's1', name: 'Mock Site' },
    constraints_affecting_site: [{ constraint_node: { name: 'Flood Zone 3' } }],
    applicable_policies: [{ policy: { title: 'Policy H1' }, chunk_text: 'Housing policy text' }],
    ai_reasoning_output: { summary: 'Mock reasoning summary' },
    trade_off_matrix: null
  };
}
