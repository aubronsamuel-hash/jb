#!/usr/bin/env node
const mode = process.argv[2] ?? 'dev';
console.log(`[vite-stub] Commande ${mode} non supportee en environnement offline.`);
console.log('[vite-stub] Utiliser npm run dev/build/preview pour ces stubs.');
