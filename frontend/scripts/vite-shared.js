#!/usr/bin/env node
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const messages = {
  dev: 'Vite stub - dev mode (aucune compilation realisee).',
  build: 'Vite stub - build mode (a implementer lors du switch dependances reelles).',
  preview: 'Vite stub - preview mode (affichage uniquement).'
};

export function runViteStub(command) {
  const message = messages[command] ?? 'Vite stub - commande inconnue.';
  const relative = path.relative(process.cwd(), __dirname) || '.';
  console.log(`[vite-stub] ${message}`);
  console.log(`[vite-stub] Scripts localises dans ${relative}`);
  console.log('[vite-stub] Voir docs/frontend/architecture.md pour passer sur de vraies dependances.');
}
