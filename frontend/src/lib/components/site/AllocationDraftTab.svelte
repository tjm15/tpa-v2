<script lang="ts">
    import type { Site, Policy } from '$types/models';
    import { sites as allSitesStore, policies as allPoliciesStore } from '$lib/stores/mainDataStore';
    import Button from '$lib/components/common/Button.svelte';
    import { get } from 'svelte/store';

    export let site: Site | null;

    let editableJustification: string = '';
    let suggestedPolicies: Policy[] = [];

    $: {
        editableJustification = site?.allocationJustification || site?.aiDraftJustification || '';
        suggestedPolicies = [];
        if (site) {
            // Mock: Suggest first 2 applicable policies if any, or first 2 policies overall
            if (site.applicablePolicies && site.applicablePolicies.length > 0) {
                suggestedPolicies = site.applicablePolicies.slice(0,2);
            } else {
                suggestedPolicies = get(allPoliciesStore).slice(0,2);
            }
        }
    }

    function handleSaveJustification() {
        if (!site) return;
        const updatedSite: Site = { ...site, allocationJustification: editableJustification };
        allSitesStore.update(sites => {
            const index = sites.findIndex(s => s.id === updatedSite.id);
            if (index !== -1) sites[index] = updatedSite;
            return sites;
        });
        alert('Allocation draft saved (mock)!');
    }

    function addPolicyReference(policyRef: string) {
        editableJustification += ` (see Policy ${policyRef})`;
    }
</script>

<div class="p-1 text-sm">
    {#if site}
        <div>
            <h4 class="text-md font-semibold text-gray-700 mb-2">Officer Justification / Allocation Draft:</h4>
            <textarea
                bind:value={editableJustification}
                rows="8"
                class="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Enter reasons for allocation or rejection..."
            ></textarea>

            {#if site.aiDraftJustification && site.allocationJustification !== site.aiDraftJustification}
                <div class="mt-2 p-2 bg-blue-50 border border-blue-200 rounded-md text-xs">
                    <p class="font-medium text-blue-700">AI Suggested Draft:</p>
                    <p class="text-blue-600 whitespace-pre-wrap">{site.aiDraftJustification}</p>
                </div>
            {/if}
            
            <div class="mt-3">
                <h5 class="text-sm font-semibold text-gray-600 mb-1">Suggested Policy References:</h5>
                <div class="flex flex-wrap gap-2">
                    {#each suggestedPolicies as p (p.id)}
                        <Button size="sm" variant="secondary" on:click={() => addPolicyReference(p.reference)}>
                            Add Ref: {p.reference}
                        </Button>
                    {/each}
                </div>
            </div>

            <div class="mt-4 flex justify-end">
                <Button on:click={handleSaveJustification} variant="primary">Save Draft</Button>
            </div>
        </div>
    {:else}
        <p class="text-gray-500">Select a site to draft its allocation justification.</p>
    {/if}
</div>