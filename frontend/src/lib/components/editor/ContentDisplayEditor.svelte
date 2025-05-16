<script lang="ts">
    export let value: string = '';
    export let placeholder: string = 'Enter content...';
    export let rows: number = 10;
    export let readOnly: boolean = false;

    // In a real component, you'd have editor logic here.
    // For now, it's just a textarea.
</script>

{#if readOnly}
    <div class="prose max-w-none p-2 border border-gray-200 rounded-md bg-gray-50 min-h-[100px]">
        <p class="whitespace-pre-wrap">{value || placeholder}</p>
    </div>
{:else}
    <textarea
        bind:value
        {rows}
        {placeholder}
        class="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
    ></textarea>
{/if}