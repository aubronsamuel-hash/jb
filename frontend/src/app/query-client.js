import { QueryClient } from '@tanstack/react-query';

const defaultQueryOptions = {
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      gcTime: 15 * 60 * 1000
    }
  }
};

export function createAppQueryClient(overrides = {}) {
  const merged = {
    ...defaultQueryOptions,
    ...overrides,
    defaultOptions: {
      ...defaultQueryOptions.defaultOptions,
      ...(overrides.defaultOptions ?? {}),
      queries: {
        ...defaultQueryOptions.defaultOptions.queries,
        ...(overrides.defaultOptions?.queries ?? {})
      }
    }
  };
  return new QueryClient(merged);
}

export function primeQueryClient(client, entries = []) {
  entries.forEach(({ key, value }) => {
    if (key) {
      client.setQueryData(key, value);
    }
  });
  return client;
}

export const queryKeys = {
  dashboard: ['dashboard', 'stats'],
  planning: ['planning', 'calendar'],
  missions: ['missions', 'list'],
  teams: ['teams', 'people'],
  equipment: ['equipment', 'catalog'],
  budgets: ['budgets', 'summary'],
  notifications: ['notifications', 'timeline'],
  settings: ['settings', 'preferences']
};
