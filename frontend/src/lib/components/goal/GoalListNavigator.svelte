<script lang="ts">
	import { goals as allGoalsStore, policies as allPoliciesStore, sites as allSitesStore } from '$lib/stores/mainDataStore';
	import { selectedGoalId } from '$lib/stores/uiStateStore';
	import type { Goal, GoalStatus } from '$types/models';
	import SearchFilterInput from '$lib/components/common/SearchFilterInput.svelte';
	import Badge from '$lib/components/common/Badge.svelte';
	import { get } from 'svelte/store';

	let searchTermLocal: string = '';
    let filterCategory: string = 'All';
    let filterStatus: GoalStatus | 'All' = 'All';

    let categories: string[] = [];
    let statuses: GoalStatus[] = ['On Track', 'Partial', 'Failing', 'Not Started', 'Achieved', 'Superseded'];


	let filteredGoals: Goal[] = [];
	$: {
		const $allGoals = get(allGoalsStore);
        categories = ['All', ...new Set($allGoals.map(g => g.category).filter(Boolean))];
        
		let goalsToFilter = $allGoals;

        if (filterCategory !== 'All') {
            goalsToFilter = goalsToFilter.filter(g => g.category === filterCategory);
        }
        if (filterStatus !== 'All') {
            goalsToFilter = goalsToFilter.filter(g => g.status === filterStatus);
        }

		if (!searchTermLocal.trim()) {
			filteredGoals = goalsToFilter;
		} else {
			const lowerSearchTerm = searchTermLocal.toLowerCase();
			filteredGoals = goalsToFilter.filter(
				(goal) =>
					goal.name.toLowerCase().includes(lowerSearchTerm) ||
					goal.description?.toLowerCase().includes(lowerSearchTerm) ||
                    goal.targetMetric.toLowerCase().includes(lowerSearchTerm)
			);
		}
	}

    let totalGoals = 0;
    $: totalGoals = get(allGoalsStore).length;

	function selectGoal(goalId: string) {
		selectedGoalId.set(goalId);
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
</script>

<div class="flex flex-col h-full">
	<div class="p-4 border-b border-gray-200">
		<h2 class="text-lg font-semibold text-gray-800">Goal Tracker</h2>
        <div class="grid grid-cols-2 gap-2 mt-2 text-sm">
            <div>
                <label for="goal-category-filter" class="block text-xs font-medium text-gray-600 mb-0.5">Category:</label>
                <select id="goal-category-filter" bind:value={filterCategory} class="w-full p-1.5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 text-xs">
                    {#each categories as category (category)}
                        <option value={category}>{category}</option>
                    {/each}
                </select>
            </div>
            <div>
                <label for="goal-status-filter" class="block text-xs font-medium text-gray-600 mb-0.5">Status:</label>
                <select id="goal-status-filter" bind:value={filterStatus} class="w-full p-1.5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 text-xs">
                    <option value="All">All Statuses</option>
                    {#each statuses as status (status)}
                        <option value={status}>{status}</option>
                    {/each}
                </select>
            </div>
        </div>
	</div>
	<SearchFilterInput bind:value={searchTermLocal} placeholder="Search goals..." label="Search strategic goals" />

	<div class="flex-1 overflow-y-auto">
		{#if filteredGoals.length === 0}
			<p class="p-4 text-sm text-gray-500">
                No goals found{searchTermLocal || filterCategory !== 'All' || filterStatus !== 'All' ? ' for current filters.' : '.'}
            </p>
		{:else}
			<ul role="listbox" aria-label="Strategic Goals" class="focus:outline-none">
				{#each filteredGoals as goal (goal.id)}
					<li
                        id="goal-option-{goal.id}"
						class="border-b border-gray-200 hover:bg-gray-50 focus-within:bg-gray-100 cursor-pointer {$selectedGoalId === goal.id ? 'bg-purple-50 border-l-4 border-purple-500' : 'border-l-4 border-transparent'}"
                        role="option"
						tabindex="0"
						aria-selected={$selectedGoalId === goal.id}
						on:click={() => selectGoal(goal.id)}
						on:keydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectGoal(goal.id); }}}
					>
						<div class="p-3">
							<div class="flex justify-between items-start">
                                <h3 class="text-sm font-semibold text-purple-600 pr-2">{goal.name}</h3>
                                <Badge text={goal.status} color={getGoalStatusColor(goal.status)} size="sm" />
                            </div>
                            <p class="text-xs text-gray-500 mt-0.5 truncate" title={goal.targetMetric}>{goal.targetMetric}</p>
                            <p class="text-xs text-gray-400 mt-0.5">{goal.category} - {goal.type}</p>
						</div>
					</li>
				{/each}
			</ul>
		{/if}
	</div>
	<div class="p-2 border-t border-gray-200 text-xs text-gray-500">
		Displaying {filteredGoals.length} of {totalGoals} goals.
	</div>
</div>