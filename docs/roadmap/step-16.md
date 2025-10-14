# Step 16 - Crew Roster CSV Export

But

* Livrer un roster techniciens au format CSV ASCII filtre par date.
* Exposer le flux via l'API micro (telechargement text/csv) et un script Windows-friendly.
* Documenter le workflow et archiver un exemple `.csv` dans `.codex`.

Contexte

* Les day sheets (Step 15) couvrent le besoin plateau mais la compta requiert un CSV pour retravailler les rosters.
* Les assignments demo contiennent toutes les informations necessaires (horaires, techniciens, lieux, statuts).
* Les contraintes ASCII/PowerShell imposent des retours CRLF et une CLI simple sans dependances externes.

Taches

1. Service roster

   * Nouveau module `backend/app/services/roster.py` filtrant les assignments par date (`YYYY-MM-DD`).
   * Normaliser les statuts inclus (par defaut `confirmed`, `in-progress`) et lever des erreurs claires (`RosterDateError`, `RosterNotFoundError`).
   * Produire un rendu CSV ASCII (`\r\n`) via `render_roster_csv()`.

2. Endpoint API

   * Ajouter `GET /api/rosters/crew-roster.csv?date=YYYY-MM-DD[&statuses=a,b]` retournant `text/csv`.
   * Valider le format date (422), la presence du parametre (422) et l'absence de donnees (404).
   * Tester dans `backend/tests/test_api_roster.py` (succes + erreurs).

3. Script & documentation

   * Script `python -m scripts.export_roster_csv --date 2024-06-10 --out build/rosters/crew-roster-2024-06-10.csv`.
   * Note `docs/backend/crew-roster-csv.md` + mise a jour `README.md` (section Crew Roster CSV).
   * Archiver `crew-roster-2024-06-10.csv` sous `.codex/sessions/step-16/` avec README recap commande.

Deliverables

* Service roster + tests unitaires.
* Endpoint API CSV + tests dedies.
* Script CLI + documentation + archive ASCII.

Acceptance Criteria

* Un appel `collect_roster("2024-06-10")` retourne au moins l'assignation confirmee Malik avec horaire correct.
* L'endpoint `/api/rosters/crew-roster.csv` repond 200 (text/csv) pour une date valide et 422/404 pour erreurs.
* Le script CLI cree un fichier CRLF ASCII, documente dans `docs/backend/crew-roster-csv.md` et reference dans `.codex`.

## Execution Step 16

### Service & Tests

* Module `backend/app/services/roster.py` fournit `collect_roster()` + `render_roster_csv()` (CSV ASCII CRLF).
* Tests `backend/tests/test_roster_services.py` valident filtres date/statuts et encodage CRLF.

### API

* Route `GET /api/rosters/crew-roster.csv` renvoie `text/csv` et gere 422/404 (tests `backend/tests/test_api_roster.py`).

### Script, Docs & Archives

* CLI `python -m scripts.export_roster_csv` cree les dossiers et affiche un recap ASCII.
* Documentation `docs/backend/crew-roster-csv.md` + README (section Crew Roster CSV).
* Archive `.codex/sessions/step-16/crew-roster-2024-06-10.csv` + README recap commande/statuts.

VALIDATE? yes
