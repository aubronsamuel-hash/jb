export function create(createState) {
  const listeners = new Set();
  const store = {
    state: undefined,
    setState(updater, replace = false) {
      const nextState =
        typeof updater === 'function' ? updater(store.state) : updater;
      if (replace) {
        store.state = nextState;
      } else {
        store.state = { ...store.state, ...nextState };
      }
      listeners.forEach((listener) => listener(store.state));
      return store.state;
    },
    getState() {
      return store.state;
    },
    subscribe(listener) {
      listeners.add(listener);
      return () => listeners.delete(listener);
    }
  };

  store.state = createState(store.setState.bind(store), store.getState.bind(store), {
    setState: store.setState.bind(store),
    getState: store.getState.bind(store),
    subscribe: store.subscribe.bind(store)
  });

  function useStore() {
    return store.state;
  }

  useStore.getState = store.getState.bind(store);
  useStore.setState = store.setState.bind(store);
  useStore.subscribe = store.subscribe.bind(store);
  useStore.api = store;

  return useStore;
}
