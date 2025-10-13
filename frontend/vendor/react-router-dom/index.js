export function createBrowserRouter(routes = [], options = {}) {
  return {
    routes,
    options,
    currentPath: options.initialEntries?.[0] ?? '/',
    basename: options.basename ?? '/',
    navigate(path) {
      this.currentPath = path;
      return this.currentPath;
    }
  };
}

export function RouterProvider({ router, children }) {
  return {
    type: 'router-provider',
    router,
    children: children ?? null
  };
}

export function Outlet() {
  return {
    type: 'router-outlet'
  };
}

export function Link({ to, children, variant = 'primary' }) {
  return {
    type: 'a',
    props: {
      href: to,
      variant,
      children: children ?? []
    }
  };
}

export function NavLink(props) {
  return Link({ ...props, variant: props.variant ?? 'nav' });
}

export function useNavigation() {
  return {
    state: 'idle'
  };
}

export function useLocation(router) {
  if (!router) {
    return {
      pathname: '/',
      search: '',
      hash: ''
    };
  }
  return {
    pathname: router.currentPath ?? '/',
    search: '',
    hash: ''
  };
}

export function redirect(path) {
  return { type: 'redirect', to: path };
}

export function createRoutesFromElements(elements) {
  return Array.isArray(elements) ? elements : [elements];
}

export function isRouteErrorResponse() {
  return false;
}
