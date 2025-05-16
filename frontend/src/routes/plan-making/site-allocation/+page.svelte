<script lang="ts">
	import ThreeZoneLayout from '$lib/components/layouts/ThreeZoneLayout.svelte';
	import SiteNavigator from '$lib/components/site/SiteNavigator.svelte';
	import SiteContextView from '$lib/components/site/SiteContextView.svelte';
	import DeliverabilitySoundnessPanel from '$lib/components/site/DeliverabilitySoundnessPanel.svelte';
</script>

<ThreeZoneLayout>
	<div slot="left-sidebar" class="h-full">
		<SiteNavigator />
	</div>
	<div slot="central-panel" class="h-full bg-slate-50">
		<SiteContextView />
	</div>
	<div slot="right-sidebar" class="h-full bg-slate-50">
		<DeliverabilitySoundnessPanel />
	</div>
</ThreeZoneLayout>
