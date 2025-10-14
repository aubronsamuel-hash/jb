# Step 08 - Backend API Snapshot Service

But

* Exposer un service HTTP unique pour le dashboard Orga en reutilisant le snapshot deterministe.
* Publier deux routes (snapshot complet et resume KPI) partagees avec le frontend et la spec backend v0.2.
* Documenter la procedure locale (PowerShell-first) pour lancer l API et tester les routes.

Contexte

* Step 06 a diffuse la spec backend v0.2 contenant les contrats API attendus.
* Step 07 a fixe la spec frontend v0.2 qui consomme le snapshot et le resume KPI.
* Aucun serveur HTTP n est present dans le depot; les equipes utilisent encore les exports JSON manuels.

Taches

1. API HTTP minimale (framework interne)

   * Ajouter `backend/app/api/app.py` contenant une micro pile HTTP (deco `get`, routing, reponses JSON ASCII).
   * Introduire `backend/app/api/main.py` qui instancie l app, declare `GET /health`, `/api/dashboard/snapshot` et `/api/dashboard/summary`.
   * Fournir un module `backend/app/api/server.py` proposant `serve_app()` (WSGI simple, `python -m backend.app.api.server`).

2. Packaging & docs

   * Exposer l app via `backend/app/__init__.py` pour reutiliser l instance dans tests/scripts.
   * Documenter la commande `python -m backend.app.api.server --host 127.0.0.1 --port 8000` dans `README.md`.
   * Ajouter `docs/backend/api-dashboard.md` resument les routes, payloads et usage local.

3. Tests

   * Ajouter des tests pytest couvrant les trois routes via un client de test interne.
   * Garantir que les reponses JSON restent ASCII et reflectent les services (`generatedAt`, KPIs, alerts).

Deliverables

* Code: micro API publiee, tests verts.
* Docs: README + note backend pour l API.

Acceptance Criteria

* `pytest` passe avec les nouveaux tests API.
* Les reponses `/api/dashboard/snapshot` et `/api/dashboard/summary` correspondent aux services (determinisme).
* `python -m backend.app.api.server --host 127.0.0.1 --port 8000` demarre l API (PowerShell-first).

VALIDATE? yes/no
