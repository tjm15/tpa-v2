<script lang="ts">
    import { sites as allSitesStore, goals as allGoalsStore } from '$lib/stores/mainDataStore';
	import { selectedPlanSiteId } from '$lib/stores/uiStateStore';
	import type { Site, StrategicGoalAlignment, DeliverabilityMetric, SoundnessCheck } from '$types/models';
	import Card from '$lib/components/common/Card.svelte';
	import Badge from '$lib/components/common/Badge.svelte';
    import { get } from 'svelte/store';

    let currentSite: Site | null | undefined = null;

    $: {
        currentSite = $selectedPlanSiteId ? get(allSitesStore).find(s => s.id === $selectedPlanSiteId) : null;
    }

    function getSoundnessColor(status: SoundnessCheck['status']) {
        if (status === '🟢 Sound') return 'green';
        if (status === '🟡 Minor Issues') return 'yellow';
        if (status === '🔴 Major Issues') return 'red';
        return 'gray';
    }
    function getGoalAlignmentColor(alignment: StrategicGoalAlignment['alignment']) {
        if (alignment === 'Supports') return 'green';
        if (alignment === 'Partially Aligns') return 'yellow';
        if (alignment === 'Undermines') return 'red';
        return 'gray';
    }

    // Mock goals if not directly on site object
    let displayedGoals: StrategicGoalAlignment[] = [];
    $: {
        if (currentSite?.strategicGoalContributions && currentSite.strategicGoalContributions.length > 0) {
            displayedGoals = currentSite.strategicGoalContributions;
        } else if (currentSite) {
            // Mock some if none are defined for demo
            const goals = get(allGoalsStore);
            displayedGoals = goals.slice(0,2).map(g => ({
                goalId: g.id,
                goalName: g.name,
                alignment: Math.random() > 0.66 ? 'Supports' : (Math.random() > 0.33 ? 'Partially Aligns' : 'Neutral'),
                notes: "Mocked alignment for demo."
            }));
        } else {
            displayedGoals = [];
        }
    }

    // Mock deliverability if not on site object
    let displayedDeliverability: DeliverabilityMetric[] = [];
    $: {
        if (currentSite?.deliverabilityAssessment && currentSite.deliverabilityAssessment.length > 0) {
            displayedDeliverability = currentSite.deliverabilityAssessment;
        } else if (currentSite) {
            displayedDeliverability = [
                { name: 'Access to road network', score: Math.floor(Math.random()*5)+5, confidence: Math.floor(Math.random()*3)+7, rationale: "Mocked: Good existing access."},
                { name: 'Infrastructure readiness', score: Math.floor(Math.random()*4)+3, confidence: Math.floor(Math.random()*4)+5, rationale: "Mocked: Some upgrades needed."},
                { name: 'Landowner intention', score: Math.floor(Math.random()*6)+4, confidence: Math.floor(Math.random()*3)+6, rationale: "Mocked: Generally willing."},
            ];
        } else {
            displayedDeliverability = [];
        }
    }
    // Mock soundness if not on site object
    let displayedSoundness: SoundnessCheck[] = [];
     $: {
        if (currentSite?.soundnessChecksPlanMaking && currentSite.soundnessChecksPlanMaking.length > 0) {
            displayedSoundness = currentSite.soundnessChecksPlanMaking;
        } else if (currentSite) {
            displayedSoundness = [
                { criterion: 'Environmental impacts considered?', status: Math.random() > 0.5 ? '🟢 Sound' : '🟡 Minor Issues', rationale: "Mocked: EIA scope agreed."},
                { criterion: 'Sustainable development rationale?', status: Math.random() > 0.5 ? '🟢 Sound' : '🔴 Major Issues', rationale: "Mocked: Justification for greenfield needs strengthening."},
            ];
        } else {
            displayedSoundness = [];
        }
    }


</script>

<div class="p-1 md:p-2 space-y-3 overflow-y-auto h-full text-sm">
    {#if currentSite}
        <Card title="Strategic Goal Contribution">
            {#if displayedGoals.length > 0}
                <ul class="space-y-2">
                    {#each displayedGoals as goal (goal.goalId)}
                        <li class="p-2 border rounded">
                            <div class="flex justify-between items-center">
                                <span class="font-medium text-gray-700">{goal.goalName}</span>
                                <Badge text={goal.alignment} color={getGoalAlignmentColor(goal.alignment)} />
                            </div>
                            {#if goal.notes}<p class="text-xs text-gray-500 mt-1">{goal.notes}</p>{/if}
                        </li>
                    {/each}
                </ul>
            {:else}
                <p class="text-xs text-gray-500">No strategic goal contributions assessed for this site.</p>
            {/if}
        </Card>

        <Card title="Deliverability Assessment">
             {#if displayedDeliverability.length > 0}
                <dl class="space-y-2">
                    {#each displayedDeliverability as metric (metric.name)}
                        <div class="p-2 border rounded">
                            <dt class="font-medium text-gray-700">{metric.name}</dt>
                            <dd class="text-gray-600">
                                Score: {metric.score}/10 
                                {#if metric.confidence}(Confidence: {metric.confidence}/10){/if}
                            </dd>
                            {#if metric.rationale}<dd class="text-xs text-gray-500 mt-0.5">{metric.rationale}</dd>{/if}
                        </div>
                    {/each}
                </dl>
            {:else}
                <p class="text-xs text-gray-500">Deliverability not yet assessed.</p>
            {/if}
        </Card>

        <Card title="Soundness & Legal Checks">
            {#if displayedSoundness.length > 0}
                <ul class="space-y-2">
                    {#each displayedSoundness as check (check.criterion)}
                        <li class="p-2 border rounded">
                            <div class="flex justify-between items-center">
                                <span class="font-medium text-gray-700">{check.criterion}</span>
                                <Badge text={check.status} color={getSoundnessColor(check.status)} />
                            </div>
                             {#if check.rationale}<p class="text-xs text-gray-500 mt-1">{check.rationale}</p>{/if}
                        </li>
                    {/each}
                </ul>
            {:else}
                 <p class="text-xs text-gray-500">Soundness checks not yet performed.</p>
            {/if}
        </Card>
    {:else}
        <div class="flex items-center justify-center h-full p-10 text-center">
			<p class="text-gray-500">Select a site to see its deliverability and soundness assessment.</p>
		</div>
    {/if}
</div>