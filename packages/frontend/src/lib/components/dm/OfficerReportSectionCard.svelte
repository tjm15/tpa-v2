<script lang="ts">
  import type { OfficerReportSection } from '$types/models';
  export let section: OfficerReportSection;
</script>

<div class="rounded-lg shadow bg-white border p-4 flex flex-col gap-2">
  <div class="flex items-center gap-2">
    <span class="font-semibold text-base">{section.title}</span>
    <span class="ml-2 text-xs text-gray-400">Order: {section.order}</span>
  </div>
  {#if section.content}
    <details class="mt-2">
      <summary class="cursor-pointer text-xs text-blue-600">Show content</summary>
      <div class="text-xs text-gray-700 whitespace-pre-line mt-1">{section.content}</div>
    </details>
  {/if}
</div>
