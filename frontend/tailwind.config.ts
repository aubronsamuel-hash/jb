import { appThemeTokens } from './src/app/theme.js';

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: appThemeTokens.colors,
      borderRadius: appThemeTokens.radius,
      fontFamily: appThemeTokens.fontFamily
    }
  },
  plugins: []
};
