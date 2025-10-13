import { createBrowserRouter } from 'react-router-dom';
import { appNavigation } from './navigation.js';
import { AppLayout } from './layouts/app-layout.js';
import { DashboardView } from './views/dashboard-view.js';
import { PlaceholderView } from './views/placeholder-view.js';

function buildChildrenRoutes(navigation) {
  const routes = [];
  for (const item of navigation) {
    if (item.id === 'dashboard') {
      routes.push({
        id: item.id,
        index: true,
        element: DashboardView({ heading: 'Dashboard' })
      });
    } else {
      routes.push({
        id: item.id,
        path: item.path.replace(/^\//, ''),
        element: PlaceholderView({ id: item.id })
      });
    }
  }
  return routes;
}

export function createRouteConfig(options = {}) {
  const navigation = options.navigation ?? appNavigation;
  const theme = options.theme ?? null;
  const children = buildChildrenRoutes(navigation);
  return [
    {
      id: 'app-shell',
      path: '/',
      element: AppLayout({ theme, navigation }),
      children
    }
  ];
}

export function createAppRouter(options = {}) {
  const routes = createRouteConfig(options);
  return createBrowserRouter(routes, {
    basename: options.basename ?? '/',
    initialEntries: options.initialEntries ?? ['/']
  });
}

export function summarizeRoutes(routes = []) {
  return routes.map((route) => ({
    id: route.id,
    path: route.path ?? null,
    hasChildren: Array.isArray(route.children) && route.children.length > 0
  }));
}
