const cacheKey = (key) => JSON.stringify(key ?? []);

export class QueryClient {
  constructor(options = {}) {
    this.options = options;
    this.cache = new Map();
  }

  getQueryData(key) {
    return this.cache.get(cacheKey(key));
  }

  setQueryData(key, value) {
    this.cache.set(cacheKey(key), value);
    return value;
  }
}

export function QueryClientProvider({ client, children }) {
  client.__children = children ?? [];
  return {
    type: 'query-client-provider',
    client,
    children: children ?? []
  };
}

export function useQuery(options) {
  if (!options || typeof options.queryFn !== 'function') {
    throw new Error('queryFn must be provided');
  }
  const key = options.queryKey ?? 'default';
  const cached = options.client?.getQueryData?.(key);
  if (cached !== undefined) {
    return {
      data: cached,
      status: 'success',
      isLoading: false,
      isError: false
    };
  }
  const result = options.queryFn();
  if (options.client?.setQueryData) {
    options.client.setQueryData(key, result);
  }
  return {
    data: result,
    status: 'success',
    isLoading: false,
    isError: false
  };
}

export function useMutation(config = {}) {
  const mutate = async (variables) => {
    if (typeof config.mutationFn === 'function') {
      return config.mutationFn(variables);
    }
    return variables;
  };
  return {
    mutate,
    status: 'success'
  };
}

export const useQueryClient = (client) => client;
