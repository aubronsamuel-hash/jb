#!/usr/bin/env node
import { runViteStub } from './vite-shared.js';

console.log('[lint-stub] ESLint/Prettier non disponibles dans l environnement local.');
runViteStub('dev');
