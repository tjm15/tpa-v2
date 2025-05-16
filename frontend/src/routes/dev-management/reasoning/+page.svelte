<script lang="ts">
	import EntityList from '$lib/components/shared/EntityList.svelte';
	import { planningApplications } from '$lib/stores/mainDataStore';
	import type { PlanningApplication, Policy } from '$types/models';
	import { get } from 'svelte/store';
	import PolicyCard from '$lib/components/dm/PolicyCard.svelte';

	let allApps: PlanningApplication[] = get(planningApplications);
	let selectedApp: PlanningApplication | null = null;
	let selectedStep: any = null;
	let selectedPolicy: Policy | null = null;

	function handleAppSelected(event: CustomEvent) {
		selectedApp = event.detail.item;
		selectedStep = null;
		selectedPolicy = null;
	}
	function handleStepSelected(event: CustomEvent) {
		selectedStep = event.detail.item;
		selectedPolicy = null;
	}
	function handlePolicySelected(policy: Policy) {
		selectedPolicy = policy;
	}
</script>

<div class="flex h-full">
	<!-- Sidebar: Reasoning Steps -->
	<div class="w-1/3 min-w-[350px] p-4 border-r overflow-y-auto">
		<h2 class="text-lg font-semibold mb-3">Applications</h2>
		<EntityList items={allApps} on:itemSelected={handleAppSelected} />
		{#if selectedApp}
			<h2 class="text-lg font-semibold mb-3 mt-6">Reasoning Steps</h2>
			<EntityList items={(selectedApp.reasoningSteps || []).map((step, idx) => ({ ...step, id: step.step ?? idx }))} on:itemSelected={handleStepSelected} />
			<button class="mt-4 p-2 bg-green-500 text-white rounded w-full hover:bg-green-600">Add Step</button>
		{/if}
	</div>
	<!-- Central: Policy Details -->
	<div class="flex-1 p-4 border-r overflow-y-auto">
		<h2 class="text-xl font-semibold mb-3">Policy Details</h2>
		{#if selectedStep && selectedApp}
			{#each selectedStep.policyReferences as ref}
				{#if selectedApp.relevantPolicies}
					{#each selectedApp.relevantPolicies.filter(p => p.reference === ref) as policy}
						<div class="mb-4">
							<button type="button" class="w-full text-left focus:outline-none focus:ring-2 focus:ring-blue-400 rounded" on:click={() => handlePolicySelected(policy)} on:keydown={(e) => (e.key === 'Enter' || e.key === ' ') && handlePolicySelected(policy)} tabindex="0" aria-pressed={selectedPolicy && selectedPolicy.reference === policy.reference}>
								<PolicyCard policy={policy} />
							</button>
						</div>
					{/each}
				{/if}
			{/each}
			{#if selectedPolicy}
				<div class="prose prose-sm max-w-none mt-4">
					<PolicyCard policy={selectedPolicy} />
				</div>
			{/if}
		{:else}
			<p class="text-gray-500">Select a reasoning step to see details or associated policies.</p>
		{/if}
	</div>
	<!-- Right: Trade-off Analysis -->
	<div class="w-1/4 min-w-[300px] p-4 overflow-y-auto">
		<h2 class="text-lg font-semibold mb-3">Trade-off Analysis</h2>
		{#if selectedApp && selectedApp.tradeOffAnalysis}
			<div class="text-sm space-y-3">
				{#if selectedApp.tradeOffAnalysis.competingGoals}
					<h4 class="font-medium">Competing Goals/Policies:</h4>
					<ul class="list-disc pl-5">
						{#each selectedApp.tradeOffAnalysis.competingGoals as trade}
							<li>{trade.goalA} vs {trade.goalB}: {trade.tension}</li>
						{/each}
					</ul>
				{/if}
				{#if selectedApp.tradeOffAnalysis.aiNarrative}
					<h4 class="font-medium mt-3">AI Narrative:</h4>
					<p>{selectedApp.tradeOffAnalysis.aiNarrative}</p>
				{/if}
			</div>
		{:else}
			<p class="text-sm text-gray-500">No trade-off analysis available.</p>
		{/if}
	</div>
</div>
