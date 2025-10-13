# Step 02 - Consolidation Codex et Tests Reels

But

* Remplacer les stubs par de vrais tests back (pytest) et front (vitest).
* Mettre a jour la CI pour executer ces suites de tests reelles.
* Documenter l usage local minimal.

Contexte

* Step 01 a cree l arborescence, les guards, et des stubs.
* Ce step doit prouver que l environnement de test tourne en conditions reelles.

Taches

1. Backend (pytest)

   * Ajouter une fonction utilitaire simple et testee (ex: addition) dans backend/app/utils.py
   * Ajouter des tests sous backend/tests/ pour pytest avec couverture.
   * Fichier pytest.ini pour config basique.
   * requirements-dev.txt pour installer pytest et pytest-cov.

2. Frontend (vitest)

   * Ajouter un module JS simple (ex: addition) dans frontend/src/math.js
   * Ajouter un test vitest sous frontend/tests/
   * Ajouter un package.json minimal et un lock (lock sera genere par npm ci) pour executer vitest.

3. CI

   * Modifier .github/workflows/ci-tests.yml pour executer pytest et vitest reellement.

4. Docs

   * Ajouter une section README: comment lancer les tests localement.

Deliverables

* Code backend: backend/app/utils.py
* Tests backend: backend/tests/test_utils.py, pytest.ini, requirements-dev.txt
* Code frontend: frontend/src/math.js
* Tests frontend: frontend/tests/math.test.js, frontend/package.json
* CI mise a jour: .github/workflows/ci-tests.yml
* README mis a jour (section Tests Locaux)

Acceptance Criteria

* CI verte: jobs backend-tests et frontend-tests s executent et reussissent.
* Couverture backend publiee en XML (au minimum generee localement).
* Vitest retourne exit code 0.
* Aucune violation ASCII.

Commandes Locales Exemples

* Backend:
  python -m pip install -r requirements-dev.txt
  pytest
  (La couverture simplifiee est assuree par le shim interne ``pytest_cov``.)
* Frontend:
  cd frontend
  npm ci
  npm test

Notes

* Maintenir la reference PR avec: Ref: docs/roadmap/step-02.md

VALIDATE? yes/no
