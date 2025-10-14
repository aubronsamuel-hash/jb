export const appNavigation = [
  {
    id: 'dashboard',
    label: 'Tableau de bord',
    path: '/',
    description: 'Vue synthetique des missions, equipes et alertes du jour.',
    icon: 'Gauge',
    guard: 'authenticated',
    badges: [{ label: 'Overview', tone: 'info' }]
  },
  {
    id: 'planning',
    label: 'Planning',
    path: '/planning',
    description: 'Gestion hebdomadaire des affectations et rotations.',
    icon: 'CalendarRange',
    guard: 'authenticated',
    badges: [{ label: 'Equipe terrain', tone: 'success' }]
  },
  {
    id: 'missions',
    label: 'Missions',
    path: '/missions',
    description: 'Pilotage des missions en cours et preparation des prochaines.',
    icon: 'MapPinned',
    guard: 'authenticated',
    badges: [{ label: 'Live', tone: 'warning' }]
  },
  {
    id: 'notifications',
    label: 'Notifications',
    path: '/notifications',
    description: 'Historique et preferences de diffusion des alertes.',
    icon: 'Bell',
    guard: 'authenticated',
    badges: [{ label: 'Canaux', tone: 'info' }]
  },
  {
    id: 'teams',
    label: 'Equipes',
    path: '/equipes',
    description: 'Referentiel des membres et competences en coulisses.',
    icon: 'Users',
    guard: 'authenticated',
    badges: [{ label: 'HR', tone: 'neutral' }]
  },
  {
    id: 'equipment',
    label: 'Materiel',
    path: '/materiel',
    description: 'Inventaire du materiel technique et disponibilite.',
    icon: 'Package',
    guard: 'authenticated',
    badges: [{ label: 'Stock', tone: 'info' }]
  },
  {
    id: 'budgets',
    label: 'Budgets',
    path: '/budgets',
    description: 'Suivi des couts missions et allocations par equipe.',
    icon: 'Wallet',
    guard: 'authenticated',
    badges: [{ label: 'Finance', tone: 'neutral' }]
  },
  {
    id: 'settings',
    label: 'Parametres',
    path: '/parametres',
    description: 'Configuration de l espace Coulisses Crew et preferences.',
    icon: 'Settings',
    guard: 'authenticated',
    badges: [{ label: 'Admin', tone: 'danger' }]
  }
];

export function findNavigationItem(id) {
  return appNavigation.find((item) => item.id === id);
}
