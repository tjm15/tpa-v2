<script lang="ts">
	export let title: string | undefined = undefined;
	export let additionalClasses: string = '';
	export let titleClasses: string = 'text-lg font-semibold text-gray-800';
    export let titleContainerClasses: string = 'px-4 py-3 border-b border-gray-200';
	export let bodyClasses: string = 'p-4';
	export let noBodyPadding: boolean = false;
</script>

<div class="bg-white shadow rounded-lg {additionalClasses}">
	{#if title || $$slots.title}
		<div class="{titleContainerClasses}">
            {#if $$slots.title}
                 <slot name="title"></slot>
            {:else if title}
			    <h3 class="{titleClasses}">{title}</h3>
            {/if}
		</div>
	{/if}
	<div class={noBodyPadding ? '' : bodyClasses}>
		<slot />
	</div>
</div>