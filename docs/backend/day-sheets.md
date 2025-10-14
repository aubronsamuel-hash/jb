# Day Sheets ASCII (Step 15)

Ce guide explique comment generer et consommer les day sheets ASCII exposes par le backend Coulisses Crew.

## Service

* Module : `backend/app/services/daysheet.py`.
* Fonction : `collect_day_sheet(date: str, include_statuses: Sequence[str] | None = None)` retourne une structure deterministe filtree sur `YYYY-MM-DD`.
* Statuts par defaut : `confirmed`, `in-progress` (configurables via `include_statuses`).
* Rendu ASCII : `render_day_sheet_ascii(payload)` retourne une chaine CRLF safe et 100% ASCII.

## Endpoint API

```
GET /api/daysheets/day-sheet.txt?date=2024-06-10[&statuses=confirmed,in-progress]
Content-Type: text/plain; charset=utf-8
```

* `date` (obligatoire) : format `YYYY-MM-DD`.
* `statuses` (optionnel) : liste separee par des virgules (ex : `confirmed,in-progress,pending`).
* Erreurs :
  * 422 `missing_date` si parametre absent/vide.
  * 422 `invalid_date` si format invalide.
  * 404 `day_sheet_not_found` si aucun assignment ne matche les criteres.

## Script CLI

Commande PowerShell friendly :

```ps1
python -m scripts.export_day_sheet --date 2024-06-10 --out build/day-sheets/2024-06-10.txt
```

* Le script cree automatiquement les dossiers et respecte les retours CRLF (`newline=""`).
* Options :
  * `--statuses confirmed,in-progress,pending` pour inclure d'autres statuts.
  * `--out` permet de controler le chemin du fichier genere.
* Sortie :
  * `Date: <date>`
  * `Assignments: <nombre>`
  * `Output: <chemin>`

## QA rapide

1. Executer `pytest backend/tests/test_daysheet_services.py backend/tests/test_api_daysheet.py`.
2. Verifier que `scripts/export_day_sheet` produit un fichier ASCII (`file.write_text(..., newline="")`).
3. Archiver la sortie dans `.codex/sessions/step-15/` pour audit.
