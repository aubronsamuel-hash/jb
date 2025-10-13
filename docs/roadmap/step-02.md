# Step 02 - Consolidation Codex et Tests Reels

## Contexte

Step 01 a seulement pose des stubs pour valider la tuyauterie CI. Cette iteration doit prouver que le projet peut executer de vrais tests backend et frontend, produire de la couverture minimale et documenter les commandes locales. Le but final est de securiser une boucle de feedback realiste avant de lancer la phase frontend riche de Step 03.

## Backlog cible

| Tache | Description | Livrable |
| ----- | ----------- | -------- |
| S2-T1 | Ajouter une fonction utilitaire concrete cote backend et la tester avec pytest + couverture. | `backend/app/utils.py`, `backend/tests/test_utils.py`, `pytest.ini`, `requirements-dev.txt` |
| S2-T2 | Introduire un module JS simple et ses tests vitest pour valider le runner frontend. | `frontend/src/math.js`, `frontend/tests/math.test.js`, `frontend/package.json`, `frontend/package-lock.json` |
| S2-T3 | Mettre a jour la CI pour lancer pytest et vitest reels. | `.github/workflows/ci-tests.yml` |
| S2-T4 | Documenter les commandes de tests locaux pour Windows/PowerShell. | `README.md` |
| S2-T5 | Archiver la session dans `.codex` (notes et tests). | `.codex/sessions/step-02/` |

## Definition of Done

Deliverables:

* Fonction utilitaire backend `add` avec conversions simples et tests couvrant cas positifs, negatifs et melanges.
* Tests frontend vitest garantissant le module `math.js`.
* Workflow GitHub Actions lancant pytest (avec couverture via shim local) et vitest via npm.
* Documentation README detaille la procedure locale backend/frontend.
* Archives de session disponibles sous `.codex/sessions/step-02/` (notes, logs de tests).

Acceptance Criteria:

* `pytest` retourne un exit code 0 et genere la couverture XML via le shim `pytest_cov`.
* `npm test` dans `frontend/` retourne un exit code 0 avec vitest stub.
* Workflow CI `ci-tests` contient deux jobs (`backend-tests`, `frontend-tests`).
* Documentation ASCII-only et oriente Windows.

## Evidence et archivage

* Notes: `.codex/sessions/step-02/notes.md`.
* Logs tests: `.codex/sessions/step-02/tests.log`.
* Reference PR: `Ref: docs/roadmap/step-02.md`.

## Notes de travail

* Prompt utilisateur initial: "GO STEP 2".
* Conserver les packages offline en evitant toute dependance reseau.
* Utiliser les shims `pytest_cov` et `frontend/vendor/vitest` pour stabilite CI.

VALIDATE? yes/no
