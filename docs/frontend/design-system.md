# Design System Orga - Step 04

Cette note decrit le design system minimal mis en place a l etape 04 pour l application Orga.

## Objectifs

* Harmoniser les tokens (palette, surfaces, typographie, spacing, elevations, transitions) avec la spec visuelle fournie.
* Exposer des helpers stubs (`createRoleBadge`, `createKpiCard`, `createModuleSummary`, `describeThemeModes`) utilisables par les futures vues React.
* Garantir un fonctionnement offline deterministe et ascii-only.

## Structure des Dossiers

```
frontend/src/app/
  theme.js                # Modes clair/sombre, palette role, tokens
  design-system/
    tokens.js             # Export tokens et helpers design system
    components.js         # RoleBadge, KpiCard, ModuleSummary stubs
    index.js              # Point d entree pour import facilite
```

## Tokens Principaux

* **Modes**: `light` (par defaut) et `dark`. Chaque mode expose `background`, `surface`, `surfaceAlt`, `text`, `border`, `muted`.
* **Palette Roles**: lumiere (jaune 600), son (bleu 500), video (vert 500), plateau (gris 500), hmc (rose 500), admin (orange 500), artiste (violet 500), production (cyan 500).
* **Semantic Colors**: `info`, `success`, `warning`, `danger` derives de la palette role.
* **Spacing Scale**: `xxs` a `xxl` (0.25rem a 2.5rem) + `gutter`, `section`.
* **Typography**: familles `sans` et `mono`; styles `display`, `headline`, `title`, `subtitle`, `body`, `caption` (font-size, line-height, weight, letter-spacing en rem).
* **Radius**: `none`, `xs`, `sm`, `md`, `lg`, `xl`, `full`.
* **Elevations**: `flat`, `raised`, `overlay` (valeurs box-shadow compatibles Tailwind).
* **Transitions**: `default`, `emphasis`, `gentle` (durees ms, timing function).

`tailwind.config.ts` importe `appThemeTokens` (mode clair) et expose `extend.colors`, `extend.borderRadius`, `extend.fontFamily`, `extend.boxShadow` et `extend.spacing`.

## Helpers Stubs

* `getRoleColor(role, theme?)`: renvoie la couleur hex associee au role (fallback sur `roleColors.production`).
* `describeThemeModes()`: retourne une liste avec resume palette (background, surface, text, accent) pour chaque mode.
* `createRoleBadge({ id, label, role, tone })`: structure JSON `{ type: 'ds-role-badge', role, color, tone, label }`.
* `createKpiCard({ id, title, value, trend })`: structure JSON `{ type: 'ds-kpi-card', surface, emphasis, metrics }`.
* `createModuleSummary({ id, title, description, roles })`: structure JSON reliant roles a leurs couleurs.

Ces helpers ne produisent pas de DOM mais facilitent les tests et un futur portage vers des composants React (shadcn/ui, etc.).

## Scripts

* `npm run storybook` (stub) appelle `frontend/scripts/storybook.js` qui explique comment serait lance un catalogue UI lorsqu on remplacera les stubs par Storybook reelle.

## Tests

`frontend/tests/design-system.test.js` verifie:

* La generation de theme pour `light` et `dark` (background, text, semantic colors).
* La disponibilite des couleurs role et la logique de fallback.
* Les helpers `createRoleBadge`, `createKpiCard`, `createModuleSummary` et `describeThemeModes`.

Les tests existants (`app-routing.test.js`) sont ajustes pour exploiter le resume de theme mis a jour.

## Utilisation Futur

* Le layout Dashboard pourra mapper `createKpiCard` sur les indicateurs (heures, budget, disponibilite).
* Les modules Planning et RH utiliseront `createModuleSummary` pour afficher roles et equipes.
* Les feuilles de route pourront reutiliser `getRoleColor` pour colorer les services.

La migration vers un Storybook reel consistera a remplacer le stub par `@storybook/react-vite` et a reexporter ces helpers en composants React tipises.
