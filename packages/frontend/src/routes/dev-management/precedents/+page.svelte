<script lang="ts">
	import SearchFilterPanel from '$lib/components/shared/SearchFilterPanel.svelte';
	import PrecedentCard from '$lib/components/dm/PrecedentCard.svelte';
	import ItemDetailView from '$lib/components/shared/ItemDetailView.svelte';
	import { precedentCases } from '$lib/stores/mainDataStore';
	import type { PrecedentCase } from '$types/models';
	import { get } from 'svelte/store';

	let precedents: PrecedentCase[] = get(precedentCases);
	let filteredPrecedents: PrecedentCase[] = precedents;
	let selectedPrecedent: PrecedentCase | null = null;

	function handleFiltered(event: CustomEvent) {
		filteredPrecedents = event.detail.items;
	}
	function handleSelected(event: CustomEvent) {
		selectedPrecedent = event.detail.item;
	}
</script>

<div class="flex h-full">
	<!-- Sidebar: Search Precedents -->
	<div class="w-1/4 min-w-[300px] p-4 border-r">
		<h2 class="text-lg font-semibold mb-3">Search Precedents</h2>
		<SearchFilterPanel items={precedents} searchPlaceholder="Search by reference, address, policy..." on:itemsFiltered={handleFiltered} on:itemSelected={handleSelected} />
	</div>
	<!-- Central: Precedent List -->
	<div class="flex-1 p-4 border-r overflow-y-auto">
		<h2 class="text-xl font-semibold mb-3">Precedent Cases ({filteredPrecedents.length})</h2>
		<div class="space-y-3">
			{#if filteredPrecedents.length > 0}
				{#each filteredPrecedents as precedent (precedent.id)}
					<button
						type="button"
						on:click={() => handleSelected(new CustomEvent('itemSelected', { detail: { item: precedent } }))}
						aria-pressed={selectedPrecedent && selectedPrecedent.id === precedent.id}
						class="w-full text-left outline-none focus:ring-2 focus:ring-blue-400"
					>
						<PrecedentCard {precedent} />
					</button>
				{/each}
			{:else}
				<p class="text-gray-500">No precedents found.</p>
			{/if}
		</div>
	</div>
	<!-- Right: Precedent Details -->
	<div class="w-1/3 min-w-[350px] p-4 overflow-y-auto">
		<ItemDetailView item={selectedPrecedent} title="Precedent Details" />
	</div>
</div>
