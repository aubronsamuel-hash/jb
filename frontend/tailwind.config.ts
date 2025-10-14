import { appThemeTokens } from './src/app/theme';

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        neutral: appThemeTokens.neutrals,
        accent: {
          blue: appThemeTokens.accents.blue,
          green: appThemeTokens.accents.green
        },
        semantic: appThemeTokens.semantic
      },
      borderRadius: appThemeTokens.radius,
      fontFamily: appThemeTokens.fonts,
      boxShadow: appThemeTokens.elevations,
      spacing: appThemeTokens.spacing
    }
  },
  plugins: []
};
