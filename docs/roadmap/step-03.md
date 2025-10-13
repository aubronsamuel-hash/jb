# Step 03 - Frontend Init React/Vite/TS

But

* Initialiser l application frontend avec une structure React + Vite + TypeScript conforme aux attentes de la spec fonctionnelle.
* Mettre en place les providers de base (router, query client, theming) et une navigation minimale pour les vues coeur (Dashboard, Planning, Missions, Equipes, Materiel, Budgets, Notifications, Parametres).
* Ajouter la configuration Tailwind CSS, PostCSS et Vite (meme en mode stub pour environnement offline) ainsi que les scripts npm associes.
* Documenter l architecture frontend et les commandes principales.

Contexte

* Step 02 a introduit un squelette JS/Vitest tres simple.
* Cette etape doit poser les fondations de l app React en respectant les contraintes offline (vendor local) et Windows-first.
* Les composants reels seront implantes dans les steps suivants; ici on pose les providers, routes, navigation et styles de base.

Taches

1. Architecture & Config

   * Creer `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/tailwind.config.ts`, `frontend/postcss.config.cjs`, `frontend/index.html`.
   * Ajouter un dossier `frontend/scripts/` avec scripts Node (ESM) pour build/mock Vite si necessaire.
   * Ajouter un dossier `frontend/vendor/` contenant les stubs des dependances clefs: react, react-dom, react-router-dom, @tanstack/react-query, tailwindcss, postcss, autoprefixer, typescript, vite (CLI stub).
   * Mettre a jour `frontend/package.json` et `frontend/package-lock.json` pour referencer ces dependances (file:vendor/...).

2. Code Source

   * Organiser `frontend/src/` avec:
     - `main.js` (bootstrap), `app/app-root.js`, `app/router.js`, `app/query-client.js`, `app/theme.js`.
     - Layout: `app/layouts/app-layout.js`.
     - Vues placeholder: `app/views/dashboard-view.js`, `app/views/placeholder-view.js`.
     - Config navigation: `app/navigation.js`.
     - Types TS: `src/types/index.d.ts` (description des contracts exposes).
   * Utiliser les stubs React/Router/Query pour retourner des structures declaratives (pas de DOM reel).
   * Prevoir un theme/tokens simples pour Tailwind (palette Orga de base).

3. Tests

   * Ajouter `frontend/tests/app-routing.test.js` pour valider la structure du router, le mapping navigation -> routes, et le comportement de `initializeApp`.
   * Conserver les tests existants (`math.test.js`).

4. Documentation

   * Mettre a jour le README (section Frontend) avec la structure, les scripts npm (`npm run dev`, `npm run build`, `npm run preview`, `npm test`).
   * Ajouter `docs/frontend/architecture.md` (nouveau dossier si besoin) décrivant les providers, navigation et strategy offline.

5. Archives

   * Alimenter `.codex/sessions/step-03/notes.md` avec les actions realisees.
   * Ajouter la sortie des tests dans `.codex/sessions/step-03/tests.log`.

Deliverables

* Docs: `docs/roadmap/step-03.md`, `docs/frontend/architecture.md`.
* Frontend config: `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/tailwind.config.ts`, `frontend/postcss.config.cjs`, `frontend/index.html`.
* Scripts: `frontend/scripts/*.js` (dev/build/preview mocks si necessaire).
* Vendor stubs: `frontend/vendor/react`, `frontend/vendor/react-dom`, `frontend/vendor/react-router-dom`, `frontend/vendor/@tanstack/react-query`, `frontend/vendor/tailwindcss`, `frontend/vendor/postcss`, `frontend/vendor/autoprefixer`, `frontend/vendor/typescript`, `frontend/vendor/vite`.
* Source: fichiers sous `frontend/src/**` decrit ci-dessus + types `.d.ts`.
* Tests: `frontend/tests/app-routing.test.js`.
* Archives: `.codex/sessions/step-03/notes.md`, `.codex/sessions/step-03/tests.log`.

Acceptance Criteria

* `npm test` passe (vitest stub) avec les nouveaux tests.
* `initializeApp()` retourne une structure contenant router, queryClient et rootTree coherent avec les definitions.
* Les routes couvrent au minimum Dashboard, Planning, Missions, Equipes, Materiel, Budgets, Notifications, Parametres avec un placeholder generique.
* Documentation a jour et ASCII-only.

Commandes Locales Exemples

* Frontend tests:
  cd frontend
  npm test
* Scripts Vite (mock):
  npm run dev
  npm run build
  npm run preview

Notes

* Referencer la PR avec `Ref: docs/roadmap/step-03.md`.
* Les stubs vendor doivent rester simples mais deterministes.

VALIDATE? yes/no
