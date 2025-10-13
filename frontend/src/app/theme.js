const paletteModes = {
  light: {
    background: '#f5f7fb',
    surface: '#ffffff',
    surfaceAlt: '#f1f3f9',
    surfaceMuted: '#e4e8f4',
    border: '#d5dae6',
    textPrimary: '#1f2937',
    textSecondary: '#4b5563',
    textMuted: '#6b7280',
    accent: '#4c51bf',
    accentMuted: '#6366f1',
    overlay: 'rgba(15, 23, 42, 0.72)'
  },
  dark: {
    background: '#0f172a',
    surface: '#111827',
    surfaceAlt: '#1f2937',
    surfaceMuted: '#273449',
    border: '#2b3a55',
    textPrimary: '#f9fafb',
    textSecondary: '#d1d5db',
    textMuted: '#9ca3af',
    accent: '#818cf8',
    accentMuted: '#a5b4fc',
    overlay: 'rgba(15, 23, 42, 0.84)'
  }
};

const roleColors = {
  lumiere: '#f5b301',
  son: '#3b82f6',
  video: '#22c55e',
  plateau: '#6b7280',
  hmc: '#ec4899',
  admin: '#f97316',
  artiste: '#8b5cf6',
  production: '#0ea5e9'
};

const semanticDefaults = {
  info: '#3b82f6',
  success: '#16a34a',
  warning: '#f59e0b',
  danger: '#ef4444'
};

const radiusScale = {
  none: '0px',
  xs: '2px',
  sm: '4px',
  md: '8px',
  lg: '12px',
  xl: '16px',
  full: '9999px'
};

const spacingScale = {
  none: '0px',
  xxs: '0.25rem',
  xs: '0.5rem',
  sm: '0.75rem',
  md: '1rem',
  lg: '1.5rem',
  xl: '2rem',
  xxl: '2.5rem',
  gutter: '1.25rem',
  section: '3rem'
};

const fontFamily = {
  sans: ['Inter', 'Segoe UI', 'system-ui', 'sans-serif'],
  mono: ['Fira Code', 'Consolas', 'monospace']
};

const typography = {
  display: { fontSize: '2.75rem', lineHeight: '3.25rem', fontWeight: 600, letterSpacing: '-0.02em' },
  headline: { fontSize: '2rem', lineHeight: '2.5rem', fontWeight: 600, letterSpacing: '-0.01em' },
  title: { fontSize: '1.5rem', lineHeight: '2rem', fontWeight: 600, letterSpacing: '-0.01em' },
  subtitle: { fontSize: '1.125rem', lineHeight: '1.75rem', fontWeight: 500, letterSpacing: '-0.005em' },
  body: { fontSize: '1rem', lineHeight: '1.5rem', fontWeight: 400, letterSpacing: '0em' },
  caption: { fontSize: '0.875rem', lineHeight: '1.25rem', fontWeight: 400, letterSpacing: '0.01em' }
};

const elevations = {
  flat: 'none',
  raised: '0 10px 30px rgba(15, 23, 42, 0.12)',
  overlay: '0 18px 42px rgba(15, 23, 42, 0.24)'
};

const transitions = {
  default: 'all 150ms ease-out',
  emphasis: 'all 220ms cubic-bezier(0.4, 0, 0.2, 1)',
  gentle: 'all 320ms ease-in-out'
};

function mergeTokens(base, overrides) {
  const result = { ...base };
  if (!overrides) {
    return result;
  }
  for (const key of Object.keys(overrides)) {
    const value = overrides[key];
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      result[key] = mergeTokens(base[key] ?? {}, value);
    } else {
      result[key] = value;
    }
  }
  return result;
}

function resolveSemanticColors(rolePalette, custom) {
  const base = {
    info: rolePalette.son ?? semanticDefaults.info,
    success: rolePalette.video ?? semanticDefaults.success,
    warning: rolePalette.lumiere ?? semanticDefaults.warning,
    danger: semanticDefaults.danger
  };
  return { ...base, ...(custom ?? {}) };
}

export function createAppTheme(options = {}) {
  const { mode = 'light', colors, roleColors: roleOverrides, semantic, radius, spacing, fontFamily: fonts, typography: typeOverrides, elevations: elevationOverrides, transitions: transitionOverrides } = options;
  const palette = paletteModes[mode] ?? paletteModes.light;
  const mergedRoleColors = { ...roleColors, ...(roleOverrides ?? {}) };
  return {
    mode,
    colors: { ...palette, ...(colors ?? {}) },
    roleColors: mergedRoleColors,
    semantic: resolveSemanticColors(mergedRoleColors, semantic),
    radius: { ...radiusScale, ...(radius ?? {}) },
    spacing: { ...spacingScale, ...(spacing ?? {}) },
    fontFamily: { ...fontFamily, ...(fonts ?? {}) },
    typography: mergeTokens(typography, typeOverrides),
    elevations: { ...elevations, ...(elevationOverrides ?? {}) },
    transitions: { ...transitions, ...(transitionOverrides ?? {}) }
  };
}

export const appThemeTokens = createAppTheme();

export function AppThemeProvider({ theme, options = {}, children }) {
  const resolvedTheme = theme ?? createAppTheme(options);
  return {
    type: 'app-theme-provider',
    theme: resolvedTheme,
    options,
    children: children ?? []
  };
}

export function useAppTheme(theme) {
  return theme ?? createAppTheme();
}

export function createThemeTokensSummary(theme) {
  const resolved = theme ?? createAppTheme();
  return {
    mode: resolved.mode,
    paletteSize: Object.keys(resolved.colors).length,
    roles: Object.keys(resolved.roleColors),
    semantic: { ...resolved.semantic },
    spacingKeys: Object.keys(resolved.spacing)
  };
}

export const themeModes = Object.freeze(Object.keys(paletteModes));
