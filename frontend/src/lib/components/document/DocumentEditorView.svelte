<script lang="ts">
	import { planDocuments as allPlanDocumentsStore, findDocumentNode } from '$lib/stores/mainDataStore';
	import { selectedDocumentId, selectedDocumentNodeId } from '$lib/stores/uiStateStore';
	import type { DocumentNode, PlanDocument } from '$types/models';
	import Card from '$lib/components/common/Card.svelte';
	import ContentDisplayEditor from '$lib/components/editor/ContentDisplayEditor.svelte'; // Use the stubbed editor
	import Button from '$lib/components/common/Button.svelte';
	import { get } from 'svelte/store';

	let currentDocument: PlanDocument | undefined | null = null;
    let currentNode: DocumentNode | undefined | null = null;
    let breadcrumbs: { id: string, title: string }[] = [];
    let editableContent: string = '';
    let editMode = false; // For View/Edit toggle

	$: {
        currentDocument = $selectedDocumentId ? get(allPlanDocumentsStore).find(d => d.id === $selectedDocumentId) : null;
		if (currentDocument && $selectedDocumentNodeId) {
			currentNode = findDocumentNode(currentDocument, $selectedDocumentNodeId); // Implement findDocumentNode in mainDataStore
            editableContent = currentNode?.content || '';

            // Build breadcrumbs
            let path: { id: string, title: string }[] = [];
            if (currentNode && currentDocument?.rootNode) {
                function findPath(node: DocumentNode, targetId: string, currentPath: {id:string, title:string}[]): boolean {
                    currentPath.push({id: node.id, title: node.title});
                    if (node.id === targetId) return true;
                    if (node.children) {
                        for (const child of node.children) {
                            if (findPath(child, targetId, currentPath)) return true;
                        }
                    }
                    currentPath.pop();
                    return false;
                }
                if (currentDocument.rootNode.id === $selectedDocumentNodeId) { // If root node itself is selected
                     path.push({id: currentDocument.rootNode.id, title: currentDocument.rootNode.title});
                } else if (currentDocument.rootNode.children) {
                    for (const child of currentDocument.rootNode.children) {
                        if (findPath(child, $selectedDocumentNodeId, path)) break;
                        path = []; // Reset if not found in this branch
                    }
                }
            }
            breadcrumbs = path;

		} else {
			currentNode = null;
            breadcrumbs = [];
            editableContent = '';
		}
	}

    function saveContent() {
        if (!currentNode || !currentDocument) return;
        // This is tricky: updating a node in a nested structure in a Svelte store
        // For a real app, you'd likely have an API call or more sophisticated store methods.
        // For mock, we'll try to update it in place (may not trigger reactivity perfectly everywhere without store.set)
        const updateNodeInTree = (nodes: DocumentNode[] | undefined, nodeId: string, newContent: string): boolean => {
            if (!nodes) return false;
            for (let i = 0; i < nodes.length; i++) {
                if (nodes[i].id === nodeId) {
                    nodes[i] = { ...nodes[i], content: newContent, lastModified: new Date().toISOString() };
                    return true;
                }
                if (updateNodeInTree(nodes[i].children, nodeId, newContent)) return true;
            }
            return false;
        }
        
        const docIndex = get(allPlanDocumentsStore).findIndex(d => d.id === currentDocument?.id);
        if (docIndex !== -1) {
            let docToUpdate = JSON.parse(JSON.stringify(get(allPlanDocumentsStore)[docIndex])); // Deep clone for modification
             if (updateNodeInTree(docToUpdate.rootNode.children || (docToUpdate.rootNode ? [docToUpdate.rootNode] : []), $selectedDocumentNodeId!, editableContent)) {
                allPlanDocumentsStore.update(docs => {
                    docs[docIndex] = docToUpdate;
                    return [...docs]; // Force reactivity
                });
                currentNode = findDocumentNode(docToUpdate, $selectedDocumentNodeId!); // Re-assign to get updated lastModified
                editMode = false;
                alert('Content saved (mock)!');
            } else {
                alert('Failed to find node to update (mock).');
            }
        }
    }
</script>

<div class="p-4 md:p-6 h-full flex flex-col">
	{#if currentNode && currentDocument}
		<Card additionalClasses="flex-1 flex flex-col min-h-0">
            <svelte:fragment slot="title">
                <div class="flex justify-between items-center">
                    <div>
                        <nav aria-label="Breadcrumb" class="text-xs text-gray-500 mb-1">
                            <ol class="list-none p-0 inline-flex">
                                <li class="flex items-center">
                                    <span class="hover:text-gray-700">{currentDocument.name}</span>
                                </li>
                                {#each breadcrumbs as crumb, i (crumb.id)}
                                <li class="flex items-center">
                                    <svg class="fill-current w-3 h-3 mx-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/></svg>
                                    {#if i === breadcrumbs.length - 1}
                                        <span class="font-semibold text-gray-700">{crumb.title}</span>
                                    {:else}
                                        <span>{crumb.title}</span>
                                    {/if}
                                </li>
                                {/each}
                            </ol>
                        </nav>
                        <h2 class="text-xl font-bold text-gray-800">
                            {currentNode.reference ? `${currentNode.reference}: ` : ''}{currentNode.title}
                        </h2>
                    </div>
                    <div class="space-x-2">
                        <Button size="sm" variant={editMode ? "secondary" : "primary"} on:click={() => editMode = !editMode}>
                            {editMode ? 'View Mode' : 'Edit Content'}
                        </Button>
                        {#if editMode}
                             <Button size="sm" variant="primary" on:click={saveContent}>Save</Button>
                        {/if}
                    </div>
                </div>
            </svelte:fragment>
            
            <div class="flex-1 overflow-y-auto p-3 md:p-4 min-h-0 prose max-w-none">
                {#if editMode}
                    <ContentDisplayEditor bind:value={editableContent} rows={20} />
                {:else}
                    <div class="p-2 border rounded bg-gray-50 min-h-[100px] whitespace-pre-wrap">
                        {@html currentNode.content || '<p class="italic text-gray-400">No content for this section.</p>'}
                    </div>
                {/if}
            </div>
            <div class="text-xs text-gray-400 p-2 border-t text-right">
                Last Modified: {currentNode.lastModified ? new Date(currentNode.lastModified).toLocaleString() : 'N/A'}
                {#if currentNode.author} by {currentNode.author}{/if}
            </div>
		</Card>
	{:else}
		<div class="flex items-center justify-center h-full">
			<p class="text-gray-500 p-10 text-center">Select a document and a section from the navigator to view or edit.</p>
		</div>
	{/if}
</div>