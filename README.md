# Projet - Bootstrap Codex

Ce depot est initialise par l agent Codex pour un cycle de dev autonome base sur steps. Voir `docs/roadmap` et `AGENT.codex.md`.

## Frontend Coulisses Crew (Step 10)

Le frontend React 18 + TypeScript repose toujours sur des stubs locaux (Vite, Storybook, Playwright) compatibles PowerShell, mais l architecture est maintenant alignee sur la specification Coulisses Crew v1.

* Entrypoint : `frontend/src/main.ts` re-exporte `initializeApp()` qui installe router, Query Client, theming clair/sombre et i18n.
* Architecture : dossiers `app/`, `components/`, `features/`, `pages/`, `i18n/`, `state/`, `styles/`, `stories/`, `tests/`. Les providers composent React Query, theme, routing et Toast manager.
* Design system : composants accessibles (`Button`, `Dialog`, `Tabs`, `Tooltip`, `DataTable`, `Avatar`, `Badge`...) exposes via `frontend/src/components/ui`. Tokens Tailwind et resume du theme dans `frontend/src/app/theme.ts`.
* Etat : store Zustand (`frontend/src/state/theme-store.ts`) pour le mode sombre et Query Client preprime (`frontend/src/app/query-client.ts`).
* Localisation : i18n francais (`frontend/src/i18n`) base sur un shim i18next.
* Documentation : `docs/frontend/coulisses-crew-frontend.md` decrit les commandes et conventions accessibilite/perf.

Scripts npm (depuis `frontend/`):

```ps1
npm run dev        # stub Vite (message informatif)
npm run build      # stub build
npm run preview    # stub preview
npm run lint       # rappel sur ESLint/Prettier a activer
npm run typecheck  # rappel sur tsc strict
npm run storybook  # stub Storybook 8
npm run test       # tests vitest stubs
npm run e2e        # stub Playwright
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

## Paie & Feuilles de temps (Step 09)

Le module paie fournit un dataset deterministe et des exports ASCII pour les besoins URSSAF/compta.

* Commande export : `python -m scripts.export_payroll_reports --out build/payroll`.
* Fichiers generes : `payroll-report.csv` (tableau par collaborateur) et `payroll-report.pdf` (stub ASCII).
* Documentation : `docs/backend/payroll-timesheets.md`.

## Calendrier ICS (Step 14)

Les flux calendaires exposent les assignations confirmees sous forme ICS securisee par token.

* Endpoint : `GET /api/calendar/assignments.ics?scope=<scope>&token=<token>` (Content-Type `text/calendar; charset=utf-8`).
* Script PowerShell-friendly : `python -m scripts.export_calendar_feed --scope USER:crew-malik --out build/calendar/malik.ics`.
* Documentation : `docs/backend/calendar-ics-feeds.md`.

## Day Sheet ASCII (Step 15)

Les day sheets consolidant les techniciens confirmes/in-progress sont disponibles en texte ASCII (CRLF).

* Endpoint : `GET /api/daysheets/day-sheet.txt?date=YYYY-MM-DD[&statuses=confirmed,in-progress]` (`text/plain; charset=utf-8`).
* Script : `python -m scripts.export_day_sheet --date 2024-06-10 --out build/day-sheets/2024-06-10.txt`.
* Documentation : `docs/backend/day-sheets.md`.


## Crew Roster CSV (Step 16)

Les rosters techniciens sont disponibles au format CSV ASCII (CRLF).

* Endpoint : `GET /api/rosters/crew-roster.csv?date=YYYY-MM-DD[&statuses=confirmed,in-progress]` (`text/csv; charset=utf-8`).
* Script : `python -m scripts.export_roster_csv --date 2024-06-10 --out build/rosters/crew-roster-2024-06-10.csv`.
* Documentation : `docs/backend/crew-roster-csv.md`.
