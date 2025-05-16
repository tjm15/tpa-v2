<script lang="ts">
  import { onMount } from 'svelte';
  import { setDmAssessment } from '$stores/dmStore';
  import { getDmMockAssessment } from '$services/dmMockData';
  import SiteContextMap from './SiteContextMap.svelte';
  import ConstraintPanel from './ConstraintPanel.svelte';
  import PolicyPanel from './PolicyPanel.svelte';
  import ReasoningPanel from './ReasoningPanel.svelte';
  import TradeOffMatrix from './TradeOffMatrix.svelte';
  // Add OfficerNotesPanel, PrecedentFinder, ExportBar as you build them

  onMount(() => {
    setDmAssessment(getDmMockAssessment());
  });
</script>

<div class="min-h-screen bg-background p-8">
  <div class="grid grid-cols-2 gap-8">
    <SiteContextMap />
    <ConstraintPanel />
    <PolicyPanel />
    <ReasoningPanel />
    <TradeOffMatrix />
    <!-- Add OfficerNotesPanel, PrecedentFinder, ExportBar here as needed -->
  </div>
</div>
