<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let type: 'button' | 'submit' | 'reset' = 'button';
	export let variant: 'primary' | 'secondary' | 'danger' | 'ghost' = 'primary';
	export let size: 'sm' | 'md' | 'lg' = 'md';
	export let disabled: boolean = false;
	export let fullWidth: boolean = false;
	export let additionalClasses: string = '';

	const dispatch = createEventDispatcher();

	let baseClasses =
		'inline-flex items-center justify-center border border-transparent rounded-md shadow-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors duration-150 ease-in-out';
	let variantClasses = '';
	let sizeClasses = '';

	$: {
		let interactivityClasses = disabled ? 'opacity-50 cursor-not-allowed' : '';
		switch (variant) {
			case 'primary':
				variantClasses = `bg-blue-600 text-white ${!disabled ? 'hover:bg-blue-700' : ''} focus:ring-blue-500`;
				break;
			case 'secondary':
				variantClasses = `bg-gray-200 text-gray-700 ${!disabled ? 'hover:bg-gray-300' : ''} focus:ring-gray-400`;
				break;
			case 'danger':
				variantClasses = `bg-red-600 text-white ${!disabled ? 'hover:bg-red-700' : ''} focus:ring-red-500`;
				break;
			case 'ghost':
				variantClasses = `text-blue-600 ${!disabled ? 'hover:bg-blue-50' : ''} focus:ring-blue-500 border-transparent`;
				break;
		}
		variantClasses += ` ${interactivityClasses}`;
	}

	$: {
		switch (size) {
			case 'sm':
				sizeClasses = 'px-3 py-1.5 text-xs';
				break;
			case 'md':
				sizeClasses = 'px-4 py-2 text-sm';
				break;
			case 'lg':
				sizeClasses = 'px-6 py-3 text-base';
				break;
		}
	}
</script>

<button
	{type}
	class="{baseClasses} {variantClasses} {sizeClasses} {fullWidth
		? 'w-full'
		: ''} {additionalClasses}"
	{disabled}
	on:click
>
	<slot />
</button>