import { queryKeys } from '../query-client.js';
import { createKpiCard, createModuleSummary } from '../design-system/index.js';

function createDefaultKpis() {
  return [
    createKpiCard({ id: 'hours', title: 'Heures semaine', value: '48', unit: 'h', intent: 'success', trend: { direction: 'up', delta: 4 } }),
    createKpiCard({ id: 'projects', title: 'Projets actifs', value: '4', intent: 'info', trend: { direction: 'stable', delta: 0 } }),
    createKpiCard({ id: 'crew', title: 'Equipe mobilisee', value: '22', unit: 'pers', intent: 'warning', trend: { direction: 'down', delta: 2 } })
  ];
}

function createDefaultModuleSummary() {
  return createModuleSummary({
    id: 'day-operations',
    title: 'Missions du jour',
    description: 'Vue synthetique des assignments quotidiens',
    roles: ['lumiere', 'son', 'video', 'plateau']
  });
}

export function DashboardView({ heading = 'Dashboard', summary = null, design = null }) {
  const metrics = summary ?? {
    missionsToday: 0,
    activeProjects: 0,
    pendingNotifications: 0
  };
  return {
    type: 'dashboard-view',
    id: 'dashboard',
    heading,
    summary: metrics,
    queryKey: queryKeys.dashboard,
    designSystem: design ?? {
      cards: createDefaultKpis(),
      moduleSummary: createDefaultModuleSummary()
    }
  };
}
