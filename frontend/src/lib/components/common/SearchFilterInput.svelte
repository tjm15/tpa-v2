<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let value: string = '';
	export let placeholder: string = 'Search...';
	export let label: string = 'Search'; // For accessibility

	const dispatch = createEventDispatcher<{ change: string; input: string }>();

	function handleChange(event: Event) {
		const target = event.target as HTMLInputElement;
		value = target.value;
		dispatch('change', value);
	}

	function handleInput(event: Event) {
		const target = event.target as HTMLInputElement;
		value = target.value;
		dispatch('input', value);
	}
</script>

<div class="p-2">
	<label for="search-input-{label.replace(/\s+/g, '-').toLowerCase()}" class="sr-only">{label}</label>
	<input
		type="search"
		id="search-input-{label.replace(/\s+/g, '-').toLowerCase()}"
		bind:value
		{placeholder}
		on:change={handleChange}
		on:input={handleInput}
		class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
	/>
</div>