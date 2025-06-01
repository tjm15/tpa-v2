<script lang="ts" generics="T extends { id: string | number }">
	import { createEventDispatcher } from 'svelte';

	export let items: T[] = [];
	export let selectedId: string | number | null = null;

	const dispatch = createEventDispatcher();

	function selectItem(item: T) {
		dispatch('itemSelected', { item });
	}
</script>

<ul class="space-y-1">
	{#each items as item (item.id)}
		<li
			class="p-2 rounded cursor-pointer"
			class:bg-blue-100={selectedId === item.id}
			class:hover:bg-gray-100={selectedId !== item.id}
			on:click={() => selectItem(item)}
			on:keydown={(e) => e.key === 'Enter' && selectItem(item)}
			tabindex="0"
			role="option"
			aria-selected={selectedId === item.id}
		>
			<slot name="itemTemplate" {item}>
				<span>{JSON.stringify(item)}</span>
			</slot>
		</li>
	{/each}
	{#if items.length === 0}
		<p class="p-2 text-gray-500">No items to display.</p>
	{/if}
</ul>
