const neutralPalette = {
  50: '#f8fafc',
  100: '#f1f5f9',
  200: '#e2e8f0',
  300: '#cbd5f5',
  400: '#94a3b8',
  500: '#64748b',
  600: '#475569',
  700: '#334155',
  800: '#1e293b',
  900: '#0f172a'
};

const accentPalette = {
  blue: {
    100: '#dbeafe',
    200: '#bfdbfe',
    300: '#93c5fd',
    400: '#60a5fa',
    500: '#2563eb',
    600: '#1d4ed8',
    700: '#1e40af'
  },
  green: {
    100: '#dcfce7',
    200: '#bbf7d0',
    300: '#86efac',
    400: '#4ade80',
    500: '#22c55e',
    600: '#16a34a',
    700: '#15803d'
  }
};

const radiusScale = {
  xs: '2px',
  sm: '4px',
  md: '8px',
  lg: '16px',
  full: '9999px'
};

const spacingScale = {
  '3xs': '0.125rem',
  '2xs': '0.25rem',
  xs: '0.5rem',
  sm: '0.75rem',
  md: '1rem',
  lg: '1.5rem',
  xl: '2rem',
  '2xl': '3rem',
  section: '4rem'
};

const fontFamilies = {
  sans: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  heading: '"Satoshi", "Segoe UI", sans-serif',
  mono: '"JetBrains Mono", Menlo, monospace'
};

const elevations = {
  none: 'none',
  sm: '0 1px 2px rgba(15, 23, 42, 0.12)',
  md: '0 8px 24px rgba(15, 23, 42, 0.16)',
  lg: '0 16px 48px rgba(15, 23, 42, 0.24)'
};

const baseSemantic = {
  info: accentPalette.blue[400],
  success: accentPalette.green[500],
  warning: '#f59e0b',
  danger: '#ef4444',
  muted: neutralPalette[400]
};

const surfacesByMode = {
  light: {
    base: '#ffffff',
    raised: '#f8fafc',
    overlay: '#e2e8f0',
    inverted: neutralPalette[900]
  },
  dark: {
    base: neutralPalette[900],
    raised: '#111827',
    overlay: '#1f2937',
    inverted: '#ffffff'
  }
};

export function createAppTheme(mode = 'light') {
  return {
    mode,
    neutrals: neutralPalette,
    accents: accentPalette,
    semantic: baseSemantic,
    surfaces: surfacesByMode[mode],
    radius: radiusScale,
    spacing: spacingScale,
    fonts: fontFamilies,
    elevations,
    focusRing: `0 0 0 3px ${accentPalette.blue[400]}55`
  };
}

export const appThemeTokens = createAppTheme('light');

export function createThemeTokensSummary(theme) {
  const accentSwatches = [
    theme.accents.blue[500],
    theme.accents.green[500],
    theme.semantic.warning,
    theme.semantic.danger
  ];
  const paletteSize = Object.keys(theme.neutrals).length;
  return {
    mode: theme.mode,
    paletteSize,
    accentSwatches,
    surfaceContrast: Object.entries(theme.surfaces).map(([surface, value]) => ({
      surface,
      value
    })),
    spacingKeys: Object.keys(theme.spacing),
    fontFamilies: theme.fonts
  };
}
