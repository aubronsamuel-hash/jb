#!/usr/bin/env node
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const relative = path.relative(process.cwd(), __dirname) || '.';

console.log('[storybook-stub] Storybook n est pas installe dans ce mode offline.');
console.log('[storybook-stub] Ce script documente le workflow a activer lors du passage sur @storybook/react-vite.');
console.log(`[storybook-stub] Scripts localises dans ${relative}`);
console.log('[storybook-stub] Actions suggerees:');
console.log('  1. Installer @storybook/react-vite, @storybook/addon-essentials lorsque le reseau sera disponible.');
console.log('  2. Creer .storybook/main.ts et preview.ts pour charger les tokens (voir docs/frontend/design-system.md).');
console.log('  3. Importer les helpers createRoleBadge/createKpiCard pour generer des stories statiques.');
console.log('  4. Executer `npx storybook dev -p 6006` une fois les dependances reelles configurees.');
