<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let items: any[] = [];
	export let searchPlaceholder: string = 'Search...';

	let searchTerm: string = '';
	let filteredItems: any[] = [];

	const dispatch = createEventDispatcher();

	$: {
		if (!searchTerm) {
			filteredItems = items;
		} else {
			filteredItems = items.filter((item) =>
				JSON.stringify(item).toLowerCase().includes(searchTerm.toLowerCase())
			);
		}
		dispatch('itemsFiltered', { items: filteredItems });
	}

	function handleItemSelect(item: any) {
		dispatch('itemSelected', { item });
	}
</script>

<div class="p-4 border-r h-full overflow-y-auto">
	<input
		type="text"
		bind:value={searchTerm}
		placeholder={searchPlaceholder}
		class="w-full p-2 border rounded mb-4"
	/>
	<ul class="space-y-2">
		{#each filteredItems as item (item.id)}
			<button
				type="button"
				on:click={() => handleItemSelect(item)}
				class="w-full text-left p-2 hover:bg-gray-100 cursor-pointer rounded"
			>
				{item.name || item.reference || item.id}
			</button>
		{/each}
	</ul>
	{#if filteredItems.length === 0}
		<p class="text-gray-500">No items found.</p>
	{/if}
</div>
