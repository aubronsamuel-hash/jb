# Module Paie & Feuilles de Temps - Step 09

Cette note resume le socle paie mis a disposition pour Coulisses Crew.

## Objet

* Fournir un dataset deterministe pour les feuilles de temps hebdomadaires.
* Calculer un rapport paie brut/net avec un taux de charges fixe (22%).
* Generer des exports ASCII (CSV + PDF stub) compatibles Windows/PowerShell.

## Modele

Le module introduit les dataclasses suivantes (voir `backend/app/models/payroll.py`):

* `TimesheetEntry`: declaration d heures pour un utilisateur, mission, date, taux horaire.
* `Timesheet`: periode, devise et collection d entrees.
* `PayrollLine`: agrege les heures, brut, charges et net pour un utilisateur.
* `PayrollReport`: resume global (totaux heures, brut, charges, net).

Les donnees deterministes se trouvent dans `backend/app/data/sample_timesheets.py`.

## Calcul

Le service `backend/app/services/payroll.py` expose:

* `build_payroll_report()` -> rapporte le dataset exemple.
* `compute_payroll_report(timesheet)` -> agrege un objet `Timesheet`.
* `payroll_report_to_csv(report)` / `payroll_report_to_pdf(report)` -> serialisations ASCII.
* `export_payroll_report(output_dir)` -> ecrit CSV + PDF stub.

Le taux de charges est fixe a 22% et converti en centimes avec un arrondi HALF_UP.

## Export

Commande PowerShell (racine repo):

```ps1
python -m scripts.export_payroll_reports --out build/payroll
```

Sortie attendue:

* `payroll-report.csv`: tableau par utilisateur + ligne TOTAL.
* `payroll-report.pdf`: stub ASCII prefixe par `%PDF-Stub 1.0` listant periode, taux et totaux.

Les deux fichiers sont deterministes et encodes en ASCII (UTF-8 sans BOM).

## Tests

`pytest` verifie:

* Les montants par collaborateur (brut, charges, net) et les totaux.
* Le format ASCII des exports CSV/PDF.
* L ecriture sur disque via `write_payroll_report()`.
