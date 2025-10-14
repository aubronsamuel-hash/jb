# Step 12 - Release Checklist (QA / Prod Readiness)

## Automatisation

- [x] `pytest` (backend) sur PowerShell + Linux.
- [x] `npm test` (frontend) via vitest stub.
- [x] Export paie ASCII (`scripts.export_payroll_reports`) sauvegarde dans `.codex/sessions/step-12/artifacts/`.

## Scenarios Manuels

- [x] Login -> Dashboard: verification toast JWT expire (`ApiClientError.toToastMessage`).
- [x] Planning Drag & Drop: pagination curseur `/api/planning/assignments` testee avec `limit=2` et `cursor` absent.
- [x] Assignation rapide: 404 sur curseur invalide (evite boucles React Query) + annonce NVDA via `computeAssignmentAccessibilityHints`.

## Monitoring & Alerting

- [x] Journalisation ASCII des erreurs HTTP (codes 404/409/422) expose via `HttpError`.
- [ ] Telemetrie auth/refresh vers canal SRE (en cours de cadrage Step 13).

## Livrables

- [x] Matrice QA (`docs/qa/step-12-feedback.md`).
- [x] Specs mises a jour (`docs/specs/api_front-backend-schema-v1.md`, `docs/frontend/coulisses-crew-frontend.md`).
- [x] Notes roadmap (`docs/roadmap/step-12.md`).
- [x] Logs tests & export dans `.codex/sessions/step-12/`.
