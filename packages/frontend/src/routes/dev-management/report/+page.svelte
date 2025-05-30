<script lang="ts">
	import EntityList from '$lib/components/shared/EntityList.svelte';
	import { planningApplications } from '$lib/stores/mainDataStore';
	import type { PlanningApplication, OfficerReportSection } from '$types/models';
	import { get } from 'svelte/store';
	import OfficerReportSectionCard from '$lib/components/dm/OfficerReportSectionCard.svelte';

	let allApps: PlanningApplication[] = get(planningApplications);
	let selectedApp: PlanningApplication | null = null;
	let selectedSection: OfficerReportSection | null = null;
	let sectionContent: string = '';

	function handleAppSelected(event: CustomEvent) {
		selectedApp = event.detail.item;
		selectedSection = null;
		sectionContent = '';
	}
	function handleSectionSelected(event: CustomEvent) {
		selectedSection = event.detail.item;
		sectionContent = selectedSection?.content || '';
	}
	function saveSection() {
		if (selectedSection) {
			selectedSection.content = sectionContent;
			alert('Section content updated (mock).');
		}
	}
</script>

<div class="flex h-full">
	<!-- Sidebar: Report Structure -->
	<div class="w-1/4 min-w-[300px] p-4 border-r overflow-y-auto">
		<h2 class="text-lg font-semibold mb-3">Applications</h2>
		<EntityList items={allApps} on:itemSelected={handleAppSelected} />
		{#if selectedApp && selectedApp.officerReport}
			<h2 class="text-lg font-semibold mb-3 mt-6">Report Structure</h2>
			<div class="space-y-3">
				{#each selectedApp.officerReport.sections as section (section.id)}
					<button
						type="button"
						on:click={() => handleSectionSelected(new CustomEvent('sectionSelected', { detail: { item: section } }))}
						aria-pressed={selectedSection && selectedSection.id === section.id}
						class="w-full text-left outline-none focus:ring-2 focus:ring-blue-400"
					>
						<OfficerReportSectionCard section={section} />
					</button>
				{/each}
			</div>
		{/if}
	</div>
	<!-- Central: Section Editor -->
	<div class="flex-1 p-4 border-r flex flex-col">
		<h2 class="text-xl font-semibold mb-3">Editing Section</h2>
		{#if selectedSection}
			<div class="mb-4">
				<OfficerReportSectionCard section={selectedSection} />
			</div>
			<textarea class="flex-grow w-full p-2 border rounded resize-none" bind:value={sectionContent} placeholder="Enter section content here..."></textarea>
			<button class="mt-2 p-2 bg-green-500 text-white rounded hover:bg-green-600" on:click={saveSection}>Save Section (Mock)</button>
		{:else}
			<p class="text-gray-500">Select a section from the left to edit.</p>
		{/if}
	</div>
	<!-- Right: Supporting Information -->
	<div class="w-1/4 min-w-[300px] p-4 overflow-y-auto text-sm">
		<h2 class="text-lg font-semibold mb-3">Supporting Information</h2>
		{#if selectedApp}
			<div class="space-y-4">
				<div>
					<h4 class="font-medium">Evidence Links:</h4>
					<ul class="list-disc pl-5 text-xs">
						{#each selectedApp.relevantPolicies || [] as policy}
							<li>Policy: {policy.reference}</li>
						{/each}
						{#each selectedApp.constraints || [] as constraint}
							<li>Constraint: {constraint.name}</li>
						{/each}
						{#each selectedApp.linkedPrecedents || [] as precedent}
							<li>Precedent: {precedent.caseReference}</li>
						{/each}
					</ul>
				</div>
				<div>
					<h4 class="font-medium">Conflict Summary:</h4>
					<p>{selectedApp.officerReport?.conflictSummary || 'N/A'}</p>
				</div>
				<div>
					<h4 class="font-medium">Compliance Flags:</h4>
					<ul class="list-disc pl-5 text-xs">
						{#each selectedApp.officerReport?.complianceFlags || [] as flag}
							<li>{flag.flag}: {flag.met ? 'Met' : 'Not Met'}</li>
						{/each}
					</ul>
				</div>
				<button class="mt-4 p-2 bg-blue-500 text-white rounded w-full hover:bg-blue-600">Export Report (Mock)</button>
			</div>
		{:else}
			<p class="text-gray-500">Select an application to view supporting information.</p>
		{/if}
	</div>
</div>
