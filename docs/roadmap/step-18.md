# Step 18 - Role Utilization ASCII Report

But

* Produire un rapport ASCII sur la charge des roles et les alertes de saturation.
* Exposer le rendu via l'API micro (telechargement text/plain) et un script Windows-friendly.
* Documenter le workflow et archiver un exemple `.txt` dans `.codex`.

Contexte

* Les snapshots contiennent les charges horaires par role (allocated vs available) mais aucune synthese exploitable.
* Les alertes generiques du dashboard ne suffisent pas a quantifier les risques de surcharge role par role.
* Les contraintes ASCII/PowerShell imposent des sorties CRLF et une CLI simple sans dependances externes.

Taches

1. Service role utilization

   * Nouveau module `backend/app/services/utilization.py` chargeant le snapshot et calculant les taux d'utilisation.
   * Configurer un seuil cible `DEFAULT_UTILIZATION_TARGET = 0.75` (ratio) et exposer `UtilizationTargetError`.
   * Renvoyer un payload structure (`collect_role_utilization`) + rendu ASCII CRLF (`render_role_utilization_ascii`).

2. Endpoint API

   * Ajouter `GET /api/roles/role-utilization.txt[?target=85]` retournant `text/plain` (ASCII CRLF).
   * Valider le parametre `target` (0 < target <= 100) et lever `invalid_target`/`utilization_report_not_found`.
   * Tester dans `backend/tests/test_api_role_utilization.py`.

3. Script & documentation

   * Script `python -m scripts.export_role_utilization --target 80 --out build/roles/role-utilization.txt`.
   * Note `docs/backend/role-utilization-report.md` + README (section Role Utilization ASCII Report).
   * Tests CLI `backend/tests/test_export_role_utilization_script.py` + service `test_role_utilization_services.py`.

4. Archives & roadmap

   * Archiver un exemple ASCII sous `.codex/sessions/step-18/` (rapport + README recap commande).
   * Documenter l'execution dans `docs/roadmap/step-18.md` (section Execution) et referencer dans PR.

Deliverables

* Service role utilization + tests unitaires.
* Endpoint API ASCII + tests dedies.
* Script CLI + documentation + archive `.codex`.

Acceptance Criteria

* `collect_role_utilization()` marque `lumiere` en `alert` (utilisation >= 0.75) et ordonne par utilisation.
* L'endpoint `/api/roles/role-utilization.txt?target=60` repond 200 (ASCII) et indique au moins 2 alertes.
* Le script CLI genere un fichier CRLF ASCII, documente dans `docs/backend/role-utilization-report.md` et reference dans `.codex`.

## Execution Step 18

### Services & Tests

* Module `backend/app/services/utilization.py` calcule les taux d utilisation, trie les roles et marque les alertes selon le seuil (0.75 par defaut).
* Tests `backend/tests/test_role_utilization_services.py` couvrent ordre, alertes, validation de seuil et rendu ASCII.

### API

* Route `GET /api/roles/role-utilization.txt` expose le rapport ASCII CRLF et gere `target` (0-100) avec erreurs `invalid_target` / `utilization_report_not_found`.
* Tests `backend/tests/test_api_role_utilization.py` valident reussite, surcharge de seuil et erreurs de validation.

### Script, Docs & Archives

* CLI `python -m scripts.export_role_utilization --out .codex/sessions/step-18/role-utilization-2024-06-10.txt --target 80` genere le fichier archive (ASCII CRLF).
* Documentation `docs/backend/role-utilization-report.md` + README (section Role Utilization ASCII Report) mis a jour.
* Archive disponible dans `.codex/sessions/step-18/` avec README recap commande.

VALIDATE? yes
