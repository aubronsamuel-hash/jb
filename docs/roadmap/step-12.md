# Step 12 - QA Feedback Integration & Release Prep

But

* Consolider les retours QA sur les parcours login, planning et assignation issus de la revue croisee frontend/backend.
* Prioriser et adresser les correctifs critiques (API, frontend, donnees) pour garantir un sprint missions sans regression.
* Formaliser la checklist de validation (tests, monitoring, alerting) et les livrables documentaires avant ouverture QA et prod.

Contexte

* La spec API v1 est validee (Step 11) mais doit etre confrontee aux scenarios reels remontes par QA et support interne.
* Les flux sensibles (auth JWT court, planning DnD, assignation rapide, paie) doivent rester compatibles Windows/PowerShell et ASCII-only.
* Les squads attendent une consolidation des evidences (tests, captures, logs) et un plan de mitigation avant go/no-go release.

Taches

1. Collecte & analyse QA

   * Centraliser les retours QA (tickets, captures, logs) et dresser une matrice gravite/impact/owner.
   * Rejouer les scenarios critiques sur env local (PowerShell) en suivant les scripts QA, noter toute deviation vs spec v1.
   * Identifier les manques de telemetry (logs, traces) et preparer les ajustements necessaires.

2. Correctifs backend & tests

   * Ajuster les endpoints FastAPI concernes (auth refresh, planning, assignation, paie) et completer les tests pytest ciblant les edge cases signales.
   * Valider la pagination par curseur, les codes erreurs et l idempotence sur les flux de creation/assignation.
   * Documenter dans la spec les changements de payloads et partager avec QA une note de version ASCII.

3. Ajustements frontend & UX

   * Mettre a jour les queries React Query/Zod schemas et les handlers d erreurs pour couvrir les cas QA (timeouts, 409, 422).
   * Renforcer les affordances UX: etats de chargement/panne, focus visibles apres DnD, toasts ASCII, shortcuts clavier Windows.
   * Tester sous Windows (navigateur Chromium + PowerShell) les sequences login -> dashboard, planning DnD, assignation rapide.

4. Validation croisee & documentation

   * Synchroniser les squads sur la resolution des tickets, partager les evidences (captures ASCII, logs) via `.codex/sessions/step-12/`.
   * Mettre a jour `docs/specs/api_front-backend-schema-v1.md`, `docs/frontend/coulisses-crew-frontend.md` et la roadmap avec les ajustements QA.
   * Formaliser une checklist release (tests automatises, smoke manual QA, monitoring) et definir les criteres go/no-go.

Deliverables

* Matrice de feedback QA et plan d action priorise.
* Correctifs backend/frontend merges avec tests mis a jour et documentation synchronisee.
* Checklist release + evidences archivees dans `.codex/sessions/step-12/`.

## Execution Step 12

### Collecte QA

* Matrice consolidee dans `docs/qa/step-12-feedback.md` (tickets QA-101, QA-134, QA-137, QA-139, QA-090).
* Evidence tests + exports deposee dans `.codex/sessions/step-12/`.

### Correctifs Backend & Tests

* Micro API supporte requetes avec query string + `HttpError` (codes 404/409/422 ASCII).
* Nouveau service `get_assignment_feed()` (pagination curseur, limites 1..50, resume statut).
* Endpoint `GET /api/planning/assignments` + tests `test_api_planning.py` / `test_planning_services.py`.

### Ajustements Frontend & UX

* `ApiClient` gere erreurs 409/422 via `ApiClientError` et toasts ASCII.
* Helpers planning (`sanitizeAssignmentFeed`, `computeAssignmentAccessibilityHints`) garantissent accessibilite NVDA.
* Tests Vitest couvrent la normalisation et les annonces aria-live.

### Documentation & Release Prep

* Specs back/front maj (pagination assignments, toasts, accessibilite).
* Checklist release dans `docs/qa/step-12-release-checklist.md`.
* Notes QA et evidences referencees pour go/no-go.

Acceptance Criteria

* Tous les tickets QA critiques/majeurs sont resolus ou disposent d un plan de mitigation documente.
* Les suites de tests (pytest backend, vitest frontend) passent sur Windows/PowerShell et couvrent les cas QA remontes.
* La checklist release est validee par backend, frontend et QA; les preuves sont accessibles et ASCII-only.

VALIDATE? yes
