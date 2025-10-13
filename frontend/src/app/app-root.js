import { createElement } from 'react';
import { QueryClientProvider } from '@tanstack/react-query';
import { RouterProvider } from 'react-router-dom';
import { AppThemeProvider } from './theme.js';

export function createAppRoot({ router, queryClient, theme, appOptions = {} }) {
  return createElement(QueryClientProvider, { client: queryClient },
    createElement(AppThemeProvider, { theme, options: appOptions },
      createElement(RouterProvider, { router })
    )
  );
}
