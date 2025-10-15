# Step 17 - Budget Variance ASCII Report

But

* Produire un rapport budgets vs reels ASCII pour la cellule finance/compta.
* Exposer le rendu via l API micro et un script Windows-friendly.
* Documenter le workflow et archiver un exemple `.txt` dans `.codex`.

Contexte

* Les exports Step 15-16 couvrent plateau (day sheet, roster) mais pas le suivi budgetaire.
* Le snapshot dashboard inclut des lignes budgets/planned vs actual utilisables sans nouvelle source.
* Les contraintes ASCII/PowerShell imposent CRLF et zero dependance externe.

Taches

1. Service budget variance

   * Nouveau module `backend/app/services/budgets.py` chargeant le snapshot et calculant deltas/ratios.
   * Configurer un seuil d alerte (`DEFAULT_ALERT_THRESHOLD = 2000`) et exposer `BudgetThresholdError`.
   * Rendre `render_budget_variance_ascii()` (texte CRLF) et trier par ecart.

2. Endpoint API

   * Ajouter `GET /api/budgets/budget-variance.txt[?threshold=EUR]` retournant `text/plain`.
   * Valider seuil (`422 invalid_threshold`, `404 budget_report_not_found`).
   * Tester dans `backend/tests/test_api_budget.py`.

3. Script & documentation

   * Script `python -m scripts.export_budget_variance --threshold 5000 --out build/budgets/budget-variance.txt`.
   * Note `docs/backend/budget-variance-report.md` + README (section Budget Variance ASCII Report).
   * Tests CLI `backend/tests/test_export_budget_variance_script.py` + service `test_budget_services`.

4. Archives & roadmap

   * Archiver un exemple ASCII sous `.codex/sessions/step-17/` (rapport + README).
   * Documenter l execution dans `docs/roadmap/step-17.md` (section Execution) et referencer dans PR.

Deliverables

* Service budget variance + tests unitaires.
* Endpoint API ASCII + tests dedies.
* Script CLI + documentation + archive `.codex`.

Acceptance Criteria

* `collect_budget_variance()` marque `p-aurora` en `alert` avec delta `2800` (seuil defaut 2000).
* L endpoint `/api/budgets/budget-variance.txt` repond 200 (ASCII) et accepte `threshold=5000`.
* Le script CLI genere un fichier CRLF ASCII et imprime resume (threshold, projets, alerts).

## Execution Step 17

### Service & Tests

* Module `backend/app/services/budgets.py` calcule les deltas/ratios depuis le snapshot et attribue le statut `alert` lorsque |delta| >= seuil.
* Campagne `pytest` (voir log Step 17) couvre les services (`test_budget_services.py`), l API (`test_api_budget.py`) et le script CLI (`test_export_budget_variance_script.py`).

### API

* Route `GET /api/budgets/budget-variance.txt` expose le rendu ASCII CRLF avec en-tete `BUDGET VARIANCE REPORT` et lignes `Status: ALERT/OK`.
* Les tests API valident le code 200, la surcharge de seuil (`threshold=5000`) et les erreurs `invalid_threshold`/`budget_report_not_found`.

### Script, Docs & Archives

* Export effectue via `python -m scripts.export_budget_variance --out .codex/sessions/step-17/budget-variance-2024-06-10.txt` (CRLF, seuil 2000 EUR).
* Documentation mise a jour (`docs/backend/budget-variance-report.md`, README section Budget Variance ASCII Report).
* Archive disponible dans `.codex/sessions/step-17/` (rapport texte + README de commande).

VALIDATE? yes
