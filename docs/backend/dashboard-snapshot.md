# Snapshot Dashboard Orga - Step 05

Cette note decrit le snapshot de donnees Orga fourni pour le dashboard offline.

## Objet

* Proposer un export deterministe versionne pour alimenter le frontend.
* Garantir la compatibilite Windows/PowerShell (commandes `python -m`).
* Documenter le schema JSON et la procedure de regeneration.

## Structure

Le backend expose des dataclasses dans `backend/app/models/orga.py` et un provider deterministe `backend/app/data/sample_snapshot.py`. Les services du module `backend/app/services/dashboard.py` composent ce snapshot et produisent des agregats KPI.

La serialization respecte le schema `tools/schemas/dashboard-snapshot.schema.json`.

```
DashboardSnapshot
  generatedAt: ISO-8601 UTC
  projects[]: { id, name, status, start, end }
  missions[]: { id, project_id, title, status, scheduled, duration_hours }
  people[]: { id, full_name, role, availability }
  roleLoads[]: { role, allocated_hours, available_hours }
  budgets[]: { project_id, planned_amount, actual_amount }
  alerts[]: string
```

## Export JSON

Commande PowerShell (depuis la racine repo):

```ps1
python -m scripts.export_dashboard_snapshot --out frontend/public/data/dashboard-snapshot.json
```

Options:

* `--indent`: niveau d indentation (defaut `2`).
* `--out`: cible alternative pour tester un export.

L export genere un fichier ASCII (UTF-8) deterministe. Le script cree les dossiers intermediaires si necessaire.

## Politique de version

* Le snapshot reste court (< 5 KB) pour faciliter la relecture en diff.
* Tout changement fonctionnel doit mettre a jour simultanement le schema JSON et les tests `backend/tests/test_dashboard_services.py`.
* Les dates et montants sont fixes pour garantir des KPIs reproductibles.

## Tests

`pytest` couvre:

* La determinisme de `build_dashboard_snapshot()`.
* Les KPIs calcules par `summarize_snapshot()` (missions, budgets, role loads).
* La conformite schema via un validateur interne (fallback local si `jsonschema` absent).
