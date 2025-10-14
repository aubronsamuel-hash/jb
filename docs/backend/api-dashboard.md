# API Dashboard Orga - Step 08

Cette note decrit le service HTTP interne expose pour le snapshot Orga.

## Objet

* Servir le snapshot deterministe et son resume KPI via HTTP.
* Permettre aux equipes frontend et produit de consommer la meme source que les exports JSON.
* Documenter les commandes Windows/PowerShell pour lancer et tester le service.

## Lancement local

Demarrage serveur (depuis la racine du depot):

```ps1
python -m backend.app.api.server --host 127.0.0.1 --port 8000
```

Les options `--host` et `--port` restent explicites pour PowerShell. Le serveur embarque utilise `wsgiref.simple_server` et l application est exposee via `backend.app:app`.

## Routes

| Methode | Path                        | Description                          |
|---------|-----------------------------|--------------------------------------|
| GET     | `/health`                   | Check readiness renvoyant `{"status": "ok"}`. |
| GET     | `/api/dashboard/snapshot`   | Snapshot integrale serialise, conforme au schema JSON Step 05. |
| GET     | `/api/dashboard/summary`    | Resume KPI derive du snapshot (missions, budgets, roles, alerts). |

Toutes les reponses sont encodees en JSON ASCII, compatibles avec les contraintes Windows-first.

## Payloads

* `/api/dashboard/snapshot` retourne la sortie de `serialize_snapshot()` (voir `backend/app/services/dashboard.py`).
* `/api/dashboard/summary` retourne la sortie de `summarize_snapshot()`.

La valeur `generatedAt` et les donnees deterministes correspondent au provider `backend/app/data/sample_snapshot.py`.

## Tests

`pytest` couvre les trois routes via `backend.app.api.testing.ApiTestClient` et valide:

* Status HTTP 200.
* Determinisme du champ `generatedAt`.
* Correspondance entre API et services Python.
