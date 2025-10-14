import fs from 'node:fs';
import { describe, it, expect } from 'vitest';

const buttonSource = fs.readFileSync('./src/components/ui/button.ts', 'utf8');
const dialogSource = fs.readFileSync('./src/components/ui/dialog.ts', 'utf8');
const dataTableSource = fs.readFileSync('./src/components/ui/data-table.ts', 'utf8');

describe('design system fichiers', () => {
  it('definit un composant bouton accesible', () => {
    expect(buttonSource.includes("type: 'ui-button'"))
      .toBe(true);
    expect(buttonSource.includes('focusRing'))
      .toBe(true);
  });

  it('expose un composant dialog avec role dialog', () => {
    expect(dialogSource.includes("role: 'dialog'"))
      .toBe(true);
    expect(dialogSource.includes('ariaModal'))
      .toBe(true);
  });

  it('documente le tableau de donnees', () => {
    expect(dataTableSource.includes("type: 'ui-data-table'"))
      .toBe(true);
    expect(dataTableSource.includes('rowCount'))
      .toBe(true);
  });
});
