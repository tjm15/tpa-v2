<script lang="ts">
  import Badge from '$lib/components/common/Badge.svelte';
  import type { PrecedentCase } from '$types/models';
  export let precedent: PrecedentCase;
</script>

<div class="rounded-lg shadow bg-white border p-4 flex flex-col gap-2 cursor-pointer hover:shadow-md transition">
  <div class="flex items-center gap-2">
    <span class="font-semibold text-base">{precedent.caseReference}</span>
    <Badge text={precedent.outcome} color={precedent.outcome === 'Allowed' ? 'green' : precedent.outcome === 'Dismissed' ? 'red' : 'gray'} size="sm" />
  </div>
  <div class="text-xs text-gray-500">{precedent.address}</div>
  <div class="text-xs text-gray-500">{precedent.decisionType} &middot; {precedent.decisionDate}</div>
  {#if precedent.keyPoliciesCited && precedent.keyPoliciesCited.length > 0}
    <div class="text-xs text-gray-500">Policies: {precedent.keyPoliciesCited.join(', ')}</div>
  {/if}
  {#if precedent.relevanceSummary}
    <div class="text-gray-700 text-sm mt-1">{precedent.relevanceSummary}</div>
  {/if}
  {#if precedent.inspectorReasoningSummary}
    <details class="mt-2">
      <summary class="cursor-pointer text-xs text-blue-600">Inspector Reasoning</summary>
      <div class="text-xs text-gray-700 whitespace-pre-line mt-1">{precedent.inspectorReasoningSummary}</div>
    </details>
  {/if}
  {#if precedent.similarityCriteria?.site || (precedent.similarityCriteria?.policyOverlap && precedent.similarityCriteria.policyOverlap.length > 0)}
    <div class="text-xs text-gray-500 mt-1">
      {#if precedent.similarityCriteria.site}
        <div>Similarity: {precedent.similarityCriteria.site}</div>
      {/if}
      {#if precedent.similarityCriteria.policyOverlap && precedent.similarityCriteria.policyOverlap.length > 0}
        <div>Policy Overlap: {precedent.similarityCriteria.policyOverlap.join(', ')}</div>
      {/if}
    </div>
  {/if}
  {#if precedent.decisionExtractLink}
    <a class="text-xs text-blue-600 underline mt-1" href={precedent.decisionExtractLink} target="_blank" rel="noopener">Full Decision</a>
  {/if}
</div>
