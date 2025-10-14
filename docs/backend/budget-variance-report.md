# Budget Variance ASCII Report (Step 17)

Ce module fournit un rapport ASCII listant les budgets planifies vs reels par projet.

## Objet

* Calculer les deltas budgets/projets sur le snapshot deterministe.
* Identifier les alertes lorsque l ecart depasse un seuil configurable.
* Offrir une sortie ASCII compatible PowerShell (CRLF) via API et script CLI.

## Service `backend/app/services/budgets.py`

* `collect_budget_variance(alert_threshold=None)` charge le snapshot et retourne un payload structure
  (projets, totaux, seuil applique). Le seuil par defaut est `2000` EUR.
* `render_budget_variance_ascii(payload)` formate le rapport en texte ASCII (CRLF) avec resume final.
* Les exceptions `BudgetThresholdError` et `BudgetReportNotFoundError` couvrent les cas invalides.

## Endpoint API

* `GET /api/budgets/budget-variance.txt[?threshold=5000]` retourne `text/plain; charset=utf-8`.
* Parametre `threshold` optionnel (entier >= 0). Erreurs:
  * `invalid_threshold` (422) pour valeur non entiere ou negative.
  * `budget_report_not_found` (404) si aucune ligne budget n est disponible.

## Script CLI

Commande PowerShell exemple:

```ps1
python -m scripts.export_budget_variance --out build/budgets/budget-variance.txt --threshold 5000
```

Sortie console (ASCII):

```
Generated at: 2024-05-06T08:00:00Z
Threshold: +/-5000 EUR
Projects: 2
Alerts: 0
Output: build\\budgets\\budget-variance.txt
```

Le fichier genere termine toujours par `\r\n` et reste ASCII pur.

## Tests

`pytest` couvre:

* `backend/tests/test_budget_services.py`
* `backend/tests/test_api_budget.py`
* `backend/tests/test_export_budget_variance_script.py`
