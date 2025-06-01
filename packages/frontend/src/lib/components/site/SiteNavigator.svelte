<script lang="ts">
	import { sites as allSitesStore } from '$lib/stores/mainDataStore';
	import { selectedPlanSiteId } from '$lib/stores/uiStateStore';
	import type { Site } from '$types/models';
	import SearchFilterInput from '$lib/components/common/SearchFilterInput.svelte';
	import Badge from '$lib/components/common/Badge.svelte';
	import { get } from 'svelte/store';

	let searchTermLocal: string = '';

	// Reactive statement for filteredSites
	let filteredSites: Site[] = [];
	$: {
		const $allSites = get(allSitesStore); // Get current value of the store
		
		if (!searchTermLocal.trim()) {
			filteredSites = $allSites.filter(s => s.planMakingStatus); // Only show sites relevant to plan-making
		} else {
			const lowerSearchTerm = searchTermLocal.toLowerCase();
			filteredSites = $allSites.filter(
				(site) =>
                    s.planMakingStatus && // Ensure it's a plan-making site
					(site.name?.toLowerCase().includes(lowerSearchTerm) ||
                    site.id.toLowerCase().includes(lowerSearchTerm) ||
					site.address?.toLowerCase().includes(lowerSearchTerm) ||
                    site.proposedUsePlanMaking?.toLowerCase().includes(lowerSearchTerm))
			);
		}
	}

    let totalPlanMakingSites = 0;
    $: {
        totalPlanMakingSites = get(allSitesStore).filter(s => s.planMakingStatus).length;
    }

	function selectSite(siteId: string) {
		selectedPlanSiteId.set(siteId);
	}
</script>

<div class="flex flex-col h-full">
	<div class="p-4 border-b border-gray-200">
		<h2 class="text-lg font-semibold text-gray-800">Site Navigator (Plan-Making)</h2>
		</div>
	<SearchFilterInput bind:value={searchTermLocal} placeholder="Search sites (name, ref, use...)" label="Search sites for allocation" />

	<div class="flex-1 overflow-y-auto">
		{#if filteredSites.length === 0}
			<p class="p-4 text-sm text-gray-500">
                No sites found{searchTermLocal ? ' for "' + searchTermLocal + '"' : ''}.
            </p>
		{:else}
			<ul role="listbox" aria-label="Candidate Sites" class="focus:outline-none">
				{#each filteredSites as site (site.id)}
					<li
                        id="site-option-{site.id}"
						class="border-b border-gray-200 hover:bg-gray-50 focus-within:bg-gray-100 cursor-pointer {$selectedPlanSiteId === site.id ? 'bg-indigo-50 border-l-4 border-indigo-500' : 'border-l-4 border-transparent'}"
                        role="option"
						tabindex="0"
						aria-selected={$selectedPlanSiteId === site.id}
						on:click={() => selectSite(site.id)}
						on:keydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectSite(site.id); }}}
                        aria-label="Select site {site.name || site.address || site.id}"
					>
						<div class="p-3">
							<h3 class="text-sm font-semibold text-indigo-600">{site.name || site.address || `Site Ref: ${site.id}`}</h3>
                            <p class="text-xs text-gray-500 truncate">
                                {site.proposedUsePlanMaking || 'Use not specified'} - {site.areaHa ? site.areaHa + ' ha' : 'Area not specified'}
                            </p>
							<div class="mt-1 flex space-x-2">
                                {#if site.planMakingStatus}
								    <Badge text={site.planMakingStatus} color="purple" />
                                {/if}
                                {#if site.source}
                                    <Badge text={site.source} color="blue" />
                                {/if}
							</div>
						</div>
					</li>
				{/each}
			</ul>
		{/if}
	</div>
	<div class="p-2 border-t border-gray-200 text-xs text-gray-500">
		Displaying {filteredSites.length} of {totalPlanMakingSites} plan-making sites.
	</div>
</div>