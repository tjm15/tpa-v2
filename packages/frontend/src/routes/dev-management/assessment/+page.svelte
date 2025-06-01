<script lang="ts">
	// This will be the main page for Assessment Mode (DM Site Assessment)
	// Skeleton structure for DM mode, ready for further development
	import SearchFilterPanel from '$lib/components/shared/SearchFilterPanel.svelte';
	import MapDisplay from '$lib/components/shared/MapDisplay.svelte';
	import PolicyCard from '$lib/components/dm/PolicyCard.svelte';
	import SpatialDesignationDisplay from '$lib/components/dm/ConstraintDisplay.svelte';
	import { planningApplications, sites } from '$lib/stores/mainDataStore';
	import type { PlanningApplication, Site, SpatialDesignation, Policy } from '$types/models';
	import { get } from 'svelte/store';

	let allApps: PlanningApplication[] = get(planningApplications);
	let allSites: Site[] = get(sites);
	let searchItems: Array<PlanningApplication | Site> = [...allApps, ...allSites];

	let selected: PlanningApplication | Site | null = null;
	let currentSite: Site | null = null;
	let currentApp: PlanningApplication | null = null;
	let siteSpatialDesignations: SpatialDesignation[] = [];
	let applicablePolicies: Policy[] = [];

	function handleItemSelected(event: CustomEvent) {
		selected = event.detail.item;
		if (selected && 'referenceNumber' in selected) {
			currentApp = selected as PlanningApplication;
			currentSite = allSites.find(s => s.id === currentApp?.siteId) || null;
		} else if (selected) {
			currentSite = selected as Site;
			currentApp = null;
		} else {
			currentSite = null;
			currentApp = null;
		}
		siteSpatialDesignations = currentApp?.spatialDesignations || currentSite?.spatialDesignations || [];
		applicablePolicies = currentApp?.relevantPolicies || currentSite?.applicablePolicies || [];
	}
</script>

<div class="flex h-full">
	<!-- Sidebar: Application/Site selection -->
	<div class="w-1/4 min-w-[300px] border-r">
		<SearchFilterPanel items={searchItems} searchPlaceholder="Search applications or sites..." on:itemSelected={handleItemSelected} />
	</div>
	<!-- Central: Map and details -->
	<div class="flex-1 flex flex-col border-r">
		<div class="flex-1 bg-gray-100">
			<MapDisplay site={currentSite} constraintsToDisplay={siteSpatialDesignations} />
		</div>
	</div>
	<!-- Right: Policies/Spatial Designations -->
	<div class="w-1/4 min-w-[300px] p-4 overflow-y-auto">
		<h3 class="text-lg font-semibold mb-3">Applicable Policies</h3>
		<div class="space-y-3">
			{#if applicablePolicies.length > 0}
				{#each applicablePolicies as policy (policy.id)}
					<PolicyCard {policy} />
				{/each}
			{:else}
				<p class="text-gray-500">No applicable policies for this selection.</p>
			{/if}
		</div>
		<h3 class="text-lg font-semibold mt-6 mb-3">Overlapping Spatial Designations</h3>
		<div class="space-y-3">
			{#if siteSpatialDesignations.length > 0}
				{#each siteSpatialDesignations as spatialDesignation (spatialDesignation.id)}
					<SpatialDesignationDisplay spatialDesignation={spatialDesignation} />
				{/each}
			{:else}
				<p class="text-gray-500">No spatial designations for this selection.</p>
			{/if}
		</div>
	</div>
</div>
