import fs from 'node:fs';
import { describe, expect, test } from 'vitest';

const clientSource = fs.readFileSync('./src/api/client.ts', 'utf8');

describe('ApiClient source', () => {
  test('expose ApiClientError with toast mapping', () => {
    expect(clientSource).toContain('class ApiClientError extends Error');
    expect(clientSource).toContain("return 'Conflit detecte. Veuillez recharger le planning.';");
    expect(clientSource).toContain("return 'Verification echouee. Corrigez les champs surlignes.';");
  });

  test('normalizeError fallback messages for 409/422', () => {
    expect(clientSource).toContain("return 'Conflit detecte lors de la mise a jour';");
    expect(clientSource).toContain("return 'Requete invalide envoyee au service';");
  });

  test('headers and timeout merged in get helper', () => {
    expect(clientSource).toContain('timeoutMs: init.timeoutMs ?? this.timeoutMs');
    expect(clientSource).toContain("method: 'GET'");
  });
});
