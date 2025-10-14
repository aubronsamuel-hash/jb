import { createRoot } from 'react-dom/client';
import { createAppRouter, createRouteConfig, summarizeRoutes } from './router';
import { createAppQueryClient, primeQueryClient, queryKeys } from './query-client';
import { appNavigation } from './navigation';
import { createAppTheme, createThemeTokensSummary } from './theme';
import { createAppProviders } from './providers';
import { ToastManager } from './layout/Toasts';
import { createI18n } from '../i18n';

export function initializeApp(options = {}) {
  const container = options.container ?? { id: options.containerId ?? 'coulisses-root' };
  const theme = createAppTheme('light');
  const router = createAppRouter({
    theme,
    basename: options.basename,
    initialEntries: options.initialEntries,
    locale: options.locale
  });
  const queryClient = createAppQueryClient();
  primeQueryClient(queryClient, [
    { key: queryKeys.dashboard, value: { missionsToday: 3, staffingRate: 0.92 } }
  ]);
  const toasts = new ToastManager();
  const i18n = createI18n({ language: options.locale });
  const providers = createAppProviders({
    theme,
    queryClient,
    router: {
      routes: router.routes,
      currentPath: router.currentPath,
      basename: router.basename
    },
    i18n,
    toasts,
    navigation: appNavigation
  });
  const root = createRoot(container);
  const renderedTree = root.render(providers);
  return {
    container,
    router,
    queryClient,
    providers,
    theme,
    themeSummary: createThemeTokensSummary(theme),
    routeSummary: summarizeRoutes(createRouteConfig({ theme })),
    renderedTree
  };
}
