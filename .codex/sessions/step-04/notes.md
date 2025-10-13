# Step 04 Notes

* Ajout du plan de travail Step 04 (`docs/roadmap/step-04.md`) et de la spec visuelle (`docs/specs/spec-orga-visual-v1.md`).
* Documentation design system: `docs/frontend/design-system.md` + mise a jour `docs/frontend/architecture.md` et `README.md`.
* Extension theme frontend (`src/app/theme.js`) avec modes clair/sombre, palette roles, spacing, typography, elevations, transitions.
* Nouveau dossier `src/app/design-system/` (tokens, components, index) et enrichissement du dashboard (`views/dashboard-view.js`).
* Mise a jour Tailwind (`tailwind.config.ts`), package npm (`package.json`) et script stub Storybook (`scripts/storybook.js`).
* Nouveau test `tests/design-system.test.js` + ajustement `tests/app-routing.test.js` pour valider le resume de theme.
* Execution `npm test` apres ajustements (voir tests.log) -> tous les tests Vitest stubs passent.
