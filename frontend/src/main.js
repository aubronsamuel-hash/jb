import { createRoot } from 'react-dom/client';
import { createAppRouter } from './app/router.js';
import { createAppQueryClient } from './app/query-client.js';
import { createAppRoot } from './app/app-root.js';
import { createAppTheme } from './app/theme.js';

export function initializeApp(options = {}) {
  const container = options.container ?? { id: 'orga-root' };
  const router = options.router ?? createAppRouter();
  const queryClient = options.queryClient ?? createAppQueryClient();
  const theme = options.theme ?? createAppTheme();
  const rootTree = createAppRoot({ router, queryClient, theme, appOptions: options.appOptions ?? {} });
  const root = createRoot(container);
  root.render(rootTree);
  return {
    container,
    router,
    queryClient,
    theme,
    rootTree
  };
}

if (typeof document !== 'undefined') {
  const element = document.getElementById('root');
  if (element) {
    initializeApp({ container: element });
  }
}
