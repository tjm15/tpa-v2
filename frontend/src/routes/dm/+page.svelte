<!-- src/routes/dm/+page.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';
  import { setStoreAssessment, useAssessment } from '$stores/appStore';
  import MapPanel from './SiteContextMap.svelte';
  import ConstraintPanel from './ConstraintPanel.svelte';
  import PolicyPanel from './PolicyPanel.svelte';
  import ReasoningPanel from './ReasoningPanel.svelte';
  import TradeOffMatrix from './TradeOffMatrix.svelte';
  onMount(() => {
    const data = getMockAssessment();
    setStoreAssessment(data);
  });
</script>
<style>
  .grid { display: grid; grid-template-columns: 1.5fr 1fr; grid-template-rows: auto auto 1fr; gap: 1rem; padding: 1rem; }
</style>
<div class="grid">
  <MapPanel {useAssessment} />
  <ConstraintPanel {useAssessment} />
  <PolicyPanel {useAssessment} />
  <ReasoningPanel {useAssessment} />
  <TradeOffMatrix {useAssessment} />
</div>
