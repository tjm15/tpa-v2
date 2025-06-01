<script lang="ts">
	import { planDocuments as allPlanDocumentsStore, findDocumentNode } from '$lib/stores/mainDataStore';
	import { selectedDocumentId, selectedDocumentNodeId } from '$lib/stores/uiStateStore';
	import type { DocumentNode, PlanDocument } from '$types/models';
	import Card from '$lib/components/common/Card.svelte';
	import Button from '$lib/components/common/Button.svelte';
	import { get } from 'svelte/store';

    let currentDocument: PlanDocument | undefined | null = null;
	let currentNode: DocumentNode | undefined | null = null;

	$: {
        currentDocument = $selectedDocumentId ? get(allPlanDocumentsStore).find(d => d.id === $selectedDocumentId) : null;
		currentNode = currentDocument && $selectedDocumentNodeId ? findDocumentNode(currentDocument, $selectedDocumentNodeId) : null;
	}

    function exportDocument(format: 'PDF' | 'DOCX' | 'JSON') {
        if (!currentDocument) return;
        alert(`Exporting '${currentDocument.name}' as ${format} (mock feature).`);
        if (format === 'JSON') {
            console.log(JSON.stringify(currentDocument, null, 2));
        }
    }
</script>

<div class="p-1 md:p-2 space-y-3 overflow-y-auto h-full text-sm">
    {#if currentNode && currentDocument}
        <Card title="Unresolved Issues">
            {#if currentNode.unresolvedIssues && currentNode.unresolvedIssues.length > 0}
                <ul class="list-disc list-inside text-xs text-red-600 space-y-1">
                    {#each currentNode.unresolvedIssues as issue}
                        <li>{issue}</li>
                    {/each}
                </ul>
            {:else}
                <p class="text-xs text-gray-500">No unresolved issues noted for this section.</p>
            {/if}
        </Card>

        <Card title="Linked Entities">
             {#if currentNode.linkedEntities && currentNode.linkedEntities.length > 0}
                <ul class="space-y-1">
                    {#each currentNode.linkedEntities as entity (entity.id)}
                        <li class="p-1.5 border rounded flex justify-between items-center text-xs hover:bg-gray-50">
                           <span>{entity.name} <span class="text-gray-400">({entity.type})</span></span>
                           <Button size="sm" variant="ghost">View</Button>
                        </li>
                    {/each}
                </ul>
            {:else}
                <p class="text-xs text-gray-500">No entities directly linked in this section's metadata.</p>
                 <p class="text-xs text-gray-400 mt-1"> (Example: Policy H1, Site SA002, NPPF §60)</p>
            {/if}
        </Card>

        <Card title="Export Options (Full Document)">
            <div class="space-y-2">
                <Button on:click={() => exportDocument('PDF')} fullWidth variant="secondary">Generate PDF (Mock)</Button>
                <Button on:click={() => exportDocument('DOCX')} fullWidth variant="secondary">Generate DOCX (Mock)</Button>
                <Button on:click={() => exportDocument('JSON')} fullWidth variant="secondary">Export JSON (Mock)</Button>
            </div>
            <p class="text-xs text-gray-500 mt-2">
                For consultation, inspection, or legal submission.
            </p>
        </Card>
    {:else if currentDocument}
        <Card title="Export Options (Full Document)">
            <div class="space-y-2">
                <Button on:click={() => exportDocument('PDF')} fullWidth variant="secondary">Generate PDF (Mock)</Button>
                <Button on:click={() => exportDocument('DOCX')} fullWidth variant="secondary">Generate DOCX (Mock)</Button>
                <Button on:click={() => exportDocument('JSON')} fullWidth variant="secondary">Export JSON (Mock)</Button>
            </div>
        </Card>
        <div class="flex items-center justify-center h-1/2 p-4 text-center">
			<p class="text-gray-500">Select a section from the document navigator to see its details.</p>
		</div>
    {:else}
         <div class="flex items-center justify-center h-full p-10 text-center">
			<p class="text-gray-500">Select a document to manage.</p>
		</div>
    {/if}
</div>