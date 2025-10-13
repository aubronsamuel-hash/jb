import { designSystemDefaults, getRoleColor, getSemanticColor } from './tokens.js';

const DEFAULT_CONTRAST = '#0f172a';
const DEFAULT_TEXT_ON_DARK = '#f8fafc';

function normalizeId(prefix, fallback) {
  if (prefix) {
    return prefix;
  }
  if (fallback) {
    return String(fallback).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') || 'item';
  }
  return 'item';
}

export function createRoleBadge(config = {}) {
  const theme = config.theme ?? designSystemDefaults.theme;
  const role = (config.role ?? 'production').toLowerCase();
  const label = config.label ?? role.charAt(0).toUpperCase() + role.slice(1);
  const tone = config.tone ?? 'solid';
  const color = getRoleColor(role, theme);
  return {
    type: 'ds-role-badge',
    id: normalizeId(config.id, `${role}-badge`),
    role,
    label,
    tone,
    color,
    textColor: tone === 'solid' ? DEFAULT_TEXT_ON_DARK : color,
    outline: tone === 'outline' ? color : 'transparent'
  };
}

export function createKpiCard(config = {}) {
  const theme = config.theme ?? designSystemDefaults.theme;
  const direction = config.trend?.direction ?? 'stable';
  const derivedIntent = config.intent ?? (direction === 'up' ? 'success' : direction === 'down' ? 'warning' : 'info');
  const emphasis = getSemanticColor(derivedIntent, theme);
  const delta = config.trend?.delta ?? 0;
  return {
    type: 'ds-kpi-card',
    id: normalizeId(config.id, config.title ?? 'kpi-card'),
    title: config.title ?? 'KPI',
    value: config.value ?? '0',
    unit: config.unit ?? '',
    surface: theme.colors.surface,
    border: theme.colors.border,
    emphasis,
    intent: derivedIntent,
    trend: {
      direction,
      delta,
      tone: direction === 'up' ? 'positive' : direction === 'down' ? 'negative' : 'neutral'
    },
    caption: config.caption ?? null
  };
}

export function createModuleSummary(config = {}) {
  const theme = config.theme ?? designSystemDefaults.theme;
  const roles = (config.roles ?? []).map((role) => ({
    role,
    color: getRoleColor(role, theme)
  }));
  return {
    type: 'ds-module-summary',
    id: normalizeId(config.id, config.title ?? 'module'),
    title: config.title ?? 'Module',
    description: config.description ?? '',
    accent: theme.colors.accent,
    roles
  };
}

export function createSurfaceSample(config = {}) {
  const theme = config.theme ?? designSystemDefaults.theme;
  return {
    type: 'ds-surface-sample',
    id: normalizeId(config.id, 'surface'),
    background: theme.colors.background,
    surface: theme.colors.surface,
    border: theme.colors.border,
    textPrimary: theme.colors.textPrimary,
    textSecondary: theme.colors.textSecondary,
    contrast: DEFAULT_CONTRAST
  };
}
