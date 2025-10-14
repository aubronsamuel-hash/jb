import { QueryClient } from '@tanstack/react-query';

export const queryKeys = {
  dashboard: ['dashboard', 'overview'],
  planning: ['planning', 'week'],
  missions: ['missions', 'list'],
  notifications: ['notifications', 'inbox'],
  teams: ['teams', 'roster'],
  equipment: ['equipment', 'inventory'],
  budgets: ['budgets', 'summary'],
  settings: ['settings', 'preferences']
};

export function createAppQueryClient(config = {}) {
  return new QueryClient({
    defaultOptions: {
      queries: {
        cacheTime: config.cacheTime ?? 1000 * 60 * 5,
        staleTime: config.staleTime ?? 1000 * 30
      }
    }
  });
}

export function primeQueryClient(client, entries) {
  entries.forEach((entry) => {
    client.setQueryData(entry.key, entry.value);
  });
}
