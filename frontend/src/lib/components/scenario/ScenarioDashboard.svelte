<script lang="ts">
	import { scenarios as allScenariosStore, sites, policies } from '$lib/stores/mainDataStore';
	import { selectedScenarioId } from '$lib/stores/uiStateStore';
	import type { Scenario } from '$types/models';
	import Card from '$lib/components/common/Card.svelte';
	import { get } from 'svelte/store';

	let currentScenario: Scenario | null | undefined = null;

	$: {
		currentScenario = $selectedScenarioId ? get(allScenariosStore).find(s => s.id === $selectedScenarioId) : null;
	}

    // Mock trade-off matrix for display
    let tradeOffData = {
        categories: ["Housing Delivery", "Heritage Impact", "Biodiversity Net Gain", "Transport Strain"],
        values: [
            [null, "Moderate Conflict", "Minor Conflict", "High Synergy"],
            ["Moderate Conflict", null, "Neutral", "Minor Conflict"],
            ["Minor Conflict", "Neutral", null, "Neutral"],
            ["High Synergy", "Minor Conflict", "Neutral", null],
        ]
    };
</script>

<div class="flex-1 min-h-0 flex flex-col space-y-4">
	{#if currentScenario}
		<div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-5 gap-4 mb-4">
            <Card title="🏡 Homes Delivered" titleClasses="text-sm font-medium" bodyClasses="p-3 text-center">
                <p class="text-2xl font-bold text-gray-800">{currentScenario.summaryMetrics?.totalHomes || 'N/A'}</p>
            </Card>
            <Card title="💼 Jobs Enabled" titleClasses="text-sm font-medium" bodyClasses="p-3 text-center">
                <p class="text-2xl font-bold text-gray-800">{currentScenario.summaryMetrics?.jobsEnabled || 'N/A'}</p>
            </Card>
            <Card title="🏗️ Infra. Need" titleClasses="text-sm font-medium" bodyClasses="p-3 text-center">
                <p class="text-2xl font-bold text-gray-800">{currentScenario.summaryMetrics?.infrastructureNeed || 'N/A'}</p>
            </Card>
            <Card title="⚠️ Risk Flags" titleClasses="text-sm font-medium" bodyClasses="p-3 text-center">
                <p class="text-2xl font-bold text-red-600">{currentScenario.summaryMetrics?.riskFlags || 0}</p>
            </Card>
            <Card title="⚖️ Trade-Off Index" titleClasses="text-sm font-medium" bodyClasses="p-3 text-center">
                <p class="text-2xl font-bold text-blue-600">{currentScenario.summaryMetrics?.tradeOffIndex || 'N/A'}</p>
            </Card>
        </div>

        <Card title="Theme-based Trade-offs (Visual Matrix Example)">
            <div class="overflow-x-auto p-1">
                <table class="min-w-full text-xs border border-gray-200">
                    <thead>
                        <tr class="bg-gray-50">
                            <th class="p-2 border"></th>
                            {#each tradeOffData.categories as category}
                                <th class="p-2 border font-medium text-gray-600">{category}</th>
                            {/each}
                        </tr>
                    </thead>
                    <tbody>
                        {#each tradeOffData.categories as rowCategory, i}
                            <tr>
                                <td class="p-2 border font-medium text-gray-600 bg-gray-50">{rowCategory}</td>
                                {#each tradeOffData.values[i] as cellValue}
                                    <td class="p-2 border text-center {
                                        cellValue?.includes('Conflict') ? 'bg-red-50 text-red-700' :
                                        cellValue?.includes('Synergy') ? 'bg-green-50 text-green-700' :
                                        cellValue === 'Neutral' ? 'bg-yellow-50 text-yellow-700' : 'bg-white'
                                    }">
                                        {cellValue || '-'}
                                    </td>
                                {/each}
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        </Card>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card title="Sites Included/Excluded">
                <p class="text-sm text-gray-600 mb-1"><strong>Included ({currentScenario.includedSiteIds?.length || 0}):</strong></p>
                <ul class="text-xs list-disc list-inside pl-2 max-h-32 overflow-y-auto">
                    {#each currentScenario.includedSiteIds || [] as siteId}
                        <li>{get(sites).find(s=>s.id === siteId)?.name || siteId}</li>
                    {/each}
                </ul>
                 <p class="text-sm text-gray-600 mt-2 mb-1"><strong>Excluded ({currentScenario.excludedSiteIds?.length || 0}):</strong></p>
                 <ul class="text-xs list-disc list-inside pl-2 max-h-32 overflow-y-auto">
                    {#each currentScenario.excludedSiteIds || [] as siteId}
                        <li>{get(sites).find(s=>s.id === siteId)?.name || siteId}</li>
                    {/each}
                </ul>
            </Card>
            <Card title="Policy Changes">
                <p class="text-sm text-gray-600 mb-1"><strong>Active ({currentScenario.activePolicyIds?.length || 0}):</strong></p>
                 <ul class="text-xs list-disc list-inside pl-2 max-h-32 overflow-y-auto">
                    {#each currentScenario.activePolicyIds || [] as policyId}
                        <li>{get(policies).find(p=>p.id === policyId)?.reference || policyId}</li>
                    {/each}
                </ul>
                <p class="text-sm text-gray-600 mt-2 mb-1"><strong>Modified ({currentScenario.modifiedPolicies?.length || 0}):</strong></p>
                 <ul class="text-xs list-disc list-inside pl-2 max-h-32 overflow-y-auto">
                    {#each currentScenario.modifiedPolicies || [] as modPolicy}
                        <li>{get(policies).find(p=>p.id === modPolicy.policyId)?.reference}: {Object.keys(modPolicy.changes).join(', ')} changed</li>
                    {/each}
                </ul>
            </Card>
        </div>

	{:else}
		<div class="flex items-center justify-center h-full">
			<p class="text-gray-500 p-10 text-center">Select a scenario from the manager to view its dashboard.</p>
		</div>
	{/if}
</div>