<script lang="ts">
	import '../app.css'; // Global styles
	import {
		activeWorkspace,
		activeMode,
		setActiveWorkspace,
		setActiveModeInCurrentWorkspace
	} from '$lib/stores/uiStateStore';
	import { loadInitialData } from '$lib/stores/mainDataStore';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import type { ActiveWorkspace, PlanMakingMode, DevelopmentManagementMode, ActiveMode } from '$lib/types/models';

	export let data: { initialWorkspace: ActiveWorkspace, initialMode: ActiveMode };

	// Workspace definitions (can stay here or be imported if shared with +layout.ts carefully)
	interface ModeDefinition {
		id: PlanMakingMode | DevelopmentManagementMode;
		label: string;
		href: string;
	}
	interface WorkspaceDefinition {
		id: ActiveWorkspace;
		label: string;
		hrefBase: string;
		modes: ModeDefinition[];
		defaultMode: PlanMakingMode | DevelopmentManagementMode;
	}

	const workspaces: WorkspaceDefinition[] = [
		{
			id: 'plan-making',
			label: 'Plan Production',
			hrefBase: '/plan-making',
			defaultMode: 'policy',
			modes: [
				{ id: 'policy', label: 'Policy', href: '/plan-making/policy' },
				{ id: 'site-allocation', label: 'Site Allocation', href: '/plan-making/site-allocation' },
				{ id: 'scenario', label: 'Scenario', href: '/plan-making/scenario' },
				{ id: 'goal-tracker', label: 'Goal Tracker', href: '/plan-making/goal-tracker' },
				{ id: 'document', label: 'Document', href: '/plan-making/document' }
			]
		},
		{
			id: 'development-management',
			label: 'Development Management',
			hrefBase: '/dev-management',
			defaultMode: 'dm-site-assessment',
			modes: [
				{ id: 'dm-site-assessment', label: 'Site Assessment', href: '/dev-management/assessment' },
				{ id: 'dm-reasoning', label: 'Reasoning', href: '/dev-management/reasoning' },
				{ id: 'dm-precedent-review', label: 'Precedent Review', href: '/dev-management/precedents' },
				{ id: 'dm-report-generation', label: 'Report Generation', href: '/dev-management/report' }
			]
		}
	];

	let currentWorkspaceModes: ModeDefinition[] = [];
	let dataLoaded = false;

	onMount(() => {
		if (!dataLoaded) {
			loadInitialData();
			dataLoaded = true;
		}
		if (data.initialWorkspace !== $activeWorkspace || data.initialMode !== $activeMode) {
			setActiveWorkspace(data.initialWorkspace, data.initialMode);
		}
	});

	$: {
		if ($page.data.initialWorkspace !== undefined && $page.data.initialMode !== undefined) {
			if ($page.data.initialWorkspace !== $activeWorkspace || $page.data.initialMode !== $activeMode) {
				setActiveWorkspace($page.data.initialWorkspace, $page.data.initialMode);
			}
		}
	}

	$: {
		const ws = workspaces.find(w => w.id === $activeWorkspace);
		currentWorkspaceModes = ws ? ws.modes : [];
	}

	function handleWorkspaceNavigation(targetWorkspaceId: ActiveWorkspace) {
		const targetWsDef = workspaces.find(ws => ws.id === targetWorkspaceId);
		if (targetWsDef) {
			const targetHref = targetWsDef.modes.find(m => m.id === targetWsDef.defaultMode)?.href || targetWsDef.hrefBase;
			goto(targetHref);
		} else if (targetWorkspaceId === 'dashboard') {
			goto('/dashboard');
		}
	}

	function handleModeNavigation(href: string, modeId: ActiveMode) {
		goto(href);
	}
</script>

<div class="flex flex-col h-screen bg-gray-100">
	<header class="bg-slate-800 text-white shadow-lg z-50 shrink-0">
		<div class="container mx-auto px-4">
			<div class="flex items-center justify-between h-16">
				<a href="/dashboard" class="text-2xl font-bold hover:text-slate-300 transition-colors"
					on:click|preventDefault={() => handleWorkspaceNavigation('dashboard')}>The Planner's Assistant</a
				>
				<nav class="flex items-center space-x-4">
					<button
						class:bg-slate-900={$activeWorkspace === 'dashboard'}
						class="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-700 transition-colors"
						on:click={() => handleWorkspaceNavigation('dashboard')}
					>
						Dashboard
					</button>
					{#each workspaces as ws (ws.id)}
						<button
							class:bg-slate-900={$activeWorkspace === ws.id}
							class="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-700 transition-colors"
							on:click={() => handleWorkspaceNavigation(ws.id)}
						>
							{ws.label}
						</button>
					{/each}
					<div class="ml-auto">
						<button
							class="p-2 rounded-md hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500"
							aria-label="Search site-wide"  title="Search site-wide"       >
							<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
								<path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
							  </svg>
						</button>
					</div>
				</nav>
			</div>
			{#if $activeWorkspace && $activeWorkspace !== 'dashboard' && currentWorkspaceModes.length > 0}
				<div class="bg-slate-700">
					<nav class="container mx-auto px-4 flex items-center space-x-2 h-12">
						{#each currentWorkspaceModes as mode (mode.id)}
							<a
								href={mode.href}
								class="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-600 transition-colors {$activeMode === mode.id ? 'bg-slate-900 text-white' : 'text-slate-300 hover:text-white'}"
								on:click|preventDefault={() => handleModeNavigation(mode.href, mode.id)}
							>
								{mode.label}
							</a>
						{/each}
					</nav>
				</div>
			{/if}
		</div>
	</header>

	<div class="flex-1 min-h-0 flex flex-col">
		{#key $page.url.pathname}
			<slot />
		{/key}
	</div>
</div>