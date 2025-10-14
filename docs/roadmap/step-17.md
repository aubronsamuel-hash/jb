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

* Module `backend/app/services/budgets.py` calcule deltas, ratio %, alerts (tri absolu) + erreurs.
* Tests `backend/tests/test_budget_services.py` couvrent seuil par defaut, override, erreurs et rendu ASCII.

### API

* Route `GET /api/budgets/budget-variance.txt` renvoie `text/plain` + `Status: ALERT/OK`.
* Tests `backend/tests/test_api_budget.py` verifient 200 (ASCII CRLF) et validations `422`.

### Script, Docs & Archives

* CLI `python -m scripts.export_budget_variance` ecrit ASCII CRLF + resume console.
* Documentation `docs/backend/budget-variance-report.md` + README (section Budget Variance).
* Archive `.codex/sessions/step-17/budget-variance-2024-06-10.txt` + README recap commande.

VALIDATE? yes
