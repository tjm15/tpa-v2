<script lang="ts">
	import {
		goals as allGoalsStore,
		policies as allPoliciesStore,
		sites as allSitesStore,
        scenarios as allScenariosStore
	} from '$lib/stores/mainDataStore';
	import { selectedGoalId } from '$lib/stores/uiStateStore';
	import type { Goal, Policy, Site, Scenario } from '$types/models';
	import Card from '$lib/components/common/Card.svelte';
	import Badge from '$lib/components/common/Badge.svelte';
	import { get } from 'svelte/store';

	let currentGoal: Goal | null | undefined = null;
    let contributingPolicies: Policy[] = [];
    let contributingSites: Site[] = [];
    let scenarioComparisons: { scenarioName: string; status: Goal['status']; value: string | number }[] = [];

	$: {
		if ($selectedGoalId) {
			currentGoal = get(allGoalsStore).find(g => g.id === $selectedGoalId);
            if (currentGoal) {
                contributingPolicies = (currentGoal.contributingPolicyIds || [])
                    .map(pid => get(allPoliciesStore).find(p => p.id === pid))
                    .filter(p => p) as Policy[];
                
                contributingSites = (currentGoal.contributingSiteIds || [])
                    .map(sid => get(allSitesStore).find(s => s.id === sid))
                    .filter(s => s) as Site[];

                // Mock scenario comparisons for this goal
                scenarioComparisons = get(allScenariosStore).map(scen => {
                    const perf = scen.goalPerformance?.find(gp => gp.goalId === currentGoal?.id);
                    return {
                        scenarioName: scen.name,
                        status: perf?.status || 'Not Started',
                        value: perf?.value || 'N/A'
                    };
                }).slice(0, 3); // Show for a few scenarios
            }
		} else {
			currentGoal = null;
            contributingPolicies = [];
            contributingSites = [];
            scenarioComparisons = [];
		}
	}
    function getGoalStatusColor(status: Goal['status']) {
        // (Same as in GoalListNavigator, could be a shared util)
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
</script>

<div class="p-4 md:p-6 h-full flex flex-col space-y-4 overflow-y-auto">
	{#if currentGoal}
		<Card>
            <svelte:fragment slot="title">
                <div class="flex justify-between items-center">
                    <h2 class="text-xl font-bold text-gray-800">{currentGoal.name}</h2>
                    <Badge text={currentGoal.status} color={getGoalStatusColor(currentGoal.status)} />
                </div>
            </svelte:fragment>
            <div class="space-y-3 text-sm">
                <p><strong class="text-gray-600">Category:</strong> {currentGoal.category}</p>
                <p><strong class="text-gray-600">Target:</strong> {currentGoal.targetMetric}</p>
                {#if currentGoal.targetValue !== undefined}
                    <p><strong class="text-gray-600">Target Value:</strong> {currentGoal.targetValue} {currentGoal.unit || ''}</p>
                {/if}
                {#if currentGoal.currentValue !== undefined}
                     <p><strong class="text-gray-600">Current Value:</strong> {currentGoal.currentValue} {currentGoal.unit || ''}</p>
                {/if}
                <p><strong class="text-gray-600">Source:</strong> {currentGoal.source || 'N/A'}</p>
                {#if currentGoal.description}
                    <p class="text-gray-600 bg-gray-50 p-2 rounded border">{currentGoal.description}</p>
                {/if}
            </div>
        </Card>

        <Card title="Contributing Policies ({contributingPolicies.length})" titleClasses="text-md font-semibold" additionalClasses="text-sm">
            {#if contributingPolicies.length > 0}
                <ul class="space-y-1 max-h-48 overflow-y-auto">
                    {#each contributingPolicies as policy (policy.id)}
                        <li class="p-1.5 border-b last:border-b-0 hover:bg-gray-50">
                           <span class="font-medium text-blue-600">{policy.reference}</span> - {policy.title} 
                           <Badge text={policy.status} color={policy.status === 'Adopted' ? 'green' : 'gray'} size="sm" additionalClasses="ml-2"/>
                        </li>
                    {/each}
                </ul>
            {:else}
                <p class="text-xs text-gray-500">No policies directly linked as contributing to this goal.</p>
            {/if}
        </Card>
        
        <Card title="Contributing Sites ({contributingSites.length})" titleClasses="text-md font-semibold" additionalClasses="text-sm">
            {#if contributingSites.length > 0}
                 <ul class="space-y-1 max-h-48 overflow-y-auto">
                    {#each contributingSites as site (site.id)}
                        <li class="p-1.5 border-b last:border-b-0 hover:bg-gray-50">
                           <span class="font-medium text-indigo-600">{site.name || site.id}</span>
                           {#if site.proposedUsePlanMaking}({site.proposedUsePlanMaking}){/if}
                           </li>
                    {/each}
                </ul>
            {:else}
                <p class="text-xs text-gray-500">No sites directly linked as contributing to this goal.</p>
            {/if}
        </Card>

        <Card title="Scenario Comparisons" titleClasses="text-md font-semibold" additionalClasses="text-sm">
            {#if scenarioComparisons.length > 0}
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Scenario</th>
                            <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                            <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Value</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        {#each scenarioComparisons as comp (comp.scenarioName)}
                            <tr>
                                <td class="px-3 py-2 whitespace-nowrap text-xs font-medium text-gray-900">{comp.scenarioName}</td>
                                <td class="px-3 py-2 whitespace-nowrap text-xs">
                                    <Badge text={comp.status} color={getGoalStatusColor(comp.status)} size="sm"/>
                                </td>
                                <td class="px-3 py-2 whitespace-nowrap text-xs text-gray-500">{comp.value}</td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            {:else}
                <p class="text-xs text-gray-500">No scenario performance data available for this goal.</p>
            {/if}
        </Card>
        
        {#if currentGoal.risks && currentGoal.risks.length > 0}
        <Card title="AI-Detected Risks / Notes" titleClasses="text-md font-semibold" additionalClasses="text-sm">
            <ul class="list-disc list-inside text-xs text-yellow-700 space-y-1">
                {#each currentGoal.risks as risk}
                    <li>{risk}</li>
                {/each}
            </ul>
        </Card>
        {/if}

	{:else}
		<div class="flex items-center justify-center h-full">
			<p class="text-gray-500 p-10 text-center">Select a strategic goal from the navigator to view its details, contributing elements, and performance.</p>
		</div>
	{/if}
</div>