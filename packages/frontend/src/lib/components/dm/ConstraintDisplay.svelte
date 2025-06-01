<script lang="ts">
  import Badge from '$lib/components/common/Badge.svelte';
  import type { SpatialDesignation } from '$types/models';
  export let spatialDesignation: SpatialDesignation;
</script>

<div class="rounded-lg shadow bg-white border p-4 flex flex-col gap-2">
  <div class="flex items-center gap-2">
    <span class="font-semibold text-base">{spatialDesignation.name}</span>
    {#if spatialDesignation.severity}
      <Badge text={spatialDesignation.severity} color={spatialDesignation.severity === 'High' ? 'red' : spatialDesignation.severity === 'Medium' ? 'yellow' : 'gray'} size="sm" />
    {/if}
  </div>
  <div class="text-sm text-gray-600">{spatialDesignation.type}</div>
  {#if spatialDesignation.description}
    <div class="text-gray-700 text-sm mt-1">{spatialDesignation.description}</div>
  {/if}
</div>
