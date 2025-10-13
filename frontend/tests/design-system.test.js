import { describe, it, expect } from 'vitest';
import { createAppTheme } from '../src/app/theme.js';
import { getRoleColor, getSemanticColor, describeThemeModes, createThemeSnapshot } from '../src/app/design-system/tokens.js';
import { createRoleBadge, createKpiCard, createModuleSummary, createSurfaceSample } from '../src/app/design-system/components.js';
import { createNavigationRoleBadges } from '../src/app/navigation.js';

describe('createAppTheme', () => {
    it('exposes light mode tokens by default', () => {
        const theme = createAppTheme();
        expect(theme.mode).toBe('light');
        expect(theme.colors.background).toBe('#f5f7fb');
        expect(theme.roleColors.lumiere).toBe('#f5b301');
        expect(theme.spacing.section).toBe('3rem');
        expect(theme.typography.body.fontSize).toBe('1rem');
    });

    it('supports dark mode palette and semantic colors', () => {
        const theme = createAppTheme({ mode: 'dark' });
        expect(theme.mode).toBe('dark');
        expect(theme.colors.background).toBe('#0f172a');
        expect(theme.semantic.success).toBe(theme.roleColors.video);
        expect(theme.semantic.warning).toBe(theme.roleColors.lumiere);
    });

    it('merges overrides without mutating defaults', () => {
        const theme = createAppTheme({ colors: { accent: '#222222' }, spacing: { custom: '5rem' } });
        expect(theme.colors.accent).toBe('#222222');
        expect(theme.spacing.custom).toBe('5rem');
        const fresh = createAppTheme();
        expect(fresh.colors.accent).toBe('#4c51bf');
        expect('custom' in fresh.spacing).toBe(false);
    });
});

describe('design system tokens', () => {
    it('returns consistent role colors and fallback', () => {
        expect(getRoleColor('son')).toBe('#3b82f6');
        expect(getRoleColor('unknown-role')).toBe('#0ea5e9');
    });

    it('resolves semantic colors with fallback', () => {
        const theme = createAppTheme({ semantic: { info: '#1e3a8a' } });
        expect(getSemanticColor('info', theme)).toBe('#1e3a8a');
        expect(getSemanticColor('danger', theme)).toBe('#ef4444');
        expect(getSemanticColor('undefined-tone', theme)).toBe(theme.semantic.info);
    });

    it('describes each mode for documentation usage', () => {
        const summary = describeThemeModes();
        const modes = summary.map((entry) => entry.mode);
        expect(modes.includes('light')).toBe(true);
        expect(modes.includes('dark')).toBe(true);
        const lightEntry = summary.find((entry) => entry.mode === 'light');
        expect(lightEntry.background).toBe('#f5f7fb');
        expect(lightEntry.semantic.success).toBe('#22c55e');
    });

    it('produces a snapshot of the theme tokens', () => {
        const snapshot = createThemeSnapshot({ mode: 'dark' });
        expect(snapshot.mode).toBe('dark');
        expect(snapshot.roleColors.hmc).toBe('#ec4899');
        expect(snapshot.spacing.gutter).toBe('1.25rem');
    });
});

describe('design system components', () => {
    it('creates role badges with tone aware colors', () => {
        const badge = createRoleBadge({ role: 'lumiere' });
        expect(badge.type).toBe('ds-role-badge');
        expect(badge.role).toBe('lumiere');
        expect(badge.color).toBe('#f5b301');
        expect(badge.textColor).toBe('#f8fafc');
    });

    it('creates KPI cards with trend metadata', () => {
        const card = createKpiCard({ title: 'Heures', value: '48', trend: { direction: 'down', delta: 3 } });
        expect(card.type).toBe('ds-kpi-card');
        expect(card.trend.tone).toBe('negative');
        expect(card.emphasis).toBe('#f5b301');
        expect(card.intent).toBe('warning');
    });

    it('creates module summaries listing roles and colors', () => {
        const summary = createModuleSummary({ title: 'Planning', roles: ['son', 'video'] });
        expect(summary.type).toBe('ds-module-summary');
        expect(summary.roles.length).toBe(2);
        expect(summary.roles[0].color).toBe('#3b82f6');
    });

    it('samples surface tokens for snapshot testing', () => {
        const sample = createSurfaceSample();
        expect(sample.type).toBe('ds-surface-sample');
        expect(sample.background).toBe('#f5f7fb');
        expect(sample.border).toBe('#d5dae6');
    });
});

describe('navigation integration', () => {
    it('builds navigation role badges using design system helpers', () => {
        const badgeGroups = createNavigationRoleBadges();
        expect(badgeGroups.length > 0).toBe(true);
        const dashboardGroup = badgeGroups.find((group) => group.target === 'dashboard');
        expect(dashboardGroup != null).toBe(true);
        expect(dashboardGroup.badges.length > 0).toBe(true);
        expect(dashboardGroup.badges[0].type).toBe('ds-role-badge');
    });
});
