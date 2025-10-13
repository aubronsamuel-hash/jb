# Step 04 - Design System Minimal & Tokens Orga

But

* Poser un design system minimal pour Orga conforme a la vision visuelle (palette metiers, surfaces, typographie, elevations).
* Mettre a jour le theme frontend avec modes clair/sombre, tokens semantiques, et utilitaires pour composants (badges roles, cartes KPI).
* Introduire une documentation de reference sur les tokens et sur l usage des composants stub en attendant l integration React reelle.
* Etendre la base de tests pour couvrir la coherence des tokens (roles, surfaces, transitions) et les generateurs de composants.

Contexte

* La spec visuelle "Application ORGA" decrit les attentes UI (dashboard, modules, couleurs metiers, exports, notifications).
* Step 03 a mis en place la structure React/Vite/Tailwind avec un theme tres simple. Step 04 doit enrichir ce theme pour preparer les ecrans du dashboard et des modules planifies.
* Les stubs doivent rester offline et ascii-only afin de respecter AGENT.codex.

Taches

1. Tokens et Theme

   * Creer une palette Orga pour mode clair et sombre avec roles metiers: lumiere, son, video, plateau, hmc, admin, artiste, production.
   * Ajouter tokens semantiques (background, surface, border, text, info, success, warning, danger) et echelles (spacing, radius, typography, elevations, transitions).
   * Offrir une fonction `getRoleColor` et utilitaires associes pour fournir les couleurs aux composants stubs.
   * Mettre a jour `tailwind.config.ts` pour exposer la palette actualisee.

2. Design System Stub

   * Ajouter un dossier `frontend/src/app/design-system/` avec tokens exportes, helpers `createRoleBadge`, `createKpiCard`, `createModuleSummary` et `describeThemeModes` (structures JSON pour tests et storybook futur).
   * Connecter ces helpers au layout ou a la navigation si pertinent (sans DOM reel) afin de demontrer l usage des tokens.
   * Ajouter un script npm `storybook` (stub) sous `frontend/scripts/storybook.js` qui explique comment lancer un futur catalogue UI.

3. Documentation

   * Ajouter `docs/frontend/design-system.md` avec la structure des tokens, roles, composants stubs et commandes.
   * Ajouter une spec visuelle `docs/specs/spec-orga-visual-v1.md` reprenant les sections clefs (dashboard, projets, planning, RH, materiel, feuille de route, notifications, charte) en ascii-only.
   * Mettre a jour `docs/frontend/architecture.md` (section Step 04) et `README.md` pour pointer vers le design system et la palette roles.

4. Tests

   * Ajouter `frontend/tests/design-system.test.js` validant `createAppTheme` (modes clair/sombre), `getRoleColor`, `createRoleBadge`, `createKpiCard`, `createModuleSummary`.
   * Mettre a jour les tests existants si necessaire pour refleter le nouveau resume de theme.

5. Archives

   * Creer `.codex/sessions/step-04/notes.md` listant les changements principaux et `.codex/sessions/step-04/tests.log` avec la sortie `npm test`.

Deliverables

* Docs: `docs/roadmap/step-04.md`, `docs/frontend/design-system.md`, `docs/specs/spec-orga-visual-v1.md`, mise a jour README et architecture.
* Code: `frontend/src/app/theme.js` enrichi, nouveau dossier `frontend/src/app/design-system/` avec helpers, `tailwind.config.ts` ajuste.
* Scripts: `frontend/scripts/storybook.js` + script npm.
* Tests: `frontend/tests/design-system.test.js`, mise a jour `frontend/tests/app-routing.test.js` si besoin.
* Archives: `.codex/sessions/step-04/notes.md`, `.codex/sessions/step-04/tests.log`.

Acceptance Criteria

* `npm test` passe avec les nouveaux tests.
* `createAppTheme` renvoie des tokens coherents pour les modes `light` et `dark` et la palette expose les roles metiers.
* Les helpers design system renvoient des structures deterministes basees sur les tokens.
* La documentation reference clairement la palette metiers et le script storybook explique le workflow offline.

Commandes Locales Exemples

* Frontend tests:
  cd frontend
  npm test
* Storybook stub:
  npm run storybook

Notes

* Ref PR: `Ref: docs/roadmap/step-04.md`.
* Aucun asset binaire, ascii-only.

VALIDATE? yes/no
