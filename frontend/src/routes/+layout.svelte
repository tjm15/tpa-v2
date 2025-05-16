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

	// Define Workspaces and their Modes
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

	onMount(() => {
		loadInitialData(); // Load mock data

		// Determine initial workspace and mode from URL
		const currentPath = $page.url.pathname;
		let foundWorkspace: ActiveWorkspace | null = null;
		let foundMode: ActiveMode | null = null;

		for (const ws of workspaces) {
			if (currentPath.startsWith(ws.hrefBase)) {
				foundWorkspace = ws.id;
				const mode = ws.modes.find(m => currentPath.startsWith(m.href));
				foundMode = mode ? mode.id : ws.defaultMode;
				break;
			}
		}

		if (foundWorkspace) {
			activeWorkspace.set(foundWorkspace);
			activeMode.set(foundMode);
		} else if (currentPath === '/' || currentPath.startsWith('/dashboard')) {
			activeWorkspace.set('dashboard');
			activeMode.set(null);
		} else {
            // If no match, redirect to dashboard or a default workspace
            goto('/dashboard', { replaceState: true });
            activeWorkspace.set('dashboard');
        }
	});

	// Update sub-navigation (modes) when workspace changes
	$: {
		const ws = workspaces.find(w => w.id === $activeWorkspace);
		currentWorkspaceModes = ws ? ws.modes : [];
	}

	// Update stores when SvelteKit navigation changes (e.g. browser back/forward)
	$: {
		const currentPath = $page.url.pathname;
		let newWs: ActiveWorkspace | null = null;
		let newMode: ActiveMode | null = null;

		if (currentPath === '/' || currentPath.startsWith('/dashboard')) {
			newWs = 'dashboard';
		} else {
			for (const wsDef of workspaces) {
				if (currentPath.startsWith(wsDef.hrefBase)) {
					newWs = wsDef.id;
					const modeDef = wsDef.modes.find(m => currentPath.startsWith(m.href));
					newMode = modeDef ? modeDef.id : wsDef.defaultMode;
					break;
				}
			}
		}
		
		if (newWs && $activeWorkspace !== newWs) {
			activeWorkspace.set(newWs);
		}
		if (newMode && $activeMode !== newMode && newWs !== 'dashboard') {
			activeMode.set(newMode);
		} else if (newWs === 'dashboard' && $activeMode !== null) {
            activeMode.set(null);
        }

	}

	function handleWorkspaceChange(wsId: ActiveWorkspace) {
		const newWsDef = workspaces.find(ws => ws.id === wsId);
		if (newWsDef) {
			setActiveWorkspace(newWsDef.id, newWsDef.defaultMode); // uiStateStore function
			goto(newWsDef.modes.find(m => m.id === newWsDef.defaultMode)?.href || newWsDef.hrefBase);
		} else if (wsId === 'dashboard') {
            setActiveWorkspace('dashboard', null);
            goto('/dashboard');
        }
	}

	function handleModeNavigation(href: string, modeId: ActiveMode) {
		setActiveModeInCurrentWorkspace(modeId); // uiStateStore function
		goto(href);
	}
</script>

<div class="flex flex-col h-screen bg-gray-100">
	<header class="bg-slate-800 text-white shadow-lg z-50">
		<div class="container mx-auto px-4">
			<div class="flex items-center justify-between h-16">
				<a href="/dashboard" class="text-2xl font-bold hover:text-slate-300 transition-colors"
					on:click|preventDefault={() => handleWorkspaceChange('dashboard')}>Planning Assistant</a
				>
				<nav class="flex items-center space-x-4">
					<button
						class="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-700 transition-colors {$activeWorkspace === 'dashboard' ? 'bg-slate-900' : ''}"
						on:click={() => handleWorkspaceChange('dashboard')}
					>
						Dashboard
					</button>
					{#each workspaces as ws (ws.id)}
						<button
							class="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-700 transition-colors {$activeWorkspace === ws.id ? 'bg-slate-900' : ''}"
							on:click={() => handleWorkspaceChange(ws.id)}
						>
							{ws.label}
						</button>
					{/each}
					<div class="ml-auto">
						<button class="p-2 rounded-md hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500">
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

	<div class="flex-1 overflow-auto">
		<slot /> </div>
</div>