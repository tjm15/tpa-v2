<script lang="ts">
  import Badge from '$lib/components/common/Badge.svelte';
  import type { Constraint } from '$types/models';
  export let constraint: Constraint;
</script>

<div class="rounded-lg shadow bg-white border p-4 flex flex-col gap-2">
  <div class="flex items-center gap-2">
    <span class="font-semibold text-base">{constraint.name}</span>
    {#if constraint.severity}
      <Badge text={constraint.severity} color={constraint.severity === 'High' ? 'red' : constraint.severity === 'Medium' ? 'yellow' : 'gray'} size="sm" />
    {/if}
  </div>
  <div class="text-sm text-gray-600">{constraint.type}</div>
  {#if constraint.description}
    <div class="text-gray-700 text-sm mt-1">{constraint.description}</div>
  {/if}
</div>
