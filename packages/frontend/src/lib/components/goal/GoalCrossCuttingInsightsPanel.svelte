<script lang="ts">
    import { goals as allGoalsStore } from '$lib/stores/mainDataStore';
    import { selectedGoalId } from '$lib/stores/uiStateStore'; // Corrected if it moved
	import type { Goal } from '$types/models';
	import Card from '$lib/components/common/Card.svelte';
	import Button from '$lib/components/common/Button.svelte';
	import { get } from 'svelte/store';

	let currentGoal: Goal | null | undefined = null;
    let relatedGoals: Goal[] = [];

	$: {
		if ($selectedGoalId) {
			currentGoal = get(allGoalsStore).find(g => g.id === $selectedGoalId);
            if (currentGoal) {
                relatedGoals = (currentGoal.relatedGoalIds || [])
                    .map(gid => get(allGoalsStore).find(g => g.id === gid))
                    .filter(g => g) as Goal[];
                
                // Mock some if none
                if (relatedGoals.length === 0 && get(allGoalsStore).length > 1) {
                    relatedGoals = get(allGoalsStore).filter(g => g.id !== currentGoal?.id).slice(0,2);
                }
            }
		} else {
			currentGoal = null;
            relatedGoals = [];
		}
	}

    function selectRelatedGoal(goalId: string) {
        selectedGoalId.set(goalId); // Navigate within Goal Tracker mode
    }

    function exportSummary() {
        if (!currentGoal) return;
        const summary = `
Goal: ${currentGoal.name}
Status: ${currentGoal.status}
Target: ${currentGoal.targetMetric}
Current Value: ${currentGoal.currentValue || 'N/A'} ${currentGoal.unit || ''}
Contributing Policies: ${currentGoal.contributingPolicyIds?.length || 0}
Contributing Sites: ${currentGoal.contributingSiteIds?.length || 0}
        `;
        // In a real app, trigger a download or copy to clipboard
        alert("Export Summary (mock):\n" + summary.trim());
        console.log(summary.trim());
    }
</script>

<div class="p-1 md:p-2 space-y-3 overflow-y-auto h-full text-sm">
    {#if currentGoal}
        <Card title="Related Goals">
            {#if relatedGoals.length > 0}
                <ul class="space-y-1">
                    {#each relatedGoals as rGoal (rGoal.id)}
                        <li class="p-1.5 border rounded-md hover:bg-gray-50">
                            <div class="flex justify-between items-center">
                                <span class="font-medium text-gray-700">{rGoal.name}</span>
                                <Button size="sm" variant="ghost" on:click={() => selectRelatedGoal(rGoal.id)}>View</Button>
                            </div>
                            <p class="text-xs text-gray-500">{rGoal.category}</p>
                        </li>
                    {/each}
                </ul>
            {:else}
                <p class="text-xs text-gray-500">No directly related goals identified.</p>
            {/if}
            </Card>

        <Card title="Potential Risks / Dependencies">
            {#if currentGoal.risks && currentGoal.risks.length > 0}
                 <ul class="list-disc list-inside text-xs text-yellow-700 space-y-1">
                    {#each currentGoal.risks as risk}
                        <li>{risk}</li>
                    {/each}
                </ul>
            {:else if currentGoal}
                <p class="text-xs text-gray-500">Example Risk: "Delivery of affordable housing goal ({currentGoal.name}) is dependent on site viability assessments which are currently unfavorable for 3 key sites."</p>
                <p class="text-xs text-gray-500 mt-1">Example Dependency: "This goal's success is tied to the timely completion of infrastructure upgrades outlined in Goal INFRA-1."</p>
            {:else}
                <p class="text-xs text-gray-500">No specific risks or dependencies noted for this goal.</p>
            {/if}
        </Card>

        <Card title="Export">
            <p class="text-xs text-gray-600 mb-2">
                Generate a summary of this goal's status and contributions.
            </p>
            <Button on:click={exportSummary} fullWidth>Export Goal Summary (Mock)</Button>
        </Card>
    {:else}
         <div class="flex items-center justify-center h-full p-10 text-center">
			<p class="text-gray-500">Select a goal to see cross-cutting insights.</p>
		</div>
    {/if}
</div>