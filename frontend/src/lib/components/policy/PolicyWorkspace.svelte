<script lang="ts">
	import { policies, getPolicyById } from '$lib/stores/mainDataStore';
	import { selectedPolicyId } from '$lib/stores/uiStateStore';
	import type { Policy } from '$types/models';
	import Card from '$lib/components/common/Card.svelte';
	import Badge from '$lib/components/common/Badge.svelte';
	import Button from '$lib/components/common/Button.svelte';
	// import ContentDisplayEditor from '$lib/components/editor/ContentDisplayEditor.svelte'; // Assuming this will be created

	let currentPolicy: Policy | null | undefined = null;
	let editableWording: string = '';
	let editableSupportingText: string = '';
	// Add more editable fields as needed

	$: {
		if ($selectedPolicyId) {
			currentPolicy = getPolicyById($selectedPolicyId);
			editableWording = currentPolicy?.wording || '';
			editableSupportingText = currentPolicy?.supportingText || '';
		} else {
			currentPolicy = null;
			editableWording = '';
			editableSupportingText = '';
		}
	}

	function handleSave() {
		if (!currentPolicy) return;
		// Create a new policy object with updated values
		const updatedPolicy: Policy = {
			...currentPolicy,
			wording: editableWording,
			supportingText: editableSupportingText,
			lastModified: new Date().toISOString()
			// Update other fields
		};
		// Update in the store
		policies.update(all => {
			const index = all.findIndex(p => p.id === updatedPolicy.id);
			if (index !== -1) {
				all[index] = updatedPolicy;
			}
			return all;
		});
		alert('Policy saved (mock)!');
	}
</script>

<div class="p-4 md:p-6 h-full flex flex-col space-y-4 overflow-y-auto">
	{#if currentPolicy}
		<Card additionalClasses="flex-shrink-0">
			<div slot="title" class="flex justify-between items-center">
				<span>{currentPolicy.reference} - {currentPolicy.title}</span>
				<div class="flex space-x-2">
                    <Badge text={currentPolicy.type} color="blue" />
					<Badge text={currentPolicy.status} color={currentPolicy.status === 'Adopted' ? 'green' : currentPolicy.status === 'Draft' ? 'yellow' : 'gray'} />
                </div>
			</div>
			<div class="grid grid-cols-2 gap-4 text-sm mb-4 p-4 border-b">
				<div><span class="font-semibold">Version:</span> {currentPolicy.version || 'N/A'}</div>
				<div><span class="font-semibold">Last Modified:</span> {currentPolicy.lastModified ? new Date(currentPolicy.lastModified).toLocaleDateString() : 'N/A'}</div>
				<div><span class="font-semibold">Author:</span> {currentPolicy.author || 'N/A'}</div>
			</div>

			<div class="p-4">
				<h3 class="text-md font-semibold text-gray-700 mb-2">Policy Wording</h3>
				<textarea
					bind:value={editableWording}
					rows="10"
					class="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
				></textarea>
				{#if currentPolicy.aiGuidance && currentPolicy.aiGuidance.length > 0}
				<div class="mt-3 space-y-2">
					{#each currentPolicy.aiGuidance as guidance}
					<div class="p-2 bg-yellow-50 border border-yellow-200 rounded-md text-xs text-yellow-700">
						<strong>AI Suggestion ({guidance.type}):</strong> {guidance.message}
					</div>
					{/each}
				</div>
				{/if}
			</div>

            <div class="p-4 border-t">
				<h3 class="text-md font-semibold text-gray-700 mb-2">Supporting Text (Optional)</h3>
				<textarea
					bind:value={editableSupportingText}
					rows="5"
					class="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
				></textarea>
			</div>

            {#if currentPolicy.internalNotes}
            <div class="p-4 border-t bg-gray-50">
                <h3 class="text-md font-semibold text-gray-700 mb-1">Internal Notes</h3>
                <p class="text-sm text-gray-600 whitespace-pre-wrap">{currentPolicy.internalNotes}</p>
            </div>
            {/if}

			<div class="p-4 flex justify-end border-t">
				<Button on:click={handleSave} variant="primary">Save Policy</Button>
			</div>
		</Card>
	{:else}
		<div class="flex items-center justify-center h-full">
			<p class="text-gray-500">Select a policy from the navigator to view or edit details.</p>
		</div>
	{/if}
</div>