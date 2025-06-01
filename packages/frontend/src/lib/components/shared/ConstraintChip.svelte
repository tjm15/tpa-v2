<script lang="ts">
	import type { Constraint } from '$types/models';
	export let constraint: Constraint;

	const severityColors: Record<string, string> = {
		High: 'bg-red-500 text-white',
		Medium: 'bg-yellow-400 text-black',
		Low: 'bg-green-500 text-white',
		Informational: 'bg-blue-500 text-white',
	};
</script>

<div
	class={`px-2 py-1 text-xs rounded-full inline-block ${!constraint.severity ? 'bg-gray-300 text-black' : severityColors[constraint.severity]}`}
>
	{constraint.name}
	{#if constraint.severity}
		({constraint.severity})
	{/if}
</div>
