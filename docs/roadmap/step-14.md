# Step 14 - Calendar ICS Feeds Delivery

But

* Offrir aux equipes Orga des flux calendaires ICS a jour (assignations confirmees) pour integration Outlook/Google.
* Garantir la securisation des feeds via tokens deterministes et scopes controles (ALL, USER, PROJECT).
* Documenter l usage API/CLI et archiver un exemple ASCII pour validation release.

Contexte

* Le monitoring release (Step 13) confirme la stabilite de l API mais les equipes terrain demandent un export calendrier.
* Les assignments demo (`sample_assignments`) couvrent plusieurs profils/missions avec horodatage ISO 8601.
* Les contraintes ASCII/Windows-first imposent des retours CRLF et une CLI simple executable en PowerShell.

Taches

1. Service calendar ICS

   * Implementer `backend/app/services/calendar.py` (filtrage `confirmed`, normalisation scope, generation ICS ASCII).
   * Charger les tokens demo via `backend/app/data/sample_calendar_tokens.py` et exposer `available_scopes()` pour les scripts.
   * Couvrir les erreurs (`InvalidScopeError`, `InvalidTokenError`).

2. Endpoint API

   * Etendre `MicroApi` avec `PlainTextResponse` + statut 401 pour servir du texte brut.
   * Ajouter `GET /api/calendar/assignments.ics` (validation scope/token, retour `text/calendar`).
   * Tester via `backend/tests/test_api_calendar.py` (succès + erreurs 422/401).

3. Script & documentation

   * Script `python -m scripts.export_calendar_feed` (auto-token demo, sortie ASCII, creation dossiers).
   * Note `docs/backend/calendar-ics-feeds.md` et mise a jour `README.md` (section Calendrier ICS).
   * Archiver un exemple `.ics` sous `.codex/sessions/step-14/`.

Deliverables

* Service calendar + tokens + tests unitaires.
* Endpoint ICS + tests API.
* Script CLI + documentation + archive ASCII.

## Execution Step 14

### Service & Tokens

* Nouveau module `backend/app/services/calendar.py` genere ICS ASCII (`X-WR-CALNAME`, `UID`, `STATUS:CONFIRMED`).
* Tokens demo exposes via `backend/app/data/sample_calendar_tokens.py` et re-exportes par `available_scopes()`.
* Tests `backend/tests/test_calendar_services.py` couvrent validation scope/token et payload.

### API & Client de test

* `PlainTextResponse` dans `backend/app/api/app.py` + `HttpError.unauthorized` (401) pour tokens invalides.
* Route `/api/calendar/assignments.ics` renvoie `text/calendar` via `PlainTextResponse`.
* `ApiTestClient` mis a jour pour gerer JSON + texte; tests `backend/tests/test_api_calendar.py` valident succes/erreurs.

### Script, Docs & Archives

* CLI `scripts/export_calendar_feed.py` supporte `--scope`, auto-token demo, sortie `build/calendar/assignments.ics`.
* Documentation `docs/backend/calendar-ics-feeds.md` + section `README.md` (usage endpoint/script).
* Archive `.codex/sessions/step-14/assignments-malik.ics` + `README.md` (commande executee, scope/token utilises).

Acceptance Criteria

* Un feed ICS ASCII est disponible pour `USER:crew-malik` et filtre correctement les assignations confirmees.
* L endpoint `/api/calendar/assignments.ics` renvoie 401 sur token invalide et 422 sur scope manquant.
* Le script CLI exporte le fichier ICS en PowerShell (`mkdir` auto) et la documentation reference les commandes.

VALIDATE? yes
