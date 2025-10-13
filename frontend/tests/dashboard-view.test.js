import { describe, expect, it } from 'vitest';

import { initializeDashboardView } from '../src/app/views/dashboard-view.js';

describe('dashboard view', () => {
  it('builds a dashboard view with KPIs, role badges and module summaries', () => {
    const view = initializeDashboardView();

    expect(view.type).toBe('dashboard-view');
    expect(view.summary.missions.total).toBe(4);
    expect(view.summary.missions.byStatus.confirmed).toBe(1);
    expect(view.summary.alerts.open > 0).toBe(true);

    const { designSystem } = view;
    expect(designSystem.kpis.length).toBe(3);
    expect(designSystem.roleBadges.length >= 3).toBe(true);
    expect(designSystem.modules.length).toBe(3);
    expect(designSystem.alerts.length).toBe(view.summary.alerts.open);

    const layout = designSystem.layout;
    expect(layout.type).toBe('dashboard-layout');
    expect(layout.sections.header.alerts).toBe(view.summary.alerts.open);
    expect(layout.ascii.indexOf('header') >= 0).toBe(true);
  });
});
