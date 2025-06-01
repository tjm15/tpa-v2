<script lang="ts">
	export let item: any | null = null;
	export let title: string = "Details";
</script>

<div class="p-4 h-full overflow-y-auto">
	<h3 class="text-lg font-semibold mb-3">{title}</h3>
	{#if item}
		<slot name="detailTemplate" {item}>
			<pre class="text-sm bg-gray-50 p-2 rounded">{JSON.stringify(item, null, 2)}</pre>
		</slot>
	{:else}
		<p class="text-gray-500">No item selected or details available.</p>
	{/if}
</div>
