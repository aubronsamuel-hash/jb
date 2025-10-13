import { describe, it, expect } from 'vitest';
import { initializeApp } from '../src/main.js';
import { createAppRouter, createRouteConfig, summarizeRoutes } from '../src/app/router.js';
import { appNavigation } from '../src/app/navigation.js';
import { createAppQueryClient, queryKeys } from '../src/app/query-client.js';
import { createAppTheme, createThemeTokensSummary } from '../src/app/theme.js';

describe('app router configuration', () => {
    it('includes all navigation modules as routes', () => {
        const config = createRouteConfig();
        expect(config.length).toBe(1);
        const rootRoute = config[0];
        expect(rootRoute.children.length).toBe(appNavigation.length);
        const ids = rootRoute.children.map((child) => child.id);
        appNavigation.forEach((nav) => {
            expect(ids.includes(nav.id)).toBe(true);
        });
    });

    it('summarizes routes structure', () => {
        const config = createRouteConfig();
        const summary = summarizeRoutes(config);
        expect(summary[0].id).toBe('app-shell');
        expect(summary[0].hasChildren).toBe(true);
    });

    it('decorates the layout with design system context', () => {
        const theme = createAppTheme();
        const config = createRouteConfig({ theme });
        const layout = config[0].element;
        expect(Array.isArray(layout.designSystem.themeModes)).toBe(true);
        expect(layout.designSystem.themeModes.length >= 2).toBe(true);
        expect(layout.designSystem.navigationBadges.length).toBe(appNavigation.length);
        const firstBadgeGroup = layout.designSystem.navigationBadges[0];
        expect(firstBadgeGroup.badges.every((badge) => badge.type === 'ds-role-badge')).toBe(true);
    });
});

describe('query client configuration', () => {
    it('exposes query keys per domain', () => {
        const domains = ['dashboard', 'planning', 'missions', 'teams', 'equipment', 'budgets', 'notifications', 'settings'];
        domains.forEach((key) => {
            expect(Array.isArray(queryKeys[key])).toBe(true);
        });
    });

    it('allows priming cache during initialization', () => {
        const client = createAppQueryClient();
        client.setQueryData(queryKeys.dashboard, { missionsToday: 3 });
        expect(client.getQueryData(queryKeys.dashboard).missionsToday).toBe(3);
    });
});

describe('initializeApp', () => {
    it('returns providers, router and theme summary', () => {
        const theme = createAppTheme();
        const result = initializeApp({
            container: { id: 'test-root' },
            router: createAppRouter({ theme }),
            queryClient: createAppQueryClient(),
            theme
        });
        expect(result.container.id).toBe('test-root');
        expect(result.router.routes[0].id).toBe('app-shell');
        expect(result.rootTree.type).toBe('query-client-provider');
        const themeSummary = createThemeTokensSummary(result.theme);
        expect(themeSummary.mode).toBe('light');
        expect(themeSummary.roles.includes('lumiere')).toBe(true);
        expect(themeSummary.semantic.success).toBe(theme.roleColors.video);
        expect(themeSummary.spacingKeys.includes('section')).toBe(true);
    });
});
