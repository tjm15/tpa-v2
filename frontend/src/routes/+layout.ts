// frontend/src/routes/+layout.ts
import type { LayoutLoad } from './$types';
import type { ActiveWorkspace, ActiveMode, PlanMakingMode, DevelopmentManagementMode } from '$lib/types/models';

interface ModeDefinitionForLoad {
    id: PlanMakingMode | DevelopmentManagementMode;
    href: string;
}
interface WorkspaceDefinitionForLoad {
    id: ActiveWorkspace;
    hrefBase: string;
    modes: ModeDefinitionForLoad[];
    defaultMode: PlanMakingMode | DevelopmentManagementMode;
}

const workspacesConfig: WorkspaceDefinitionForLoad[] = [
    { id: 'plan-making', hrefBase: '/plan-making', defaultMode: 'policy', modes: [
        { id: 'policy', href: '/plan-making/policy' },
        { id: 'site-allocation', href: '/plan-making/site-allocation' },
        { id: 'scenario', href: '/plan-making/scenario' },
        { id: 'goal-tracker', href: '/plan-making/goal-tracker' },
        { id: 'document', href: '/plan-making/document' }
    ] },
    { id: 'development-management', hrefBase: '/dev-management', defaultMode: 'dm-site-assessment', modes: [
        { id: 'dm-site-assessment', href: '/dev-management/assessment' },
        { id: 'dm-reasoning', href: '/dev-management/reasoning' },
        { id: 'dm-precedent-review', href: '/dev-management/precedents' },
        { id: 'dm-report-generation', href: '/dev-management/report' }
    ] }
];

export const load: LayoutLoad = ({ url }) => {
    const currentPath = url.pathname;
    let initialWorkspace: ActiveWorkspace = 'dashboard';
    let initialMode: ActiveMode = null;

    for (const wsDef of workspacesConfig) {
        if (currentPath.startsWith(wsDef.hrefBase)) {
            initialWorkspace = wsDef.id;
            const modeDef = wsDef.modes.find(m => currentPath.startsWith(m.href));
            initialMode = modeDef ? modeDef.id : wsDef.defaultMode;
            break;
        }
    }
    if (initialWorkspace === 'dashboard') {
        initialMode = null;
    } else if (initialWorkspace === null && currentPath !== '/' && !currentPath.startsWith('/dashboard')) {
        initialWorkspace = 'dashboard';
        initialMode = null;
    }
    return {
        initialWorkspace,
        initialMode
    };
};
