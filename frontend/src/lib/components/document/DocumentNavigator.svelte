<script lang="ts">
    import { planDocuments as allPlanDocumentsStore } from '$lib/stores/mainDataStore';
	import { selectedDocumentId, selectedDocumentNodeId } from '$lib/stores/uiStateStore';
	import type { PlanDocument, DocumentNode } from '$types/models';
	import SearchFilterInput from '$lib/components/common/SearchFilterInput.svelte'; // If needed for searching nodes
	import DocumentNodeTreeItem from './DocumentNodeTreeItem.svelte';
    import { get } from 'svelte/store';
    import { onMount } from 'svelte';

    let currentDocument: PlanDocument | undefined | null = null;
    let documentRootNodes: DocumentNode[] = [];

    onMount(() => {
        // If no document selected, pick the first one from the store
        if (!$selectedDocumentId && get(allPlanDocumentsStore).length > 0) {
            selectedDocumentId.set(get(allPlanDocumentsStore)[0].id);
        }
    });

    function getDocumentById(id: string): PlanDocument | undefined {
        return get(allPlanDocumentsStore).find((doc) => doc.id === id);
    }

    $: {
        if ($selectedDocumentId) {
            currentDocument = getDocumentById($selectedDocumentId);
            documentRootNodes = currentDocument?.rootNode?.children || (currentDocument?.rootNode ? [currentDocument.rootNode] : []);
        } else {
            currentDocument = null;
            documentRootNodes = [];
        }
    }

    function handleNodeSelectedInTree(event: CustomEvent<string>) {
        // selectedDocumentNodeId is already set by DocumentNodeTreeItem
        console.log('Node selected in tree:', event.detail);
    }
</script>

<div class="flex flex-col h-full">
	<div class="p-4 border-b border-gray-200">
		<h2 class="text-lg font-semibold text-gray-800">Document Navigator</h2>
        {#if $allPlanDocumentsStore.length > 0}
        <div class="mt-2">
            <label for="document-mode-select" class="block text-sm font-medium text-gray-700 mb-1">Select Document:</label>
            <select id="document-mode-select" bind:value={$selectedDocumentId} class="w-full p-2 border border-gray-300 rounded-md text-sm shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500">
                {#each $allPlanDocumentsStore as doc (doc.id)}
                    <option value={doc.id}>{doc.name} ({doc.type})</option>
                {/each}
            </select>
        </div>
        {:else}
        <p class="text-sm text-gray-500 mt-2">No documents loaded.</p>
        {/if}
	</div>
    <div class="flex-1 overflow-y-auto p-2">
		{#if currentDocument && documentRootNodes.length > 0}
			<ul role="tree" aria-label="{currentDocument.name} structure">
                {#each documentRootNodes as rootChildNode (rootChildNode.id)}
				    <DocumentNodeTreeItem node={rootChildNode} level={0} on:selectNode={handleNodeSelectedInTree} />
                {/each}
			</ul>
		{:else if currentDocument}
            <p class="p-4 text-sm text-gray-500">Document '{currentDocument.name}' has no structure defined or is empty.</p>
        {:else}
             <p class="p-4 text-sm text-gray-500">Select a document to view its structure.</p>
        {/if}
	</div>
</div>