<script lang="ts">
	import ThreeZoneLayout from '$lib/components/layouts/ThreeZoneLayout.svelte';
	import PolicyNavigator from '$lib/components/policy/PolicyNavigator.svelte';
	import PolicyWorkspace from '$lib/components/policy/PolicyWorkspace.svelte';
	import PolicyImpactPanel from '$lib/components/policy/PolicyImpactPanel.svelte';
	import { selectedPolicyId } from '$lib/stores/uiStateStore'; // To reset on unmount if needed
	import { onDestroy } from 'svelte';

    // Optional: Reset selected policy when navigating away from this specific mode's page
    // However, the main +layout.svelte handles broader workspace/mode changes.
    // This might be useful if you want selection to clear even when switching tabs within the same workspace.
    // onDestroy(() => {
    //     if ($page.url.pathname !== '/plan-making/policy') { // Check if truly navigating away
    //         selectedPolicyId.set(null);
    //     }
    // });
</script>

<ThreeZoneLayout>
	<div slot="left-sidebar" class="h-full">
		<PolicyNavigator />
	</div>
	<div slot="central-panel" class="h-full bg-slate-50">
		<!-- Added a subtle bg for central panel -->
		<PolicyWorkspace />
	</div>
	<div slot="right-sidebar" class="h-full bg-slate-50">
		<!-- Added a subtle bg for right sidebar -->
		<PolicyImpactPanel />
	</div>
</ThreeZoneLayout>