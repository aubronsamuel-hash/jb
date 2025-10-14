# Step 09 - Payroll Timesheets Baseline

But

* Livrer un noyau paie/feuilles de temps conforme a la spec backend v0.2.
* Fournir un dataset deterministe et des exports ASCII (CSV/PDF stub) pour URSSAF/compta.
* Documenter la procedure PowerShell pour generer les feuilles de temps et le rapport de paie.

Contexte

* Step 08 expose l API dashboard consommee par les equipes Orga.
* La roadmap backend enchaine sur le module paie afin de securiser les workflows administratifs.
* Les squads compta ont besoin d un calcul brut/net reproduisible avant d activer les integrations externes.

Taches

1. Modelisation

   * Ajouter des dataclasses `TimesheetEntry`, `Timesheet`, `PayrollLine`, `PayrollReport`.
   * Introduire un provider deterministe `backend/app/data/sample_timesheets.py`.

2. Service paie

   * Ajouter `backend/app/services/payroll.py` calculant brut/net (charges fixes) et agregeant les heures par utilisateur.
   * Exposer des helpers d export CSV et PDF ASCII (stub) respectant Windows/PowerShell.

3. Scripts & docs

   * Ajouter `scripts/export_payroll_reports.py` permettant `python -m scripts.export_payroll_reports --out build/payroll`.
   * Documenter la commande dans `README.md` et publier `docs/backend/payroll-timesheets.md`.

4. Tests

   * Couvrir les calculs et exports via `backend/tests/test_payroll.py` (ASCII, totaux, presence fichiers).
   * Garantir que les scripts generent du contenu deterministe.

Deliverables

* Code: modeles, service paie, script export.
* Tests: pytest couvre calculs et exports.
* Docs: README + note backend paie.

Acceptance Criteria

* `pytest` passe avec les nouveaux tests.
* `python -m scripts.export_payroll_reports --out build/payroll` cree CSV + PDF ASCII deterministes.
* Les exports contiennent brut/net calcule et heures totales par collaborateur.

VALIDATE? yes/no
