# Projet - Bootstrap Codex

Ce depot est initialise par l agent Codex pour un cycle de dev autonome base sur steps. Voir `docs/roadmap` et `AGENT.codex.md`.

## Frontend Orga (Step 04)

Le frontend React/Vite reste en mode offline avec stubs locaux. Cette etape ajoute un design system minimal conforme a la spec visuelle.

* Entrypoint : `frontend/src/main.js` expose `initializeApp()`.
* Providers : Query Client, Theme tokens, Router (voir `docs/frontend/architecture.md`).
* Design system : tokens modes clair/sombre, palette roles, helpers (`createRoleBadge`, `createKpiCard`, `createModuleSummary`). Documentation sous `docs/frontend/design-system.md`.
* Navigation : Dashboard, Planning, Missions, Equipes, Materiel, Budgets, Notifications, Parametres.
* Configs : `frontend/vite.config.ts`, `frontend/tailwind.config.ts`, `frontend/tsconfig.json`, `frontend/postcss.config.cjs`.

Scripts npm (depuis `frontend/`):

```ps1
npm run dev       # lance le stub Vite en mode dev (affiche un message)
npm run build     # stub build
npm run preview   # stub preview
npm run storybook # stub design system / instructions Storybook
npm test          # lance les tests vitest stubs
```

## Tests Locaux

### Backend (pytest)

```ps1
python -m pip install -r requirements-dev.txt
pytest
```

> La couverture minimale est fournie par le shim local `pytest_cov`, aucun paquet externe n est requis.

### Frontend (vitest)

```ps1
cd frontend
npm test
```

Les tests front s appuient sur le runner stub `frontend/vendor/vitest` et couvrent la configuration router/navigation ainsi que les tokens du design system.
