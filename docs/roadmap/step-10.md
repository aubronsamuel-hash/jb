# Step 10 - Coulisses Crew Frontend Foundation

But

* Initialiser le frontend Coulisses Crew (React 18 + TypeScript) selon la specification v1.
* Mettre en place l architecture applicative (routing, state, theming) et les conventions UI/UX de base.
* Documenter les commandes de demarrage/tests et les standards d accessibilite/performance.

Contexte

* Les modules backend fondamentaux (missions, planning, paie) sont disponibles via l API.
* Les equipes produit attendent un socle frontend permettant d enchainer les features planifiees (planning, missions, notifications...).
* Les contraintes Windows/PowerShell et ASCII-only doivent etre respectees pour l outillage CLI.

Taches

1. Bootstrap Vite + React 18 + TypeScript

   * Generer le projet `frontend` avec Vite (React + TS) et configurer ESLint/Prettier/TypeScript strict.
   * Installer Tailwind CSS, shadcn/ui, lucide-react, React Router v6, React Query, Zustand, i18next, Vitest/RTL, Playwright, Storybook 8.
   * Configurer les scripts npm (dev, build, lint, test, storybook, e2e) compatibles Windows.

2. Architecture et providers

   * Structurer `src` selon l arborescence definie (app, features, components, api, state, hooks, pages, styles, i18n, stories, tests).
   * Ajouter `app/main.tsx`, `app/router.tsx`, `app/providers.tsx` avec React Router, React Query, Zustand, theming clair/sombre, i18n fr.
   * Mettre en place les layouts de base (`PageHeader`, `ErrorBoundary`, `Toasts`) et integrer Radix pour accessibilite.

3. Design system et styles

   * Configurer Tailwind (`tailwind.config.ts`, `src/styles/index.css`) avec palettes neutres + accent bleu/vert, support dark mode.
   * Ajouter wrappers shadcn/ui dans `components/ui` (Button, Input, Select, Dialog, Tabs, Tooltip, Toast, Avatar, Badge, DataTable...).
   * Verifier focus states, roles ARIA, contraste AA.

4. Outils et qualite

   * Configurer Vitest + RTL, Playwright, Storybook (Chromatic CI) et axe-core en dev.
   * Mettre en place React Query devtools (optionnel dev), Zustand devtools, scripts lint/test/pre-commit.
   * Ajouter configuration PWA optionnelle (cache assets, lecture planning offline) derriere flag.

5. Documentation

   * Rediger `docs/frontend/coulisses-crew-frontend.md` decrivant architecture, commandes, conventions, perf.
   * Mettre a jour `README.md` (section frontend) avec instructions install/build/test Windows.
   * Ajouter references a la spec v1 et aux prochains jalons (planning semaine, missions CRUD...).

Deliverables

* Code: structure frontend, providers, design system, tooling.
* Tests: suites unitaires de base (Vitest), smoke Playwright, Storybook fonctionnel.
* Docs: note frontend detaillee + README mis a jour.

Acceptance Criteria

* `npm run lint`, `npm run test`, `npm run build` et `npm run storybook -- --ci` passent sous Node 18+ (PowerShell).
* L appli charge sans erreur, routes publiques/privees configurees avec gardes d habilitation.
* Respect du theming clair/sombre et accessibilite AA sur composants principaux.

VALIDATE? yes/no
