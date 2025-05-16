import type { SiteAssessmentResponse } from '$types/models';

export function getDmMockAssessment(): SiteAssessmentResponse {
  return {
    site: { id: 'dm1', name: 'Demo Manor' },
    constraints_affecting_site: [
      { constraint_node: { name: 'Flood Zone 2' } },
      { constraint_node: { name: 'Green Belt' } },
      { constraint_node: { name: 'Heritage Area' } }
    ],
    applicable_policies: [
      { policy: { title: 'Policy DM1' }, chunk_text: 'Development must respect local character.' },
      { policy: { title: 'Policy DM2' }, chunk_text: 'Flood risk must be mitigated.' },
      { policy: { title: 'Policy DM3' }, chunk_text: 'No net loss of biodiversity.' }
    ],
    ai_reasoning_output: {
      summary: 'The site is constrained by flood risk and heritage status. Policy DM2 requires a flood risk assessment. Policy DM3 may require ecological mitigation.'
    },
    trade_off_matrix: {
      matrix: [
        ['Policy DM1', 'Policy DM2', 'Policy DM3'],
        ['Compatible', 'Conflict', 'Neutral'],
        ['Conflict', 'Compatible', 'Conflict']
      ],
      notes: 'Policy DM2 and DM3 may conflict due to required land for mitigation.'
    }
  };
}
