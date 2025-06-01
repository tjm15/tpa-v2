<script lang="ts">
	import { getPolicyById, policies as allPolicies, sites as allSites, goals as allGoals } from '$lib/stores/mainDataStore';
	import { selectedPolicyId } from '$lib/stores/uiStateStore';
	import type { Policy, LinkedPolicy, AffectedSite, StrategicGoalAlignment, Site, Goal } from '$types/models';
	import Card from '$lib/components/common/Card.svelte';
	import Badge from '$lib/components/common/Badge.svelte';
	import Button from '$lib/components/common/Button.svelte'; // For potential navigation
    import { derived } from 'svelte/store';

	// These would ideally come directly from the currentPolicy object after processing.
    // For now, we derive them as examples.
	const currentPolicyDetails = derived([allPolicies, selectedPolicyId], ([$allPolicies, $selectedPolicyId]) => {
        if (!$selectedPolicyId) return null;
        const policy = $allPolicies.find(p => p.id === $selectedPolicyId);
        if (!policy) return null;

        // Mocked/Derived linked policies
        const linkedPolicies: LinkedPolicy[] = policy.linkedPolicies || [];
        if (policy.reference === 'H1' && !$allPolicies.find(p=>p.reference === 'DM12')?.linkedPolicies?.find(lp => lp.policyId === policy.id)) {
            // Example: If DM12 doesn't already link H1, let's mock a link for demo
            const dm12 = $allPolicies.find(p => p.reference === 'DM12');
            if (dm12) {
                 linkedPolicies.push({policyId: dm12.id, policyReference: dm12.reference, relationship: 'REFERENCED_BY', summary: 'Design policy supporting H1 quality.' });
            }
        }


        // Mocked/Derived affected sites
        const affectedSites: AffectedSite[] = policy.affectedSites || [];
         if (policy.reference === 'H1' && $allSites.length > 0) {
            if (!affectedSites.find(as => as.siteId === $allSites[0].id)) { // Avoid duplicates if already in mock
                affectedSites.push({siteId: $allSites[0].id, siteName: $allSites[0].name || 'Unnamed Site', impact: 'Conditions Development', details: 'Requires 30% affordable housing.'});
            }
        }


        // Mocked/Derived strategic goal alignments
        const strategicGoalAlignments: StrategicGoalAlignment[] = policy.strategicGoalAlignments || [];
        if (policy.strategicGoalAlignments?.length === 0 && $allGoals.length > 0) {
             if (!strategicGoalAlignments.find(sga => sga.goalId === $allGoals[0].id)) {
                strategicGoalAlignments.push({goalId: $allGoals[0].id, goalName: $allGoals[0].name, alignment: 'Supports', notes: 'Directly contributes to this housing goal.'});
             }
        }


        return {
            policy,
            linkedPolicies,
            affectedSites,
            strategicGoalAlignments
        };
    });

	function getRelationshipColor(relationship: LinkedPolicy['relationship']) {
		switch (relationship) {
			case 'CONFLICTS_WITH': return 'red';
			case 'SUPPORTS': return 'green';
			case 'REFERENCES': case 'REFERENCED_BY': return 'blue';
			case 'OVERLAPS_WITH': return 'yellow';
			default: return 'gray';
		}
	}

    function navigateToPolicy(policyId: string) {
        selectedPolicyId.set(policyId); // Navigate within Policy Mode
        // Later, this could open a modal or navigate to a different part of the app
        alert(`Maps to policy ${policyId} (mock)`);
    }

    function navigateToSite(siteId: string) {
        // This would ideally navigate to Site Allocation Mode with this site selected
        alert(`Maps to site ${siteId} (mock)`);
    }
</script>

<div class="p-1 md:p-2 space-y-3 overflow-y-auto h-full">
	{#if $currentPolicyDetails && $currentPolicyDetails.policy}
		<Card title="A. Conflict & Linkage" additionalClasses="text-sm">
			{#if $currentPolicyDetails.linkedPolicies.length > 0}
				<ul class="space-y-2">
					{#each $currentPolicyDetails.linkedPolicies as linked (linked.policyId)}
						<li class="p-2 border rounded-md hover:bg-gray-50">
							<div class="flex justify-between items-center">
								<span class="font-semibold text-gray-700">{linked.policyReference}</span>
								<Badge text={linked.relationship} color={getRelationshipColor(linked.relationship)} />
							</div>
							{#if linked.summary}
								<p class="text-xs text-gray-500 mt-1">{linked.summary}</p>
							{/if}
                            <Button size="sm" variant="ghost" additionalClasses="mt-1 text-xs" on:click={() => navigateToPolicy(linked.policyId)}>
                                View Policy
                            </Button>
						</li>
					{/each}
				</ul>
			{:else}
				<p class="text-xs text-gray-500">No direct policy conflicts or linkages identified.</p>
			{/if}
		</Card>

		<Card title="B. Site Allocation Impact" additionalClasses="text-sm">
			{#if $currentPolicyDetails.affectedSites.length > 0}
				<ul class="space-y-2">
					{#each $currentPolicyDetails.affectedSites as site (site.siteId)}
						<li class="p-2 border rounded-md hover:bg-gray-50">
							<div class="flex justify-between items-center">
                                <span class="font-semibold text-gray-700">{site.siteName}</span>
                                <Badge text={site.impact} color={site.impact === 'Restricts' ? 'red' : site.impact === 'Enables' ? 'green' : 'yellow'} />
                            </div>
							{#if site.details}
								<p class="text-xs text-gray-500 mt-1">{site.details}</p>
							{/if}
                            <Button size="sm" variant="ghost" additionalClasses="mt-1 text-xs" on:click={() => navigateToSite(site.siteId)}>
                                View Site
                            </Button>
						</li>
					{/each}
				</ul>
			{:else}
				<p class="text-xs text-gray-500">This policy does not directly affect specific site allocations based on current data.</p>
			{/if}
		</Card>

		<Card title="C. Strategic Goal Alignment" additionalClasses="text-sm">
			{#if $currentPolicyDetails.strategicGoalAlignments.length > 0}
				<ul class="space-y-2">
					{#each $currentPolicyDetails.strategicGoalAlignments as goal (goal.goalId)}
						<li class="p-2 border rounded-md">
                            <div class="flex justify-between items-center">
							    <span class="font-semibold text-gray-700">{goal.goalName}</span>
                                <Badge
                                    text={goal.alignment}
                                    color={goal.alignment === 'Supports' ? 'green' : goal.alignment === 'Undermines' ? 'red' : goal.alignment === 'Partially Aligns' ? 'yellow' : 'gray'}
                                />
                            </div>
							{#if goal.notes}
								<p class="text-xs text-gray-500 mt-1">{goal.notes}</p>
							{/if}
						</li>
					{/each}
				</ul>
			{:else}
				<p class="text-xs text-gray-500">No strategic goal alignments defined for this policy.</p>
			{/if}
		</Card>
	{:else}
		<div class="flex items-center justify-center h-full">
			<p class="text-gray-500">Select a policy to see its impact and integrity details.</p>
		</div>
	{/if}
</div>