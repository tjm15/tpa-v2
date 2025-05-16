<script lang="ts">
	export let text: string;
	export let color: 'blue' | 'green' | 'yellow' | 'red' | 'gray' | 'purple' = 'gray';
	export let size: 'sm' | 'md' = 'sm';
	export let additionalClasses: string = '';

	let bgColorClass = '';
	let textColorClass = '';
	let textSizeClass = size === 'sm' ? 'text-xs' : 'text-sm';

	$: {
		switch (color) {
			case 'blue':
				bgColorClass = 'bg-blue-100';
				textColorClass = 'text-blue-700';
				break;
			case 'green':
				bgColorClass = 'bg-green-100';
				textColorClass = 'text-green-700';
				break;
			case 'yellow':
				bgColorClass = 'bg-yellow-100';
				textColorClass = 'text-yellow-700';
				break;
			case 'red':
				bgColorClass = 'bg-red-100';
				textColorClass = 'text-red-700';
				break;
			case 'purple':
				bgColorClass = 'bg-purple-100';
				textColorClass = 'text-purple-700';
				break;
			default: // gray
				bgColorClass = 'bg-gray-100';
				textColorClass = 'text-gray-700';
				break;
		}
	}
</script>

<span
	class="inline-flex items-center px-2.5 py-0.5 rounded-full font-medium {textSizeClass} {bgColorClass} {textColorClass} {additionalClasses}"
>
	{text}
</span>