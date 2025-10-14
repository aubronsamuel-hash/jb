# Coulisses Crew Frontend Foundation (Step 10)

## Architecture generale

```
frontend/
├── src/
│   ├── app/              # Providers, router, theming, navigation
│   ├── api/              # Client HTTP (stub) pour l API Coulisses Crew
│   ├── components/ui/    # Design system (wrappers shadcn/ui accessibles)
│   ├── features/         # Regroupement par domaine fonctionnel
│   ├── hooks/            # Hooks partages (theme, toasts)
│   ├── i18n/             # Ressources de traduction i18next (fr par defaut)
│   ├── pages/            # Pages routes (dashboard, placeholders)
│   ├── state/            # Stores Zustand
│   ├── stories/          # Stories Storybook 8 (placeholder)
│   ├── styles/           # Tailwind + tokens globaux
│   └── tests/            # Utilitaires de test Vitest/RTL
├── scripts/              # Stubs CLI Windows-first (Vite, Storybook, lint...)
├── vendor/               # Paquets stubs (React, React Query, Zustand, i18next...)
├── tailwind.config.ts    # Palette neutre + accents bleu/vert (dark mode)
├── tsconfig.json         # TypeScript strict
└── vite.config.ts        # Configuration Vite (stub)
```

## Providers et routing

* `initializeApp()` (src/app/main.ts) installe :
  * `QueryClient` (@tanstack/react-query) avec `queryKeys` par domaine (dashboard, planning, missions...).
  * Router (`createBrowserRouter` stub) et structure des routes derivee de `appNavigation`.
  * Theming clair/sombre via tokens `createAppTheme()` et store Zustand (`useThemeStore`).
  * I18n francais (`createI18n`) et Toast manager (`ToastManager`).
* Les providers retournent un arbre deterministe (type `app-providers`) facilitant les snapshots/tests.

## Design system

* Les composants `Button`, `Dialog`, `Tabs`, `Tooltip`, `Toast`, `Avatar`, `Badge`, `DataTable` exposent des metadonnees accesibles (roles ARIA, focus ring, labels).
* Tailwind est configure avec :
  * Palette neutre (50 -> 900) et accents bleu/vert.
  * Ombres et rayons pour respecter les guidelines Coulisses Crew.
  * Mode sombre via `[data-theme="dark"]`.
* Les pages utilisent `PageHeader`, `AppLayout`, `ToastManager` et `ErrorBoundary` pour assurer la structure et les toasts Radix-like.

## Commandes npm (PowerShell/Windows)

```ps1
npm run dev        # Vite stub (affiche la procedure locale)
npm run build      # Build stub
npm run preview    # Preview stub
npm run lint       # Rappel ESLint/Prettier (a installer via pnpm/npm quand le reseau sera disponible)
npm run typecheck  # Conseil pour lancer `npx tsc --noEmit`
npm run storybook  # Stub Storybook 8 (Chromatic a activer plus tard)
npm run test       # Vitest (stubs React/Query/Zustand)
npm run e2e        # Stub Playwright (guides e2e)
```

## Tests et qualite

* `frontend/tests/*.test.ts` couvre bootstrap app (router, providers) et les composants UI accessibles.
* `frontend/tests/api-client.test.js` verifie la normalisation des erreurs 409/422 et les toasts ASCII (`ApiClientError`).
* `frontend/tests/planning-assignments.test.js` valide la sanitation du flux pagination et le message aria-live.
* Vitest reste embarque (`vendor/vitest`) -> pas d installation externe.
* Playwright/Storybook exposes des scripts stubs pour guider la future integration CI.

## Accessibilite & performance

* Focus ring defini globalement (`0 0 0 3px rgba(37, 99, 235, 0.45)`).
* Roles ARIA explicites pour les composants UI et layout (`banner`, `main`, `dialog`, `tooltip`, `table`).
* Contraste AA assure via palette neutre + accents (blue 500 / green 500) et surfaces `createAppTheme()`.
* Etat offline : assets Tailwind et React charges via dossiers `vendor/` (ASCII-only, compatible air-gap).
* `computeAssignmentAccessibilityHints()` fournit un resume ASCII (total, confirmes, en attente, declines) annonce via `aria-live` sur la liste planning.

## Step 12 - Ajustements QA

* `ApiClient.normalizeError()` retourne un `ApiClientError` type avec codes `invalid_pagination`, `cursor_not_found`, `conflict` et un message ASCII adapte aux toasts Windows.
* `ApiClientError.toToastMessage()` distingue 409 (conflit assignation), 422 (validation) et autres indisponibilites.
* `sanitizeAssignmentFeed()` nettoie le payload backend `/api/planning/assignments` avant injection React Query.
* Les toasts/accessibilite sont testes via Vitest pour garantir compatibilite PowerShell + NVDA.

## Etapes suivantes

* Brancher l API backend (missions/planning) dans `src/api/` et hydrater React Query.
* Completer les stories Storybook 8 avec Chromatic.
* Remplacer les stubs CLI par les outils officiels (Vite, ESLint, Playwright) lors de l ouverture reseau.
