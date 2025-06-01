<script lang="ts">
  import Badge from '$lib/components/common/Badge.svelte';
  import type { Policy } from '$types/models';
  export let policy: Policy;

  function getStatusColor(status: string) {
    switch (status) {
      case 'Active':
        return 'green';
      case 'Superseded':
        return 'gray';
      case 'Draft':
        return 'yellow';
      default:
        return 'blue';
    }
  }
</script>

<div class="rounded-lg shadow bg-white border p-4 flex flex-col gap-2">
  <div class="flex items-center gap-2">
    <span class="font-semibold text-base">
      {policy.reference}{policy.title ? `: ${policy.title}` : ''}
    </span>
    {#if policy.status}
      <Badge text={policy.status} color={getStatusColor(policy.status)} size="sm" />
    {/if}
  </div>
  {#if policy.requirementsSummary}
    <div class="text-gray-700 text-sm mt-1">{policy.requirementsSummary}</div>
  {/if}
  {#if policy.wording}
    <details class="mt-2">
      <summary class="cursor-pointer text-xs text-blue-600">Show full wording</summary>
      <div class="text-xs text-gray-700 whitespace-pre-line mt-1">{policy.wording}</div>
    </details>
  {/if}
</div>
