<script lang="ts">
	import ThreeZoneLayout from '$lib/components/layouts/ThreeZoneLayout.svelte';
	import GoalListNavigator from '$lib/components/goal/GoalListNavigator.svelte';
	import GoalDetailView from '$lib/components/goal/GoalDetailView.svelte';
	import GoalCrossCuttingInsightsPanel from '$lib/components/goal/GoalCrossCuttingInsightsPanel.svelte';
</script>

<div class="h-full flex flex-col">
    <ThreeZoneLayout>
        <div slot="left-sidebar" class="h-full">
            <GoalListNavigator />
        </div>
        <div slot="central-panel" class="h-full bg-slate-50">
            <GoalDetailView />
        </div>
        <div slot="right-sidebar" class="h-full bg-slate-50">
            <GoalCrossCuttingInsightsPanel />
        </div>
    </ThreeZoneLayout>
</div>
