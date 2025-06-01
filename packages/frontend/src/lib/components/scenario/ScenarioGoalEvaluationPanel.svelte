<script lang="ts">
	import { scenarios as allScenariosStore, goals as allGoalsStore } from '$lib/stores/mainDataStore';
	import { selectedScenarioId } from '$lib/stores/uiStateStore';
	import type { Scenario, Goal, SoundnessCheck, GoalStatus } from '$types/models';
	import Card from '$lib/components/common/Card.svelte';
	import Badge from '$lib/components/common/Badge.svelte';
	import { get } from 'svelte/store';

	let currentScenario: Scenario | null | undefined = null;

	$: {
		currentScenario = $selectedScenarioId ? get(allScenariosStore).find(s => s.id === $selectedScenarioId) : null;
	}

    interface DisplayGoalPerformance {
        goalId: string;
        goalName: string;
        status: GoalStatus;
        value: number | string;
        target?: string;
    }

    let goalPerformances: DisplayGoalPerformance[] = [];
    $: {
        if (currentScenario?.goalPerformance) {
            const allGoals = get(allGoalsStore);
            goalPerformances = currentScenario.goalPerformance.map(gp => {
                const goalDetails = allGoals.find(g => g.id === gp.goalId);
                return {
                    ...gp,
                    goalName: goalDetails?.name || gp.goalId,
                    target: goalDetails?.targetMetric
                };
            });
        } else {
            goalPerformances = [];
        }
    }

    function getGoalStatusColor(status: GoalStatus) {
        switch(status) {
            case 'Achieved':
            case 'On Track': return 'green';
            case 'Partial': return 'yellow';
            case 'Failing': return 'red';
            case 'Not Started':
            case 'Superseded':
            default: return 'gray';
        }
    }

    function getSoundnessColor(status: SoundnessCheck['status']) {
        if (status === '🟢 Sound') return 'green';
        if (status === '🟡 Minor Issues') return 'yellow';
        if (status === '🔴 Major Issues') return 'red';
        return 'gray';
    }

    let soundnessFlagsToDisplay: SoundnessCheck[] = [];
    $: {
        soundnessFlagsToDisplay = currentScenario?.soundnessFlags || [
            // Mock if none
            { criterion: "Housing supply vs need", status: Math.random() > 0.5 ? '🟢 Sound' : '🟡 Minor Issues', rationale: "Mock: Meets 90% of calculated need."},
            { criterion: "Employment land strategy", status: '🟡 Minor Issues', rationale: "Mock: Slight undersupply in specialist sectors."},
            { criterion: "SEA compliance", status: '🟢 Sound', rationale: "Mock: All SEA objectives considered."}
        ];
    }
</script>

<div class="p-1 md:p-2 space-y-3 overflow-y-auto h-full text-sm">
    {#if currentScenario}
        <Card title="Goal Evaluation">
            {#if goalPerformances.length > 0}
                <ul class="space-y-2">
                    {#each goalPerformances as perf (perf.goalId)}
                        <li class="p-2 border rounded-md">
                            <div class="flex justify-between items-center">
                                <span class="font-medium text-gray-700">{perf.goalName}</span>
                                <Badge text={perf.status} color={getGoalStatusColor(perf.status)} />
                            </div>
                            <p class="text-xs text-gray-500 mt-0.5">Value: {perf.value}</p>
                            {#if perf.target}
                                <p class="text-xs text-gray-500">Target: {perf.target}</p>
                            {/if}
                        </li>
                    {/each}
                </ul>
            {:else}
                <p class="text-xs text-gray-500">Goal performance data not available for this scenario.</p>
            {/if}
        </Card>

        <Card title="Soundness Flags">
            {#if soundnessFlagsToDisplay.length > 0}
                <ul class="space-y-2">
                    {#each soundnessFlagsToDisplay as flag (flag.criterion)}
                         <li class="p-2 border rounded-md">
                            <div class="flex justify-between items-center">
                                <span class="font-medium text-gray-700">{flag.criterion}</span>
                                <Badge text={flag.status} color={getSoundnessColor(flag.status)} />
                            </div>
                            {#if flag.rationale}<p class="text-xs text-gray-500 mt-1">{flag.rationale}</p>{/if}
                        </li>
                    {/each}
                </ul>
            {:else}
                <p class="text-xs text-gray-500">No soundness flags identified for this scenario.</p>
            {/if}
        </Card>

        {#if currentScenario.aiCommentary}
        <Card title="AI Commentary">
            <p class="text-xs text-gray-600 whitespace-pre-wrap">{currentScenario.aiCommentary}</p>
        </Card>
        {/if}
    {:else}
        <div class="flex items-center justify-center h-full p-10 text-center">
			<p class="text-gray-500">Select a scenario to see its goal evaluation and risks.</p>
		</div>
    {/if}
</div>