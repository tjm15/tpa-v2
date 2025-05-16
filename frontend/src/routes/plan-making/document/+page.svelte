<script lang="ts">
	import ThreeZoneLayout from '$lib/components/layouts/ThreeZoneLayout.svelte';
	import DocumentNavigator from '$lib/components/document/DocumentNavigator.svelte';
	import DocumentEditorView from '$lib/components/document/DocumentEditorView.svelte';
	import DocumentIntegrityPanel from '$lib/components/document/DocumentIntegrityPanel.svelte';
</script>

<div class="h-full flex flex-col">
    <ThreeZoneLayout>
        <div slot="left-sidebar" class="h-full">
            <DocumentNavigator />
        </div>
        <div slot="central-panel" class="h-full bg-slate-50">
            <DocumentEditorView />
        </div>
        <div slot="right-sidebar" class="h-full bg-slate-50">
            <DocumentIntegrityPanel />
        </div>
    </ThreeZoneLayout>
</div>
