# Architecture Frontend - Step 04

Cette note resume le socle frontend et le design system minimal installe lors du step 04.

## Objectifs

* Maintenir la structure React + Vite + TypeScript (mode offline) conforme a la spec Orga.
* Enrichir le theme avec tokens modes clair/sombre, palette roles et echelles (spacing, typography, elevations, transitions).
* Fournir des helpers design system stubs utilisables pour le dashboard et les modules (badges roles, cartes KPI, resume modules).

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
    storybook.js
    vite-shared.js
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
      design-system/
        index.js
        tokens.js
        components.js
      views/
        dashboard-view.js
        placeholder-view.js
    math.js
    types/
      index.d.ts
  tests/
    app-routing.test.js
    design-system.test.js
    math.test.js
  vendor/
    (stubs react, react-dom, react-router-dom, @tanstack/react-query, tailwindcss, postcss, autoprefixer, typescript, vite, vitest)
```

## Theme et Tokens

* `theme.js` expose `createAppTheme`, `appThemeTokens`, `themeModes`.
* Modes: `light` (defaut) et `dark` avec surfaces, textes et accent dedies.
* Palette role: lumiere, son, video, plateau, hmc, admin, artiste, production.
* Tokens supplementaires: spacing (`xxs` -> `xxl`, `gutter`, `section`), radius (`xs` -> `xl`), typography (display -> caption), elevations, transitions.
* `tailwind.config.ts` importe `appThemeTokens` et propage `colors`, `borderRadius`, `fontFamily`, `boxShadow`, `spacing`.

## Design System Stub

* `design-system/tokens.js`: helpers `getRoleColor`, `getSemanticColor`, `describeThemeModes`, `createThemeSnapshot`.
* `design-system/components.js`: stubs `createRoleBadge`, `createKpiCard`, `createModuleSummary`, `createSurfaceSample`.
* `design-system/index.js`: re-export.
* `dashboard-view.js` utilise ces helpers pour fournir des cartes KPI et un resume module par defaut.

## Scripts npm (mode offline)

* `npm run dev` : stub Vite (voir `scripts/vite-*.js`).
* `npm run build` : stub build.
* `npm run preview` : stub preview.
* `npm run storybook` : script documentaire indiquant comment lancer un futur Storybook.
* `npm test` : vitest stub (tests router + design system).

## Tests

* `app-routing.test.js` valide navigation/initializeApp et verifie le resume de theme (mode, roles, spacing).
* `design-system.test.js` couvre `createAppTheme`, tokens roles/semantic, badges, cartes, resume modules.
* `math.test.js` conserve l exemple simple.

## Offline Strategy

* Packages critiques en `frontend/vendor` (stubs). Pas d acces reseau necessaire.
* Scripts CLI stubs rappellent comment migrer vers les dependances reelles.
* Documentation supplementaire sous `docs/frontend/design-system.md` pour l usage des tokens.

VALIDATE requis par Sam avant integration finale.
