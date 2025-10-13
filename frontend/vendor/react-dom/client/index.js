export function createRoot(container) {
  const state = {
    container,
    lastRendered: null
  };
  return {
    render(node) {
      state.lastRendered = node;
      if (container) {
        container.__rendered = node;
      }
      return node;
    },
    getSnapshot() {
      return state.lastRendered;
    }
  };
}
