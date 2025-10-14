import fs from 'node:fs';
import { describe, it, expect } from 'vitest';

const navigationSource = fs.readFileSync('./src/app/navigation.ts', 'utf8');
const mainSource = fs.readFileSync('./src/app/main.ts', 'utf8');
const themeSource = fs.readFileSync('./src/app/theme.ts', 'utf8');

describe('coulisses crew bootstrap', () => {
  it('reference les modules de navigation principaux', () => {
    expect(navigationSource.includes("id: 'dashboard'")).toBe(true);
    expect(navigationSource.includes("id: 'planning'")).toBe(true);
    expect(navigationSource.includes("id: 'missions'")).toBe(true);
    expect(navigationSource.includes("id: 'notifications'")).toBe(true);
  });

  it('compose initializeApp avec providers et router', () => {
    expect(mainSource.includes('createAppProviders')).toBe(true);
    expect(mainSource.includes('createAppRouter')).toBe(true);
    expect(mainSource.includes('primeQueryClient')).toBe(true);
  });

  it('expose un theme clair/sombre avec tokens accentues', () => {
    expect(themeSource.includes("createAppTheme(mode = 'light')")).toBe(true);
    expect(themeSource.includes('accentPalette.blue')).toBe(true);
    expect(themeSource.includes('focusRing:')).toBe(true);
  });
});
