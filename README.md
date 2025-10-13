# Projet - Bootstrap Codex

Ce depot est initialise par l agent Codex pour un cycle de dev autonome base sur steps. Voir `docs/roadmap` et `AGENT.codex.md`.

## Frontend Orga (Step 03)

Le frontend est structure en React + Vite + TypeScript (mode offline). Les dependances clefs sont fournies sous `frontend/vendor` (stubs) pour rester deterministes et compatibles Windows/PowerShell.

* Entrypoint : `frontend/src/main.js` expose `initializeApp()`.
* Providers : Query Client, Theme tokens, Router (voir `docs/frontend/architecture.md`).
* Navigation initiale : Dashboard, Planning, Missions, Equipes, Materiel, Budgets, Notifications, Parametres.
* Configs : `frontend/vite.config.ts`, `frontend/tailwind.config.ts`, `frontend/tsconfig.json`, `frontend/postcss.config.cjs`.

Scripts npm (depuis `frontend/`):

```ps1
npm run dev      # lance le stub Vite en mode dev (affiche un message)
npm run build    # stub build
npm run preview  # stub preview
npm test         # lance les tests vitest stubs
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

Les tests front s appuient sur le runner stub `frontend/vendor/vitest` et couvrent la configuration router/navigation.
