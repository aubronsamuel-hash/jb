const defaultColors = {
  background: '#0f0f1a',
  surface: '#181828',
  surfaceAlt: '#20203a',
  primary: '#5b3fd1',
  primaryAccent: '#7c5cff',
  accent: '#f7b538',
  success: '#4caf50',
  warning: '#ff9800',
  danger: '#ff5252',
  textPrimary: '#f8f8ff',
  textSecondary: '#c8c8d8',
  border: '#2a2a45'
};

const defaultRadius = {
  none: '0px',
  sm: '4px',
  md: '8px',
  lg: '12px',
  xl: '16px',
  full: '9999px'
};

const defaultFontFamily = {
  sans: ['Inter', 'Segoe UI', 'system-ui', 'sans-serif'],
  mono: ['Fira Code', 'Consolas', 'monospace']
};

export const appThemeTokens = {
  colors: defaultColors,
  radius: defaultRadius,
  fontFamily: defaultFontFamily
};

export function createAppTheme(overrides = {}) {
  return {
    colors: { ...defaultColors, ...(overrides.colors ?? {}) },
    radius: { ...defaultRadius, ...(overrides.radius ?? {}) },
    fontFamily: { ...defaultFontFamily, ...(overrides.fontFamily ?? {}) }
  };
}

export function AppThemeProvider({ theme, options = {}, children }) {
  const resolvedTheme = theme ?? createAppTheme();
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
    paletteSize: Object.keys(resolved.colors).length,
    radiusScale: Object.keys(resolved.radius),
    fonts: Object.fromEntries(
      Object.entries(resolved.fontFamily).map(([key, value]) => [key, Array.isArray(value) ? value.join(', ') : String(value)])
    )
  };
}
