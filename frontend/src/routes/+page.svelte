<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(() => {
		goto('/dashboard', { replaceState: true });
	});
</script>

<div class="flex items-center justify-center h-screen">
	<p>Loading...</p>
</div>