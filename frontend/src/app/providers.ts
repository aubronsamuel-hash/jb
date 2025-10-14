export function createAppProviders(options) {
  const { theme, queryClient, router, i18n, toasts, navigation } = options;
  const cache = queryClient.cache;
  const queryList = cache && typeof cache.keys === 'function' ? Array.from(cache.keys()) : [];
  return {
    type: 'app-providers',
    layers: [
      {
        name: 'QueryClientProvider',
        meta: {
          queries: queryList
        }
      },
      {
        name: 'ThemeProvider',
        meta: {
          mode: theme.mode,
          focusRing: theme.focusRing
        }
      },
      {
        name: 'I18nProvider',
        meta: {
          language: i18n.language
        }
      },
      {
        name: 'RouterProvider',
        meta: {
          routeCount: router.routes.length,
          currentPath: router.currentPath,
          basename: router.basename
        }
      }
    ],
    context: {
      theme,
      queryClient,
      router,
      i18n,
      toasts,
      navigation,
      toastViewport: toasts.summary()
    }
  };
}
