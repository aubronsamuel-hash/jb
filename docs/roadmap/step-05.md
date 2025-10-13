# Step 05 - Dashboard Orga Snapshot & Experience

But

* Fournir un snapshot de donnees Orga (projets, missions, budgets, personnes) exploitable hors ligne.
* Offrir des services backend capables de calculer les KPIs clefs du dashboard (charge roles, statut missions, ecarts budget).
* Alimenter la vue Dashboard frontend avec les helpers du design system pour afficher KPI, alertes et resumes modules.
* Documenter les jeux de donnees, le mapping API -> frontend et les commandes de regeneration.

Contexte

* Step 04 a etabli un design system et des tokens coherents pour tous les roles metiers.
* La spec Orga requiert un dashboard qui resume planning, equipes, budgets et alertes pour Sam et son equipe.
* Aucun backend reel n est disponible; le snapshot doit rester deterministe, versionne, et accessible en lecture seule par le frontend.

Taches

1. Snapshot domaine backend

   * Creer `backend/app/models/orga.py` avec des dataclasses (Project, Mission, Person, RoleLoad, BudgetLine, DashboardSnapshot).
   * Ajouter `backend/app/data/sample_snapshot.py` qui retourne un objet `DashboardSnapshot` contenant: projets actifs, missions par statut, personnes disponibles, budgets prevu/reel, alertes (conflits planning, depassements).
   * Prevoir un schema JSON (`tools/schemas/dashboard-snapshot.schema.json`) refletant la structure exportee pour usage cross-langage.

2. Services et export

   * Introduire `backend/app/services/dashboard.py` avec:
     - `build_dashboard_snapshot()` (compose les dataclasses depuis `sample_snapshot`).
     - `summarize_snapshot(snapshot)` (renvoie KPIs: missions par statut, charge par role, budget ecart, alertes).
     - `serialize_snapshot(snapshot)` (dict ascii pour JSON) conforme au schema.
   * Ajouter un script CLI PowerShell-first `scripts/export_dashboard_snapshot.py` (exploitable via `python -m scripts.export_dashboard_snapshot --out frontend/public/data/dashboard-snapshot.json`).
   * Mettre a jour `backend/tests/` pour couvrir `summarize_snapshot` et la validation schema via `jsonschema` (utiliser dependance locale si deja presente sinon stub interne).

3. Integration frontend Dashboard

   * Ajouter `frontend/src/app/api/dashboard-api.js` avec une fonction `loadDashboardSnapshot()` qui lit le JSON local (via `import snapshot from '../data/dashboard-snapshot.json' assert { type: 'json' };`).
   * Etendre `frontend/src/app/views/dashboard-view.js` pour consommer `loadDashboardSnapshot()` et produire:
     - Cartes KPI (missions totales, pourcentage confirmees, alertes ouvertes) via `createKpiCard`.
     - Badges roles charges (utilitaire `createRoleBadge`) pour chaque role metier.
     - Resume modules (projets, planning, materiel) via `createModuleSummary` avec liens navigation.
   * Ajouter `frontend/src/app/components/dashboard-layout.js` pour structurer l affichage (grille ascii, sections). Exporter les structures (objet) plutot que du DOM.

4. Tests

   * Backend: `backend/tests/test_dashboard_services.py` couvrant `build_dashboard_snapshot`, `summarize_snapshot` et `serialize_snapshot` avec verifications deterministes.
   * Frontend: `frontend/tests/dashboard-view.test.js` validant que `initializeDashboardView()` retourne les KPI, badges et resumes attendus a partir du snapshot JSON.
   * Mettre a jour `frontend/tests/app-routing.test.js` si des nouvelles routes/dashboard sections sont ajoutees.

5. Documentation et archives

   * Documenter le format snapshot dans `docs/backend/dashboard-snapshot.md` (schema, commandes export, politique version).
   * Enrichir `docs/frontend/design-system.md` (section Dashboard) avec la maniere d utiliser les helpers pour KPI/badges.
   * Mettre a jour `README.md` (section Frontend Orga) pour mentionner la commande d export snapshot et la consommation offline.
   * Archiver la session sous `.codex/sessions/step-05/` (notes + tests log backend et frontend).

Deliverables

* Docs: `docs/roadmap/step-05.md`, `docs/backend/dashboard-snapshot.md`, updates README/design-system.
* Backend: nouveaux modules `models/orga.py`, `data/sample_snapshot.py`, `services/dashboard.py`, script export.
* Frontend: API `dashboard-api.js`, composant `dashboard-layout.js`, mise a jour `dashboard-view.js`, JSON snapshot versionne sous `frontend/public/data/dashboard-snapshot.json`.
* Tests: `backend/tests/test_dashboard_services.py`, `frontend/tests/dashboard-view.test.js` + updates existantes si requis.
* Archives: `.codex/sessions/step-05/notes.md`, `.codex/sessions/step-05/tests.log`.

Acceptance Criteria

* `pytest` et `npm test` passent avec les nouveaux tests deterministes (aucun acces reseau).
* Le snapshot JSON respecte le schema et reste stable entre executions (`export_dashboard_snapshot.py` idempotent).
* La vue Dashboard retourne un objet structure avec KPI, badges roles, resumes modules utilisant les helpers design system.
* Documentation ASCII-only, oriente Windows/PowerShell, reference la commande d export et le workflow offline.

Commandes Locales Exemples

* Generer snapshot JSON:
  ```ps1
  python -m scripts.export_dashboard_snapshot --out frontend/public/data/dashboard-snapshot.json
  ```
* Tests backend:
  ```ps1
  pytest
  ```
* Tests frontend:
  ```ps1
  cd frontend
  npm test
  ```

Notes

* Referencer la PR: `Ref: docs/roadmap/step-05.md`.
* Conserver le snapshot JSON petit (<= 5 KB) et facile a relire en diff.

VALIDATE? yes/no
