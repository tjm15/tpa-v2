<script lang="ts">
	import { sites as allSitesStore, constraints as allConstraintsStore } from '$lib/stores/mainDataStore';
	import { selectedPlanSiteId } from '$lib/stores/uiStateStore';
	import type { Site, Constraint } from '$types/models';
	import MapDisplay from '$lib/components/shared/MapDisplay.svelte';
	import Card from '$lib/components/common/Card.svelte';
	import PolicyRequirementsTab from './PolicyRequirementsTab.svelte';
	import AllocationDraftTab from './AllocationDraftTab.svelte';
	import { get } from 'svelte/store';

	let currentSite: Site | null | undefined = null;
    let siteConstraints: Constraint[] = [];
    let activeTab: 'policy' | 'draft' = 'policy';

	$: {
		if ($selectedPlanSiteId) {
			currentSite = get(allSitesStore).find(s => s.id === $selectedPlanSiteId);
            // Filter constraints relevant to the site (mock logic, real app might fetch this or have direct links)
            siteConstraints = currentSite?.constraints || get(allConstraintsStore).slice(0,2); // Example: show first 2 global constraints if site has none
		} else {
			currentSite = null;
            siteConstraints = [];
		}
	}
</script>

<div class="p-1 md:p-2 h-full flex flex-col">
	{#if currentSite}
		<div class="flex-shrink-0 mb-1 md:mb-2">
            <Card additionalClasses="overflow-hidden">
                <svelte:fragment slot="title">
                    <div class="flex justify-between items-center">
                        <h2 class="text-xl font-bold text-gray-800">{currentSite.name || currentSite.address || `Site ID: ${currentSite.id}`}</h2>
                        </div>
                </svelte:fragment>
                 <div class="text-xs text-gray-600 px-4 pb-2 grid grid-cols-2 gap-x-4">
                    <span><strong>Area:</strong> {currentSite.areaHa ? `${currentSite.areaHa} ha` : 'N/A'}</span>
                    <span><strong>UPRN:</strong> {currentSite.uprn || 'N/A'}</span>
                    <span><strong>Parish:</strong> {currentSite.parish || 'N/A'}</span>
                    <span><strong>Source:</strong> {currentSite.source || 'N/A'}</span>
                </div>
            </Card>
        </div>

		<div class="h-1/2 min-h-[300px] flex-shrink-0 mb-1 md:mb-2">
			<MapDisplay site={currentSite} constraintsToDisplay={siteConstraints} />
		</div>

		<div class="flex-1 min-h-0 flex flex-col">
            <Card additionalClasses="h-full flex flex-col" noBodyPadding>
                <div class="flex border-b border-gray-200">
                    <button class="px-4 py-2 text-sm font-medium focus:outline-none focus:bg-gray-100" class:font-bold={activeTab === 'policy'} on:click={() => activeTab = 'policy'}>Policy Requirements</button>
                    <button class="px-4 py-2 text-sm font-medium focus:outline-none focus:bg-gray-100" class:font-bold={activeTab === 'draft'} on:click={() => activeTab = 'draft'}>Allocation Draft</button>
                </div>
                <div class="flex-1 overflow-y-auto min-h-0">
                    {#if activeTab === 'policy'}
                        <PolicyRequirementsTab site={currentSite} />
                    {:else}
                        <AllocationDraftTab site={currentSite} />
                    {/if}
                </div>
            </Card>
        </div>
	{:else}
		<div class="flex-1 flex items-center justify-center text-gray-400">
			<p>Select a site to view details.</p>
		</div>
	{/if}
</div>