# Step 13 - Release Monitoring & Telemetry Bootstrap

But

* Outiller la squad pour verifier en ASCII la sante de l API avant ouverture prod.
* Fournir un resume operations (missions, alertes, planning) exploitable en PowerShell.
* Industrialiser la collecte en script pour diffusion rapide apres chaque deploy.

Contexte

* La release Step 12 est prete mais l equipe manque d un point de verite unique pour confirmer la stabilite.
* Les checkpoints doivent reutiliser les services existants (snapshot, planning) sans dependances externes.
* Les evidences doivent rester ASCII et scriptables pour integration dans `.codex` et les notes de go/no-go.

Taches

1. Service operations

   * Ajouter un module `operations` qui assemble dashboard + planning en un statut release.
   * Exposer version API, etat global et echantillons assignments limite configurable.
   * Garantir un payload 100% ASCII (ids, codes et ratios arrondis).

2. Endpoint API `/api/ops/status`

   * Brancher le service operations dans la micro API.
   * Couvrir via tests les clefs principales (release, dashboard, planning) et ascii.

3. Script CLI `scripts/monitor_release.py`

   * Ajouter un CLI Windows-first qui imprime en ASCII un resume humain et option JSON.
   * Permettre de regler la limite d echantillons assignments.

4. Documentation & archives

   * Documenter le workflow de verification release dans `docs/backend`.
   * Archiver la sortie du script dans `.codex/sessions/step-13/`.

Deliverables

* Module operations + endpoint `/api/ops/status` testes.
* Script CLI `monitor_release.py` avec exemple d utilisation.
* Documentation backend + archive ASCII dans `.codex/sessions/step-13/`.

## Execution Step 13

### Service operations

* Nouveau module `backend/app/services/operations.py` assemble snapshot + planning en statut release ASCII.
* Validation via `test_operations_services.py` (limite param et ids ASCII).

### Endpoint API

* Route `/api/ops/status` expose `release`, `dashboard`, `planning`.
* Tests `backend/tests/test_api_ops.py` garantissent statut `ok` et version `0.2.0`.

### Script & Documentation

* CLI `python -m scripts.monitor_release` supporte `--limit` + `--format json`.
* Guide `docs/backend/ops-release-monitoring.md` documente usage et exemples ASCII.

### Archives

* `.codex/sessions/step-13/ops-status.txt` sortie CLI ASCII.
* `.codex/sessions/step-13/ops-status.json` export JSON de reference.

Acceptance Criteria

* L endpoint `/api/ops/status` renvoie un statut `ok`, la version API et un echantillon assignments ASCII.
* Le script CLI imprime un resume ASCII par defaut et supporte `--format json`.
* La documentation et l archive `.codex/sessions/step-13/` referencent le script et le payload capture.

VALIDATE? yes
