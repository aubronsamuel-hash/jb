# Step 15 - Day Sheet ASCII Exports

But

* Livrer un day sheet ASCII deterministe pour les chefs de plateau (journee cible).
* Exposer le rendu via l'API micro (texte brut) et un script Windows-friendly.
* Documenter le workflow et archiver un exemple `.txt` dans `.codex`.

Contexte

* Les flux ICS (Step 14) adressent l'agenda individuel mais la production demande un day sheet partage.
* Les assignments demo contiennent les informations necessaires (horaires, missions, lieux, techniciens).
* Les contraintes ASCII/PowerShell imposent des retours CRLF et des scripts simples sans dependances exotiques.

Taches

1. Service day sheet

   * Nouveau module `backend/app/services/daysheet.py` filtrant les assignments par date (`YYYY-MM-DD`).
   * Normaliser les statuts inclus (par defaut `confirmed`, `in-progress`) et lever des erreurs claires (`DaySheetDateError`, `DaySheetNotFoundError`).
   * Rendre un payload structure + rendu ASCII (`\r\n`) via `render_day_sheet_ascii()`.

2. Endpoint API

   * Ajouter `GET /api/daysheets/day-sheet.txt?date=YYYY-MM-DD[&statuses=a,b]` retournant `text/plain`.
   * Valider le format date (422), la presence du parametre (422) et l'absence de donnees (404).
   * Tester dans `backend/tests/test_api_daysheet.py` (succes + erreurs).

3. Script & documentation

   * Script `python -m scripts.export_day_sheet --date 2024-06-10 --out build/day-sheets/2024-06-10.txt`.
   * Note `docs/backend/day-sheets.md` + mise a jour `README.md` (section Day Sheet ASCII).
   * Archiver `day-sheet-2024-06-10.txt` sous `.codex/sessions/step-15/` avec README recap commande.

Deliverables

* Service day sheet + tests unitaires.
* Endpoint API texte + tests dedicaces.
* Script CLI + documentation + archive ASCII.

Acceptance Criteria

* Un appel `collect_day_sheet("2024-06-10")` retourne au moins l'assignation confirmee Malik avec fenetre horaire correcte.
* L'endpoint `/api/daysheets/day-sheet.txt` repond 200 (plain text) pour une date valide et 422/404 pour erreurs.
* Le script CLI cree un fichier CRLF ASCII, documente dans `docs/backend/day-sheets.md` et reference dans `.codex`.

## Execution Step 15

### Service & Tests

* Module `backend/app/services/daysheet.py` filtre les assignments (`confirmed`/`in-progress`) et genere un rendu ASCII CRLF.
* Tests `backend/tests/test_daysheet_services.py` valident date, statuts optionnels et encodage ASCII.

### API

* Route `GET /api/daysheets/day-sheet.txt` (micro API) retourne `text/plain` et gere 422/404 selon les erreurs.
* Tests `backend/tests/test_api_daysheet.py` couvrent succes et validations (`missing_date`, `invalid_date`, `day_sheet_not_found`).

### Script, Docs & Archives

* CLI `scripts/export_day_sheet.py` produit un fichier CRLF, logs deterministes (`Date`, `Assignments`, `Output`).
* Documentation `docs/backend/day-sheets.md` + README mis a jour (section Day Sheet ASCII).
* Archive `.codex/sessions/step-15/day-sheet-2024-06-10.txt` + README recap commande/statuts.

VALIDATE? yes
