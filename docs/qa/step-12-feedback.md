# Step 12 - QA Feedback Matrix

| Flux | Ticket | Gravite | Description QA | Resolution / Owner |
| ---- | ------ | ------- | -------------- | ------------------ |
| Login | QA-101 | Majeur | Message d erreur generique lors de JWT expire, absence de toast cible. | Frontend: `ApiClient.normalizeError` fournit un message conflict/validation ASCII et `ApiClientError.toToastMessage()` pour l annonce toasts (FE Squad). |
| Planning | QA-134 | Critique | Pagination par curseur impossible sur `/planning/assignments`, tests manual PowerShell KO. | Backend: nouvel endpoint `GET /api/planning/assignments` avec curseurs ASCII et limites controlees (`AssignmentPaginationError`) + tests pytest (BE Squad). |
| Assignation | QA-137 | Critique | Retour 200 sur curseur invalide, React Query boucle infinie. | Backend: `HttpError.not_found` renvoie 404 + code `cursor_not_found`, React Query consomme le code via `ApiClient.normalizeError` (BE/FE). |
| Assignation | QA-139 | Majeur | Accessibilite planning: NVDA n annonce pas le statut. | Frontend: helper `computeAssignmentAccessibilityHints` construit message ASCII pour aria-live (FE Squad). |
| Paie | QA-090 | Mineur | Evidence export paie non partagee. | Documentation: checklist release reference l export ASCII et stockage `.codex/sessions/step-12/` (QA Coord.). |

## Evidence

* Tests `pytest` et `npm test` executes sous PowerShell-equivalent (voir `.codex/sessions/step-12/tests.log`).
* Payload de pagination verifie via `backend/tests/test_api_planning.py`.
* Toasts d erreur verifies via `frontend/tests/api-client.test.js`.

## Suivi

* Restant: QA smoke DnD Windows programmee Step 13.
* Monitoring: logs ASCII a activer sur serveur auth (suivi SRE).
