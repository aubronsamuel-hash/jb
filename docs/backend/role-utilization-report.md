# Role Utilization ASCII Report (Step 18)

Ce module fournit un rapport ASCII listant l utilisation des roles et les alertes de saturation.

## Objet

* Calculer les taux d utilisation (allocated vs available) a partir du snapshot deterministe.
* Identifier les roles en surcharge en fonction d un seuil cible configurable.
* Offrir une sortie ASCII compatible PowerShell (CRLF) via API et script CLI.

## Service `backend/app/services/utilization.py`

* `collect_role_utilization(target_ratio=None)` charge le snapshot, ordonne les roles par utilisation et renvoie un payload structure.
  Le seuil par defaut est `DEFAULT_UTILIZATION_TARGET = 0.75`.
* `render_role_utilization_ascii(payload)` formate le rapport en texte ASCII (CRLF) avec un resume (totaux, alertes, moyenne).
* Les exceptions `UtilizationTargetError` et `UtilizationReportNotFoundError` couvrent les cas invalides.

## Endpoint API

* `GET /api/roles/role-utilization.txt[?target=85]` retourne `text/plain; charset=utf-8`.
* Parametre `target` optionnel (pourcentage > 0 et <= 100). Erreurs:
  * `invalid_target` (422) pour valeur non numerique ou hors bornes.
  * `utilization_report_not_found` (404) si aucune donnee role n est disponible.

## Script CLI

Commande PowerShell exemple:

```ps1
python -m scripts.export_role_utilization --out build/roles/role-utilization.txt --target 80
```

Sortie console (ASCII):

```
Generated at: 2024-05-06T08:00:00Z
Target utilization: 80.0%
Roles: 4
Alerts: 2
Output: build\roles\role-utilization.txt
```

Le fichier genere termine toujours par `\r\n` et reste ASCII pur.

## Tests

`pytest` couvre:

* `backend/tests/test_role_utilization_services.py`
* `backend/tests/test_api_role_utilization.py`
* `backend/tests/test_export_role_utilization_script.py`
