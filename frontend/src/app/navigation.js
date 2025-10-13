import { createRoleBadge } from './design-system/index.js';

const navigationRoleAssignments = {
  dashboard: ['production', 'admin'],
  planning: ['production', 'lumiere', 'son'],
  missions: ['production', 'lumiere', 'son', 'video'],
  teams: ['production', 'admin', 'hmc'],
  equipment: ['plateau', 'video'],
  budgets: ['admin', 'production'],
  notifications: ['admin'],
  settings: ['admin', 'production']
};

function ensureNavigationRoles(navigation, roleAssignments = navigationRoleAssignments) {
  return navigation.map((item) => {
    const roles = Array.isArray(item.roles) && item.roles.length > 0
      ? item.roles
      : roleAssignments[item.id] ?? [];
    return { ...item, roles };
  });
}

const baseNavigation = [
  { id: 'dashboard', label: 'Dashboard', path: '/', description: 'Vue d ensemble KPI et evenements' },
  { id: 'planning', label: 'Planning', path: '/planning', description: 'Planning jour/semaine/mois' },
  { id: 'missions', label: 'Missions', path: '/missions', description: 'Gestion des missions et statuts' },
  { id: 'teams', label: 'Equipes', path: '/equipes', description: 'Intermittents, disponibilites et pool' },
  { id: 'equipment', label: 'Materiel', path: '/materiel', description: 'Catalogue, logistique, fournisseurs' },
  { id: 'budgets', label: 'Budgets', path: '/budgets', description: 'Suivi budgetaire et analytics' },
  { id: 'notifications', label: 'Notifications', path: '/notifications', description: 'Regles email/Telegram et historique' },
  { id: 'settings', label: 'Parametres', path: '/parametres', description: 'Templates, roles, integrations' }
];

export const appNavigation = ensureNavigationRoles(baseNavigation);

export function findNavigationItem(id) {
  return appNavigation.find((item) => item.id === id) ?? null;
}

export function listNavigationPaths() {
  return appNavigation.map((item) => item.path);
}

export function createNavigationMap() {
  return Object.fromEntries(appNavigation.map((item) => [item.id, item]));
}

export function createNavigationRoleBadges(options = {}) {
  const navigation = ensureNavigationRoles(options.navigation ?? appNavigation);
  const theme = options.theme ?? null;
  return navigation.map((item) => ({
    id: `${item.id}-role-badges`,
    target: item.id,
    badges: item.roles.map((role) => createRoleBadge({ role, tone: 'outline', theme }))
  }));
}
