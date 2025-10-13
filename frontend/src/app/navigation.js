export const appNavigation = [
  { id: 'dashboard', label: 'Dashboard', path: '/', description: 'Vue d ensemble KPI et evenements' },
  { id: 'planning', label: 'Planning', path: '/planning', description: 'Planning jour/semaine/mois' },
  { id: 'missions', label: 'Missions', path: '/missions', description: 'Gestion des missions et statuts' },
  { id: 'teams', label: 'Equipes', path: '/equipes', description: 'Intermittents, disponibilites et pool' },
  { id: 'equipment', label: 'Materiel', path: '/materiel', description: 'Catalogue, logistique, fournisseurs' },
  { id: 'budgets', label: 'Budgets', path: '/budgets', description: 'Suivi budgetaire et analytics' },
  { id: 'notifications', label: 'Notifications', path: '/notifications', description: 'Regles email/Telegram et historique' },
  { id: 'settings', label: 'Parametres', path: '/parametres', description: 'Templates, roles, integrations' }
];

export function findNavigationItem(id) {
  return appNavigation.find((item) => item.id === id) ?? null;
}

export function listNavigationPaths() {
  return appNavigation.map((item) => item.path);
}

export function createNavigationMap() {
  return Object.fromEntries(appNavigation.map((item) => [item.id, item]));
}
