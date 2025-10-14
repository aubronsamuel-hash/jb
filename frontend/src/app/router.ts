import { createBrowserRouter } from 'react-router-dom';
import { appNavigation } from './navigation';
import { AppLayout } from './layout/AppLayout';
import { ToastManager } from './layout/Toasts';
import { createDashboardPage } from '../pages/dashboard';
import { createNotFoundPage } from '../pages/not-found';
import { createPlaceholderPage } from '../pages/placeholder';
import { appThemeTokens, createAppTheme } from './theme';

export function createRouteConfig(options = {}) {
  const theme = options.theme ?? appThemeTokens;
  const navigation = options.navigation ?? appNavigation;
  const toasts = options.toasts ?? new ToastManager();
  const locale = options.locale ?? 'fr';

  const dashboardRoute = {
    id: 'dashboard',
    path: '/',
    element: createDashboardPage(theme),
    meta: {
      guard: 'authenticated',
      layout: 'app'
    }
  };

  const featureRoutes = navigation
    .filter((item) => item.id !== 'dashboard')
    .map((item) => ({
      id: item.id,
      path: item.path,
      element: createPlaceholderPage(item.id, item.description),
      meta: {
        guard: item.guard,
        icon: item.icon
      }
    }));

  const rootRoute = {
    id: 'app-shell',
    path: '/',
    element: AppLayout({
      theme,
      navigation,
      currentPath: navigation[0]?.path ?? '/',
      locale,
      toasts,
      outlet: { type: 'router-outlet' }
    }),
    children: [dashboardRoute, ...featureRoutes]
  };

  const notFoundRoute = {
    id: 'not-found',
    path: '*',
    element: createNotFoundPage()
  };

  return [rootRoute, notFoundRoute];
}

export function createAppRouter(options = {}) {
  const theme = options.theme ?? createAppTheme('light');
  const navigation = options.navigation ?? appNavigation;
  const routes = createRouteConfig({
    ...options,
    theme,
    navigation
  });
  const router = createBrowserRouter(routes, {
    basename: options.basename ?? '/',
    initialEntries: options.initialEntries ?? ['/']
  });
  return {
    ...router,
    routes
  };
}

export function summarizeRoutes(routes) {
  return routes.map((route) => ({
    id: route.id,
    path: route.path ?? null,
    hasChildren: Array.isArray(route.children) && route.children.length > 0
  }));
}
