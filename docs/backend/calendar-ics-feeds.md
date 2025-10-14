# Calendar ICS Feeds (Step 14)

Cette note resume la generation de flux calendaires ICS pour Coulisses Crew.

## Vue d ensemble

* Les flux exposent les assignations confirmees (statut `confirmed`) en lecture seule.
* Les scopes supportes: `ALL`, `USER:<user_id>`, `PROJECT:<mission_id>`.
* Les tokens sont deterministes pour la demo et definis dans `backend/app/data/sample_calendar_tokens.py`.
* Le service produit uniquement de l ASCII et normalise les metadonnees (`X-WR-CALNAME`, `UID`, etc.).

## Service Python

Module: `backend/app/services/calendar.py`

* `build_calendar_feed(scope, token)` valide le scope/token avant de retourner le payload ICS (`\r\n`).
* `normalize_scope()` accepte `ALL`, `all`, scopes vides ou avec prefixe/valeur.
* `available_scopes()` expose la carte scope -> token pour les scripts CLI.

## Endpoint API

```
GET /api/calendar/assignments.ics?scope=<scope>&token=<token>
Content-Type: text/calendar; charset=utf-8
```

* Retourne le contenu ICS brut via `PlainTextResponse` (nouveau wrapper).
* Codes d erreur:
  * 422 `missing_token` si `token` absent ou vide.
  * 422 `invalid_scope` si le scope ne suit pas `PREFIX:valeur`.
  * 401 `invalid_token` si le token ne correspond pas au scope.

## Script CLI

```
python -m scripts.export_calendar_feed --scope USER:crew-malik --out build/calendar/malik.ics
```

* Detecte automatiquement le token demo pour le scope (surchargable via `--token`).
* Cree les repertoires parents et logge scope/token/fichier en ASCII.
* Preserve les fins de ligne `CRLF` lors de l ecriture pour compatibilite PowerShell.

## Archives

* Exemple depose dans `.codex/sessions/step-14/assignments-malik.ics` (scope USER:crew-malik).
* README associe re-capitulant la commande et les tokens utilises.
