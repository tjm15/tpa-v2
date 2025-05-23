<script lang="ts">
	import { scenarios as allScenariosStore, sites, policies, goals } from '$lib/stores/mainDataStore';
	import { selectedScenarioId } from '$lib/stores/uiStateStore';
	import type { Scenario } from '$types/models';
	import SearchFilterInput from '$lib/components/common/SearchFilterInput.svelte';
	import Button from '$lib/components/common/Button.svelte';
	import Badge from '$lib/components/common/Badge.svelte';
	import { get } from 'svelte/store';

	let searchTermLocal: string = '';

	let filteredScenarios: Scenario[] = [];
	$: {
		const $allScenarios = get(allScenariosStore);
		if (!searchTermLocal.trim()) {
			filteredScenarios = $allScenarios;
		} else {
			const lowerSearchTerm = searchTermLocal.toLowerCase();
			filteredScenarios = $allScenarios.filter(
				(scenario) =>
					scenario.name.toLowerCase().includes(lowerSearchTerm) ||
					scenario.description?.toLowerCase().includes(lowerSearchTerm)
			);
		}
	}

	function selectScenario(scenarioId: string) {
		selectedScenarioId.set(scenarioId);
	}

	function addNewScenario() {
		const newScenarioName = prompt("Enter name for new scenario:", "New Scenario " + (get(allScenariosStore).length + 1));
		if (newScenarioName) {
			const newScenario: Scenario = {
				id: `scen-${Date.now()}`,
				name: newScenarioName,
				description: "Newly created scenario",
				activePolicyIds: get(policies).map(p => p.id), // Default to all current policies
                includedSiteIds: get(sites).filter(s => s.planMakingStatus === 'Draft Allocation' || s.planMakingStatus === 'Adopted Allocation').map(s => s.id), // Default to currently allocated sites
				summaryMetrics: { totalHomes: 0, jobsEnabled: 0, riskFlags: 0 },
                goalPerformance: get(goals).map(g => ({ goalId: g.id, status: 'Not Started', value: 'N/A' })),
				createdAt: new Date().toISOString()
			};
			allScenariosStore.update(scens => [...scens, newScenario]);
			selectedScenarioId.set(newScenario.id);
		}
	}

    function duplicateScenarioHandler(event: MouseEvent, scenario: Scenario) {
        event.stopPropagation(); // Stop propagation here
        const newName = prompt("Enter name for duplicated scenario:", `${scenario.name} (Copy)`);
        if (newName && scenario) {
            const newScenarioData: Scenario = { // Renamed to avoid conflict with scenario param
                ...JSON.parse(JSON.stringify(scenario)), // Deep copy
                id: `scen-${Date.now()}`,
                name: newName,
                createdAt: new Date().toISOString(),
                baselineScenarioId: scenario.id // Link to original for diff later
            };
            allScenariosStore.update(scens => [...scens, newScenarioData]);
            selectedScenarioId.set(newScenarioData.id);
        }
    }

    function deleteScenarioHandler(event: MouseEvent, scenarioId: string, scenarioName: string) {
        event.stopPropagation(); // Stop propagation here
        if (confirm(`Are you sure you want to delete scenario: "${scenarioName}"?`)) {
            allScenariosStore.update(scens => scens.filter(s => s.id !== scenarioId));
            if (get(selectedScenarioId) === scenarioId) {
                selectedScenarioId.set(null);
            }
        }
    }

    function getGoalsMetCount(scenario: Scenario): string {
        if (!scenario.goalPerformance) return "0/0";
        const metGoals = scenario.goalPerformance.filter(gp => gp.status === 'Achieved' || gp.status === 'On Track').length;
        return `${metGoals}/${scenario.goalPerformance.length}`;
    }
</script>

<div class="flex flex-col h-full">
	<div class="p-4 border-b border-gray-200">
		<h2 class="text-lg font-semibold text-gray-800">Scenario Manager</h2>
        <Button on:click={addNewScenario} size="sm" additionalClasses="mt-2 w-full">Add New Scenario</Button>
	</div>
	<SearchFilterInput bind:value={searchTermLocal} placeholder="Search scenarios..." label="Search scenarios" />

	<div class="flex-1 overflow-y-auto">
		{#if filteredScenarios.length === 0}
			<p class="p-4 text-sm text-gray-500">
                No scenarios found{searchTermLocal ? ' for "' + searchTermLocal + '"' : ''}.
            </p>
		{:else}
			<ul role="listbox" aria-label="Available Scenarios" class="focus:outline-none">
				{#each filteredScenarios as scenario (scenario.id)}
					<li
                        id="scenario-option-{scenario.id}"
						class="border-b border-gray-200 hover:bg-gray-50 focus-within:bg-gray-100 {$selectedScenarioId === scenario.id ? 'bg-teal-50 border-l-4 border-teal-500' : 'border-l-4 border-transparent'}"
                        role="option"
						tabindex="0"
						aria-selected={$selectedScenarioId === scenario.id}
						on:click={() => selectScenario(scenario.id)}
						on:keydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectScenario(scenario.id); }}}
                        aria-label="Select scenario {scenario.name}"
					>
						<div class="p-3">
							<div class="flex justify-between items-center">
                                <h3 class="text-sm font-semibold text-teal-600 truncate" title={scenario.name}>{scenario.name}</h3>
                                <div class="flex-shrink-0 space-x-1">
									<Button size="sm" variant="ghost" on:click={(event) => duplicateScenarioHandler(event, scenario)} additionalClasses="group">
										<span title="Duplicate Scenario">📋</span>
									</Button>
									<Button size="sm" variant="ghost" on:click={(event) => deleteScenarioHandler(event, scenario.id, scenario.name)} additionalClasses="text-red-500 hover:text-red-700">
										<span title="Delete Scenario">🗑️</span>
									</Button>
                                </div>
                            </div>
                            {#if scenario.description}
                                <p class="text-xs text-gray-500 truncate mt-0.5" title={scenario.description}>{scenario.description}</p>
                            {/if}
                            <div class="mt-1.5 flex flex-wrap gap-1 text-xs">
                                <Badge text="🧱 Sites: {scenario.includedSiteIds?.length || 0}" color="blue" size="sm"/>
                                <Badge text="📘 Policies: {scenario.activePolicyIds?.length || 0}" color="purple" size="sm"/>
                                <Badge text="🎯 Goals Met: {getGoalsMetCount(scenario)}" color="green" size="sm"/>
                            </div>
						</div>
					</li>
				{/each}
			</ul>
		{/if}
	</div>
    <div class="p-2 border-t border-gray-200 text-xs text-gray-500">
		{filteredScenarios.length} scenario(s) displayed.
        </div>
</div>