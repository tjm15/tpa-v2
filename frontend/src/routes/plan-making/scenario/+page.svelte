<script lang="ts">
	import ThreeZoneLayout from '$lib/components/layouts/ThreeZoneLayout.svelte';
	import ScenarioSwitcher from '$lib/components/scenario/ScenarioSwitcher.svelte';
	import ScenarioDashboard from '$lib/components/scenario/ScenarioDashboard.svelte';
	import ScenarioGoalEvaluationPanel from '$lib/components/scenario/ScenarioGoalEvaluationPanel.svelte';
</script>

<ThreeZoneLayout>
	<div slot="left-sidebar" class="h-full">
		<ScenarioSwitcher />
	</div>
	<div slot="central-panel" class="h-full bg-slate-50">
		<ScenarioDashboard />
	</div>
	<div slot="right-sidebar" class="h-full bg-slate-50">
		<ScenarioGoalEvaluationPanel />
	</div>
</ThreeZoneLayout>
