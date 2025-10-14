import { ErrorBoundary } from './ErrorBoundary';
import { PageHeader } from './PageHeader';

export function AppLayout(props) {
  const boundary = new ErrorBoundary({ fallbackTitle: 'Section indisponible' });
  const mainContent = boundary.render(props.outlet ?? { type: 'router-outlet' });
  const header = PageHeader({
    theme: props.theme,
    navigation: props.navigation,
    currentPath: props.currentPath,
    locale: props.locale
  });
  return {
    type: 'app-layout',
    header,
    main: mainContent,
    toastViewport: props.toasts.summary(),
    accessibility: {
      mainRole: 'main',
      headerRole: 'banner',
      hasSkipLink: true
    }
  };
}
