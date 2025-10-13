import { queryKeys } from '../query-client.js';
import { createKpiCard, createModuleSummary, createRoleBadge } from '../design-system/index.js';
import { loadDashboardSnapshot } from '../api/dashboard-api.js';
import { createDashboardLayout } from '../components/dashboard-layout.js';

function computeSummary(snapshot) {
  const missions = snapshot.missions ?? [];
  const projects = snapshot.projects ?? [];
  const alerts = snapshot.alerts ?? [];
  const roleLoads = snapshot.roleLoads ?? snapshot.role_loads ?? [];
  const budgets = snapshot.budgets ?? [];

  const byStatus = missions.reduce((acc, mission) => {
    const status = mission.status ?? 'unknown';
    acc[status] = (acc[status] ?? 0) + 1;
    return acc;
  }, {});
  const missionsTotal = missions.length;
  const confirmedCount = byStatus.confirmed ?? 0;
  const confirmedRatio = missionsTotal ? Number(((confirmedCount / missionsTotal) * 100).toFixed(1)) : 0;
  const roleSummary = roleLoads.map((load) => {
    const allocated = load.allocated_hours ?? load.allocatedHours ?? 0;
    const available = load.available_hours ?? load.availableHours ?? 0;
    const utilization = available ? Number((allocated / available).toFixed(2)) : 0;
    return {
      role: load.role,
      allocatedHours: allocated,
      availableHours: available,
      utilization
    };
  });
  const budgetSummary = budgets.map((line) => {
    const planned = line.planned_amount ?? line.plannedAmount ?? 0;
    const actual = line.actual_amount ?? line.actualAmount ?? 0;
    return {
      projectId: line.project_id ?? line.projectId,
      planned,
      actual,
      delta: actual - planned
    };
  });

  return {
    generatedAt: snapshot.generatedAt ?? snapshot.generated_at,
    missions: { total: missionsTotal, byStatus, confirmedRatio },
    projects: { active: projects.filter((project) => project.status !== 'archived').length },
    alerts: { open: alerts.length, items: alerts },
    roleLoads: roleSummary,
    budgets: budgetSummary
  };
}

function buildKpiCards(summary) {
  const alertsOpen = summary.alerts.open;
  const confirmedRatio = summary.missions.confirmedRatio;
  const alertCaption = alertsOpen ? summary.alerts.items[0] : 'Aucune alerte ouverte';

  return [
    createKpiCard({
      id: 'kpi-missions-total',
      title: 'Missions totales',
      value: String(summary.missions.total),
      intent: 'info',
      trend: { direction: 'stable', delta: summary.missions.total }
    }),
    createKpiCard({
      id: 'kpi-missions-confirmed',
      title: 'Confirmations',
      value: `${confirmedRatio}%`,
      intent: confirmedRatio >= 50 ? 'success' : 'warning',
      trend: { direction: confirmedRatio >= 50 ? 'up' : 'down', delta: confirmedRatio }
    }),
    createKpiCard({
      id: 'kpi-alerts-open',
      title: 'Alertes ouvertes',
      value: String(alertsOpen),
      intent: alertsOpen ? 'warning' : 'success',
      trend: { direction: alertsOpen ? 'up' : 'down', delta: alertsOpen },
      caption: alertCaption
    })
  ];
}

function buildRoleBadges(summary) {
  return summary.roleLoads.map((load) => {
    const intensity = load.utilization >= 0.85 ? 'warning' : 'info';
    const tone = load.utilization >= 0.85 ? 'outline' : 'solid';
    const percentage = Math.round(load.utilization * 100);
    return createRoleBadge({
      id: `role-${load.role}`,
      role: load.role,
      label: `${load.role} ${percentage}%`,
      tone,
      intent: intensity
    });
  });
}

function buildModuleSummaries(summary) {
  const statuses = Object.entries(summary.missions.byStatus)
    .map(([status, count]) => `${status}: ${count}`)
    .join(', ');
  const roles = summary.roleLoads.map((load) => load.role);

  return [
    createModuleSummary({
      id: 'module-projects',
      title: 'Projets actifs',
      description: `${summary.projects.active} projets suivis`,
      roles: roles.slice(0, 3)
    }),
    createModuleSummary({
      id: 'module-planning',
      title: 'Planning missions',
      description: `Statuts: ${statuses}`,
      roles
    }),
    createModuleSummary({
      id: 'module-materiel',
      title: 'Materiel & logistique',
      description: summary.alerts.items[0] ?? 'Aucune alerte critique',
      roles: ['plateau', 'video']
    })
  ];
}

function buildAlertCards(summary) {
  return summary.alerts.items.map((alert, index) => ({
    id: `alert-${index + 1}`,
    type: 'dashboard-alert',
    severity: alert.includes('Budget') ? 'warning' : 'info',
    message: alert
  }));
}

export function DashboardView({ heading = 'Dashboard', snapshot = null, summary = null } = {}) {
  const effectiveSnapshot = snapshot ?? loadDashboardSnapshot();
  const computedSummary = summary ?? computeSummary(effectiveSnapshot);
  const kpis = buildKpiCards(computedSummary);
  const roleBadges = buildRoleBadges(computedSummary);
  const modules = buildModuleSummaries(computedSummary);
  const alerts = buildAlertCards(computedSummary);
  const layout = createDashboardLayout({ heading, kpis, roleBadges, modules, alerts });

  return {
    type: 'dashboard-view',
    id: 'dashboard',
    heading,
    summary: computedSummary,
    queryKey: queryKeys.dashboard,
    designSystem: {
      layout,
      kpis,
      roleBadges,
      modules,
      alerts
    }
  };
}

export function initializeDashboardView(options = {}) {
  const heading = options.heading ?? 'Dashboard';
  const snapshot = options.snapshot ?? loadDashboardSnapshot();
  const summary = computeSummary(snapshot);
  return DashboardView({ heading, snapshot, summary });
}
