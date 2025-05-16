<script lang="ts">
	import { policies as allPoliciesStore, planDocuments as allPlanDocumentsStore } from '$lib/stores/mainDataStore';
	import { selectedPolicyId, selectedDocumentId as selectedDocumentIdStore } from '$lib/stores/uiStateStore';
	import type { Policy, PlanDocument } from '$types/models';
	import SearchFilterInput from '$lib/components/common/SearchFilterInput.svelte';
	import Badge from '$lib/components/common/Badge.svelte';
	import { onMount, onDestroy } from 'svelte';
	import { get } from 'svelte/store'; // To get initial values if needed

	let searchTermLocal: string = ''; // Local variable for the search input
	let currentSelectedDocumentId: string | null = get(selectedDocumentIdStore); // Initialize with current store value

	// Subscribe to selectedDocumentIdStore to keep currentSelectedDocumentId in sync
	const unsubscribeSelectedDocId = selectedDocumentIdStore.subscribe(value => {
		currentSelectedDocumentId = value;
	});

	// Initialize selectedDocumentIdStore if no document is selected and documents are available
	onMount(() => {
		const planDocuments = get(allPlanDocumentsStore);
		if (!currentSelectedDocumentId && planDocuments.length > 0) {
			const localPlan = planDocuments.find(doc => doc.type === 'Local Plan');
			if (localPlan) {
				selectedDocumentIdStore.set(localPlan.id);
			} else {
				selectedDocumentIdStore.set(planDocuments[0].id);
			}
		}
	});
	
	// Reactive statement for filteredPolicies
	let filteredPolicies: Policy[] = [];
	$: {
		const $allPolicies = get(allPoliciesStore); // Get current value of the store
		const $selectedDocumentId = currentSelectedDocumentId; // Use the local synced variable
		
		let policiesToFilter = $allPolicies;
		if ($selectedDocumentId) {
			policiesToFilter = policiesToFilter.filter(p => p.documentId === $selectedDocumentId);
		}
		if (!searchTermLocal.trim()) {
			filteredPolicies = policiesToFilter;
		} else {
			const lowerSearchTerm = searchTermLocal.toLowerCase();
			filteredPolicies = policiesToFilter.filter(
				(policy) =>
					policy.title.toLowerCase().includes(lowerSearchTerm) ||
					policy.reference.toLowerCase().includes(lowerSearchTerm) ||
					(policy.wording && policy.wording.toLowerCase().includes(lowerSearchTerm)) // Added check for wording existence
			);
		}
	}

    let availableDocuments: PlanDocument[] = [];
    $: {
        availableDocuments = get(allPlanDocumentsStore).filter(doc => doc.type === 'Local Plan' || doc.type === 'SPD');
    }

    let totalPoliciesInSelectedDocument = 0;
    $: {
        const $allPolicies = get(allPoliciesStore);
        totalPoliciesInSelectedDocument = $allPolicies.filter(p => !currentSelectedDocumentId || p.documentId === currentSelectedDocumentId).length;
    }


	function selectPolicy(policyId: string) {
		selectedPolicyId.set(policyId);
	}

    onDestroy(() => {
        unsubscribeSelectedDocId();
    });

</script>

<div class="flex flex-col h-full">
	<div class="p-4 border-b border-gray-200">
		<h2 class="text-lg font-semibold text-gray-800">Policy Navigator</h2>
		{#if availableDocuments.length > 1}
			<div class="mt-2">
				<label for="document-select" class="block text-sm font-medium text-gray-700 mb-1">Select Document:</label>
				<select 
                    id="document-select" 
                    bind:value={$selectedDocumentIdStore} 
                    class="w-full p-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
					{#each availableDocuments as doc (doc.id)}
						<option value={doc.id}>{doc.name} ({doc.type})</option>
					{/each}
				</select>
			</div>
		{/if}
	</div>
	<SearchFilterInput bind:value={searchTermLocal} placeholder="Search policies (e.g. H2, housing)" label="Search policies" />

	<div class="flex-1 overflow-y-auto">
		{#if filteredPolicies.length === 0}
			<p class="p-4 text-sm text-gray-500">
                No policies found{searchTermLocal ? ' for "' + searchTermLocal + '"' : ''}{currentSelectedDocumentId ? ' in selected document.' : '.'}
            </p>
		{:else}
			<ul>
				{#each filteredPolicies as policy (policy.id)}
					<li
						class="border-b border-gray-200 hover:bg-gray-50 focus-within:bg-gray-100 {$selectedPolicyId === policy.id ? 'bg-blue-50 border-l-4 border-blue-500' : 'border-l-4 border-transparent'}"
                        role="button"
						tabindex="0"
						on:click={() => selectPolicy(policy.id)}
						on:keydown={(e) => { if (e.key === 'Enter' || e.key === ' ') selectPolicy(policy.id); }}
						aria-pressed={$selectedPolicyId === policy.id}
                        aria-label="Select policy {policy.reference} {policy.title}"
					>
						<div class="p-3">
							<div class="flex justify-between items-center mb-1">
								<h3 class="text-sm font-semibold text-blue-600">{policy.reference} - {policy.title}</h3>
							</div>
							<div class="flex space-x-2">
								<Badge text={policy.type} color="blue" />
								<Badge text={policy.status} color={policy.status === 'Adopted' ? 'green' : policy.status === 'Draft' ? 'yellow' : 'gray'} />
							</div>
						</div>
					</li>
				{/each}
			</ul>
		{/if}
	</div>
	<div class="p-2 border-t border-gray-200 text-xs text-gray-500">
		Displaying {filteredPolicies.length} of {totalPoliciesInSelectedDocument} policies.
	</div>
</div>