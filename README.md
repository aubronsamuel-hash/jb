# Projet - Bootstrap Codex

Ce depot est initialise par l agent Codex pour un cycle de dev autonome base sur steps. Voir docs/roadmap et AGENT.codex.md.

# jb

## Tests Locaux

Backend (pytest):

```
python -m pip install -r requirements-dev.txt
pytest
```

> La couverture minimale est fournie par le shim local `pytest_cov`, aucun
> paquet externe n est requis.

Frontend (vitest):

```
cd frontend
npm ci
npm test
```
