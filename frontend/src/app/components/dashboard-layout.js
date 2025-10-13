const DEFAULT_ASCII_LAYOUT = [
  '+----------------+----------------+',
  '|    header      |    header      |',
  '+----------------+----------------+',
  '|      kpis      |      kpis      |',
  '+----------------+----------------+',
  '|   role-loads   |    modules     |',
  '+----------------+----------------+',
  '|    alerts      |    modules     |',
  '+----------------+----------------+'
].join('\n');

export function createDashboardLayout(config = {}) {
  const heading = config.heading ?? 'Dashboard Orga';
  const kpis = config.kpis ?? [];
  const roleBadges = config.roleBadges ?? [];
  const modules = config.modules ?? [];
  const alerts = config.alerts ?? [];

  return {
    type: 'dashboard-layout',
    heading,
    grid: [
      ['header', 'header'],
      ['kpis', 'kpis'],
      ['roles', 'modules'],
      ['alerts', 'modules']
    ],
    ascii: DEFAULT_ASCII_LAYOUT,
    sections: {
      header: {
        type: 'dashboard-header',
        title: heading,
        alerts: alerts.length
      },
      kpis,
      roles: roleBadges,
      modules,
      alerts
    }
  };
}
