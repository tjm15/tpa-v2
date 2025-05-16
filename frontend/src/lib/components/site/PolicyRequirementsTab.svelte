<script lang="ts">
    import type { Site } from '$types/models';
    import Card from '$lib/components/common/Card.svelte';
    import Badge from '$lib/components/common/Badge.svelte';

    export let site: Site | null;

    let conflictsOrBurdens: string[] = [];
    $: {
        conflictsOrBurdens = [];
        if (site && site.applicablePolicies && site.applicablePolicies.length > 1) {
            // Basic mock conflict detection
            const policyTypes = new Set(site.applicablePolicies.map(p => p.type));
            if (policyTypes.has('Strategic') && policyTypes.has('Development Management (DM)')) {
                // This is normal, not a conflict. More complex logic needed for real conflicts.
            }
            if (site.applicablePolicies.filter(p => p.requirementsSummary?.toLowerCase().includes("affordable housing")).length > 1) {
                // conflictsOrBurdens.push("Multiple policies address affordable housing; ensure consistency.");
            }
        }
    }
</script>

<div class="p-1 text-sm space-y-3">
    {#if site && site.policyRequirementsSummary && site.policyRequirementsSummary.length > 0}
        <h4 class="text-md font-semibold text-gray-700 mb-2">Applicable Policy Requirements:</h4>
        <ul class="space-y-2">
            {#each site.policyRequirementsSummary as req (req.policyId)}
                <li class="p-3 border rounded-md bg-white shadow-sm">
                    <div class="flex justify-between items-center">
                        <span class="font-medium text-gray-800">{req.policyRef}</span>
                        {#if req.relevance}
                            <Badge text="Key Consideration" color="yellow" size="sm" />
                        {/if}
                    </div>
                    <p class="text-gray-600 mt-1">{req.requirement}</p>
                </li>
            {/each}
        </ul>
        {#if conflictsOrBurdens.length > 0}
            <div class="mt-4 p-3 bg-yellow-50 border border-yellow-300 rounded-md">
                <h5 class="font-semibold text-yellow-700">Potential Conflicts/Cumulative Burden:</h5>
                <ul class="list-disc list-inside text-yellow-600 text-xs">
                    {#each conflictsOrBurdens as item}
                        <li>{item}</li>
                    {/each}
                </ul>
            </div>
        {/if}
    {:else if site}
        <p class="text-gray-500">No specific policy requirements automatically resolved for this site.</p>
    {:else}
        <p class="text-gray-500">Select a site to see policy requirements.</p>
    {/if}
</div>