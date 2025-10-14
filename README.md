# Projet - Bootstrap Codex

Ce depot est initialise par l agent Codex pour un cycle de dev autonome base sur steps. Voir `docs/roadmap` et `AGENT.codex.md`.

## Frontend Orga (Step 05)

Le frontend React/Vite reste en mode offline avec stubs locaux. Cette etape ajoute un snapshot Orga deterministe et relie le dashboard aux helpers du design system.

* Entrypoint : `frontend/src/main.js` expose `initializeApp()`.
* Providers : Query Client, Theme tokens, Router (voir `docs/frontend/architecture.md`).
* Design system : tokens modes clair/sombre, palette roles, helpers (`createRoleBadge`, `createKpiCard`, `createModuleSummary`, `createNavigationRoleBadges`) et layout dashboard (`createDashboardLayout`). Documentation sous `docs/frontend/design-system.md`.
* Snapshot Orga : `frontend/public/data/dashboard-snapshot.json` (generer via `python -m scripts.export_dashboard_snapshot`). Charge offline par `loadDashboardSnapshot()`.
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

## Backend API (Step 08)

Le service HTTP repose sur une micro pile interne pour servir le snapshot Orga et son resume KPI.

* Lancement : `python -m backend.app.api.server --host 127.0.0.1 --port 8000`.
* Verification rapide (PowerShell) : `Invoke-RestMethod http://127.0.0.1:8000/health` renvoie `{ status = "ok" }`.
* Routes clefs : `/health`, `/api/dashboard/snapshot`, `/api/dashboard/summary` (spec backend v0.2 / frontend v0.2).

Les reponses restent ASCII pour respecter les contraintes Windows-first. Consultez `docs/backend/api-dashboard.md` pour le detail des payloads et la procedure complete.
