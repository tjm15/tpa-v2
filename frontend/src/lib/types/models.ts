// src/lib/types/models.ts
export type SiteNode = { id: string; name: string };
export type ConstraintOverlayData = { constraint_node: { name: string }};
export type PolicyChunkData = { policy: { title: string }; chunk_text: string };
export type ReasoningOutputData = { summary: string };
export type TradeOffMatrixData = any;

export interface SiteAssessmentResponse {
  site: SiteNode;
  constraints_affecting_site: ConstraintOverlayData[];
  applicable_policies: PolicyChunkData[];
  ai_reasoning_output: ReasoningOutputData;
  trade_off_matrix: TradeOffMatrixData | null;
}
