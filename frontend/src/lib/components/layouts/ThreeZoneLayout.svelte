<script lang="ts">
	// Props could be added later for sidebar widths, etc.
</script>

<div class="flex flex-col md:flex-row h-full flex-1 min-h-0 bg-gray-100">
	<aside class="w-1/4 min-w-[280px] max-w-[400px] bg-white border-r border-gray-200 overflow-y-auto shadow-lg">
		<slot name="left-sidebar"></slot>
	</aside>

	<main class="flex-1 flex flex-col">
		<slot name="central-panel"></slot>
	</main>

	<aside class="w-1/4 min-w-[300px] max-w-[450px] bg-white border-l border-gray-200 overflow-y-auto shadow-lg">
		<slot name="right-sidebar"></slot>
	</aside>
</div>

<style lang="postcss">
	/* Ensure Tailwind directives are in app.css or a global stylesheet */
	/* You can add specific styles for this layout if needed, */
	/* but prefer using Tailwind classes directly in the slots or child components. */
</style>