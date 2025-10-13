# Architecture Frontend - Step 03

Cette note resume le socle frontend installe lors du step 03.

## Objectifs

* Structure React + Vite + TypeScript (mode offline) conforme a la spec Orga.
* Providers de base (Router, Query Client, Theme) relies a des stubs locaux pour permettre le dev sans dependances distantes.
* Navigation initiale couvrant les modules majeurs (Dashboard, Planning, Missions, Equipes, Materiel, Budgets, Notifications, Parametres).

## Organisation des Dossiers

```
frontend/
  index.html
  package.json
  package-lock.json
  postcss.config.cjs
  tailwind.config.ts
  tsconfig.json
  vite.config.ts
  scripts/
    vite-dev.js
    vite-build.js
    vite-preview.js
  src/
    main.js
    app/
      app-root.js
      query-client.js
      router.js
      theme.js
      navigation.js
      layouts/
        app-layout.js
      views/
        dashboard-view.js
        placeholder-view.js
    math.js
    types/
      index.d.ts
  tests/
    app-routing.test.js
    math.test.js
  vendor/
    (stubs react, react-dom, react-router-dom, @tanstack/react-query, tailwindcss, postcss, autoprefixer, typescript, vite)
```

## Providers

* **QueryClientProvider** (stub @tanstack/react-query) : expose un cache memo in-memory.
* **RouterProvider** (stub react-router-dom) : encapsule l arborescence de routes definie via `createBrowserRouter`.
* **AppThemeProvider** : simple wrapper retournant les tokens Tailwind (palette, radius) pour usage futur.

`createAppRoot()` assemble QueryClientProvider -> AppThemeProvider -> RouterProvider -> layout.

## Navigation & Routes

* `app/navigation.js` liste les entrees: dashboard, planning, missions, equipes, materiel, budgets, notifications, parametres.
* `app/router.js` construit les routes a partir de ces modules avec placeholder generique.
* Chaque vue placeholder expose titre, description, identifiant module.

## Scripts npm (mode offline)

* `npm run dev` : appelle `vendor/vite/bin/vite.js dev` (stub CLI affichant instructions).
* `npm run build` : idem (mode build) ecrit un message et cree `/tmp`? -> ici log console (pas d ecriture hors repo).
* `npm run preview` : idem (mode preview).
* `npm test` : execute `vitest` stub apres eventuel build TS (non requis pour le moment).

## Types & TypeScript

* `tsconfig.json` active `allowJs` pour permettre un portage progressif TypeScript.
* `src/types/index.d.ts` decrit les signatures publiques (`initializeApp`, `createAppRouter`, etc.).
* Les modules JS incluent des annotations JSDoc pour faciliter l adoption TS plus tard.

## Tailwind Tokens

* Palette Orga (noir, gris, violet theatre, accent or) definie dans `app/theme.js` et re-exportee dans `tailwind.config.ts`.
* Les vraies classes seront ajoutees a mesure que l UI evolue.

## Offline Strategy

* Tous les packages critiques sont stubs sits `frontend/vendor`.
* `package.json` reference `file:vendor/...` pour eviter tout fetch reseau.
* Scripts CLI (Vite/Tailwind) affichent un message explicite indiquant que c est un stub et comment proceder lors du passage a de vraies dependances.

## Tests

* `app-routing.test.js` verifie la coherence router/navigation et `initializeApp`.
* `math.test.js` conserve un exemple simple.

Cette base servira pour les steps suivants (composition UI, interactions, exports). VALIDATE requis par Sam avant integration finale.
