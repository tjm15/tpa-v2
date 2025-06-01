<script lang="ts">
	import type { DocumentNode } from '$types/models';
	import { selectedDocumentNodeId } from '$lib/stores/uiStateStore';
	import { createEventDispatcher } from 'svelte';

	export let node: DocumentNode;
	export let level: number = 0;

	const dispatch = createEventDispatcher<{ selectNode: string }>();

	let expanded = level < 2; // Auto-expand first couple of levels

	function toggleExpand() {
		expanded = !expanded;
	}

	function handleNodeSelect() {
		selectedDocumentNodeId.set(node.id);
		dispatch('selectNode', node.id); // For potential parent handling
	}

    function getIconForType(type: DocumentNode['type']) {
        switch(type) {
            case 'Chapter': return '📚';
            case 'PolicySection': return '📜';
            case 'MapSection': return '🗺️';
            case 'Appendix': return '📎';
            case 'GlossaryItem': return '📖';
            default: return '📄';
        }
    }
</script>

<li role="treeitem" aria-expanded={node.children && node.children.length > 0 ? expanded : undefined} aria-selected={$selectedDocumentNodeId === node.id}>
	<div
		role="button"
		class="flex items-center py-1.5 pr-2 rounded-md hover:bg-gray-100 cursor-pointer focus-within:bg-gray-200 focus:outline-none {$selectedDocumentNodeId === node.id ? 'bg-green-50 ring-1 ring-green-300' : ''}"
		style="padding-left: {level * 1.25 + 0.5}rem;"
		on:click={handleNodeSelect}
		on:keydown={(e) => {
			if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handleNodeSelect(); }
			if (e.key === 'ArrowRight' && node.children && node.children.length > 0 && !expanded) { e.preventDefault(); toggleExpand(); }
			if (e.key === 'ArrowLeft' && node.children && node.children.length > 0 && expanded) { e.preventDefault(); toggleExpand(); }
		}}
		tabindex="0"
	>
		{#if node.children && node.children.length > 0}
			<button
				on:click|stopPropagation={toggleExpand}
				class="mr-1 text-xs p-0.5 rounded hover:bg-gray-200"
				aria-label={expanded ? 'Collapse' : 'Expand'}
			>
				{expanded ? '▼' : '►'}
			</button>
		{/if}
        <span class="mr-1.5 text-sm">{getIconForType(node.type)}</span>
		<span class="text-sm text-gray-700 truncate select-none" title={node.title}>
            {node.reference ? `${node.reference}: ` : ''}{node.title}
        </span>
        {#if node.unresolvedIssues && node.unresolvedIssues.length > 0}
            <span class="ml-auto text-red-500 text-xs" title="{node.unresolvedIssues.length} unresolved issue(s)">⚠️</span>
        {/if}
	</div>

	{#if expanded && node.children && node.children.length > 0}
		<ul role="group">
			{#each node.children as childNode (childNode.id)}
				<svelte:self node={childNode} level={level + 1} on:selectNode />
			{/each}
		</ul>
	{/if}
</li>