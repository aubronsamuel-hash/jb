export function createDashboardPage(theme) {
  return {
    type: 'dashboard-page',
    hero: {
      title: 'Vue generale Coulisses Crew',
      description:
        'Synthese du jour : missions actives, equipes en coulisses et niveau de stress des operations.'
    },
    widgets: [
      {
        id: 'missions-today',
        title: 'Missions du jour',
        description: '3 missions en cours · 1 mission en preparation',
        tone: 'info'
      },
      {
        id: 'staffing',
        title: 'Equipes terrain',
        description: '92% des postes critiques couverts',
        tone: 'success'
      },
      {
        id: 'alerts',
        title: 'Alertes critiques',
        description: '1 alerte logistique a traiter rapidement',
        tone: 'warning'
      }
    ],
    accessibility: {
      headingLevel: 1,
      regionLabel: `Tableau de bord ${theme.mode}`
    }
  };
}
