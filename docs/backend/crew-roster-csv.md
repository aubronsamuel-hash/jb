# Crew Roster CSV (Step 16)

Le roster techniciens fournit un export ASCII (CSV) pour les equipes Orga et Compta.

## Services

* Module `backend/app/services/roster.py` filtre les assignments par date (`YYYY-MM-DD`) et statuts (`confirmed`, `in-progress` par defaut).
* Exceptions levees: `RosterDateError` (format date invalide) et `RosterNotFoundError` (aucune donnee sur la periode).
* `collect_roster()` retourne un payload structure (rows + summary) consomme par l'API et les scripts.
* `render_roster_csv()` produit un texte CSV ASCII avec retour `\r\n` (compatible PowerShell).

## API

* Endpoint: `GET /api/rosters/crew-roster.csv?date=YYYY-MM-DD[&statuses=a,b]`.
* En-tete: `Content-Type: text/csv; charset=utf-8` + `X-Orga-Api`.
* Reponses d'erreur:
  * 422 `missing_date` si `date` absent.
  * 422 `invalid_date` si le format ne suit pas `YYYY-MM-DD`.
  * 404 `roster_not_found` si aucun assignment ne matche les filtres.

## Script CLI

```ps1
python -m scripts.export_roster_csv --date 2024-06-10 --out build/rosters/crew-roster-2024-06-10.csv
```

* Option `--statuses declined` pour changer les statuts inclus (liste separee par des virgules).
* Le script affiche un recap ASCII (Date, Assignments, Output) et cree les dossiers parents si besoin.

## Tests

```ps1
python -m pytest backend/tests/test_roster_services.py backend/tests/test_api_roster.py backend/tests/test_export_roster_csv_script.py
```

Ces tests valident la generation du CSV, les erreurs API et l'encodage CRLF.

## Archives

* `.codex/sessions/step-16/crew-roster-2024-06-10.csv` (export par defaut `confirmed,in-progress`).
* `.codex/sessions/step-16/README.md` (commande executee, statuts inclus).
