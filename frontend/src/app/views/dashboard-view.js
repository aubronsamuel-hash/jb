import { queryKeys } from '../query-client.js';

export function DashboardView({ heading = 'Dashboard', summary = null }) {
  return {
    type: 'dashboard-view',
    id: 'dashboard',
    heading,
    summary: summary ?? {
      missionsToday: 0,
      activeProjects: 0,
      pendingNotifications: 0
    },
    queryKey: queryKeys.dashboard
  };
}
