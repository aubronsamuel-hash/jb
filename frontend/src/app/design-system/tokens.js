import { createAppTheme, themeModes, appThemeTokens } from '../theme.js';

export function getRoleColor(role, theme = appThemeTokens) {
  const palette = theme?.roleColors ?? appThemeTokens.roleColors;
  if (!role) {
    return palette.production;
  }
  const key = String(role).toLowerCase();
  return palette[key] ?? palette.production;
}

export function getSemanticColor(name, theme = appThemeTokens) {
  const semantic = theme?.semantic ?? appThemeTokens.semantic;
  const key = String(name).toLowerCase();
  return semantic[key] ?? semantic.info;
}

export function describeThemeModes() {
  return themeModes.map((mode) => {
    const theme = createAppTheme({ mode });
    return {
      mode,
      background: theme.colors.background,
      surface: theme.colors.surface,
      text: theme.colors.textPrimary,
      accent: theme.colors.accent,
      semantic: { ...theme.semantic }
    };
  });
}

export function createThemeSnapshot(options = {}) {
  const theme = createAppTheme(options);
  return {
    mode: theme.mode,
    colors: { ...theme.colors },
    roleColors: { ...theme.roleColors },
    semantic: { ...theme.semantic },
    spacing: { ...theme.spacing },
    radius: { ...theme.radius },
    typography: { ...theme.typography },
    elevations: { ...theme.elevations },
    transitions: { ...theme.transitions }
  };
}

export const designSystemDefaults = Object.freeze({
  theme: appThemeTokens,
  modes: themeModes,
  primaryRoles: Object.keys(appThemeTokens.roleColors)
});
