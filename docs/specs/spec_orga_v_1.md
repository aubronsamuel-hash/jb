# SPEC - Orga (Coulisses Crew) v1.0

Ref: docs/specs/spec-fonctionnelle-v1.0.md
Owner: Sam (validator unique). Toute etape majeure requiert VALIDATE: yes par Sam.
ASCII only. Windows-first (PowerShell 7+). Monorepo.

============================================================
1) VISION
============================================================
Orga est un SaaS pour organiser spectacles et equipes techniques: projets, missions, planning, intermittents, paie, feuilles de route, materiel, budgets, exports, notifications. Cible: directeurs techniques, regisseurs, prod.

KPIs clefs: temps gagne sur planif (>50%), erreurs de planning (<1%), respect budget (+/-3%), delai de diffusion docs (<5 min).

============================================================
2) PERSONAS
============================================================
- Sam (DT / Regisseur General): cree projets, plans, budgets, equipes, feuilles de route, communique fournisseurs.
- Chargé de production: valide budgets, suit couts, paie, factures.
- Regie lumiere/son/plateau: recoit missions, horaires, feuilles de route, declare heures.
- Artistes: consultent planning et notes (lecture seule).
- Fournisseurs (ex: Dushow): recoivent demandes materiel, bons de commande.

============================================================
3) PORTEE FONCTIONNELLE (MODULES)
============================================================
3.1 Projets
- Creer/editer projet: titre, lieu, adresse, contact, periode, statut.
- Rattacher missions, budgets, fichiers, materiel, equipes.
- Templates de projet (pre-remplissage plan standard theatre X).

3.2 Lieux / Salles
- Base de lieux: scene, perches, FOH, puissance, restrictions, plans PDF.
- Contacts tech, livraisons, acces, consignes securite.

3.3 Missions
- Taches assignables avec role, personne, date/heure debut-fin, lieu, statut (draft, propose, confirme, realise, annule).
- Repetition; conflits; remplacements; checklists.
- Pieces jointes (PDF, images), notes internes.

3.4 Planning / Calendrier
- Vues: Jour / Semaine / Mois / Timeline (Gantt simplifie).
- Drag and drop, multi-ressource (par personne, par role, par lieu).
- Export ICS par personne et par projet; PDF planning journee A4 paysage.
- Detection conflits (chevauchement personne/role/lieu).

3.5 Equipes / Intermittents
- Fiches personnes: roles, competences, tarifs, disponibilites, docs (RIB, carte pro).
- Gestion remplacements; pool par role (ex: poursuite, HMC, etc.).
- Avatars/photos (stockees localement ou objet storage).

3.6 Disponibilites & Demandes
- Sondages de dispo (email/Telegram) et confirmations.
- Vue agregat des dispos par jour/mission.

3.7 Feuilles de route / Day-sheets
- Generateur de feuilles de route A4 paysage compactes: horaires, qui fait quoi, photos simulees, contacts, tech riders.
- Versions pour distribution equipe (confidentialite niveaux).
- Templates (ex: Josefine Baker) avec placeholders.

3.8 Materiel & Logistique
- Catalogue: projecteurs, consoles, truss, perches, cables, gélatines.
- Bons de demande/location, comparateur fournisseurs, etat stock.
- Planning de materiel par projet; listes de cablage; gélatines.

3.9 Paie / Heures / Invoices
- Saisie heures; validation; export CSV/Excel pour paie.
- Taux horaires/cachets; calcul couts par mission/projet.
- Generation de PDF recaps pour prod; suivi factures fournisseurs simples.

3.10 Budgets & Analytics
- Budget previsionnel par projet (lumiere/son/plateau/location/personnel).
- Reel vs prevu; ecarts; KPI; dashboard cout/heure/personne.

3.11 Notifications
- Email et Telegram (bot) pour convocations, changements planning, rappels.
- Regles: J-7, J-1, H-2.

3.12 Documents / Exports
- PDF: planning jour, feuille de route, bons materiel, recap heures.
- ICS: par personne/projet. CSV/Excel: heures, budget, materiel.

3.13 Permissions & Roles
- Roles: Admin, DT, Prod, Chef equipe, Tech, Lecture seule.
- Portee: par organisation et par projet. Journaux d’audit.

3.14 Archives & Historique
- Versions des docs; historique missions; audit trail (qui, quoi, quand).

3.15 Intégrations (phase 2+)
- Google Calendar (import), Drive, API fournisseurs (si dispo), SSO.

============================================================
4) CONTRAINTES NON FONCTIONNELLES
============================================================
- Disponibilite: 99.5% Phase 1.
- Performance: <200ms p95 pour endpoints courants; generation PDF <10s.
- Securite: JWT, RBAC, chiffrement at-rest (DB) et en transit (TLS).
- RGPD: droit a l’oubli, export donnees, consentement notifications.
- Logs/metrics: traces, erreurs, temps reponse; alertes basiques.

============================================================
5) ARCHITECTURE HAUTE NIVEAU
============================================================
Backend: FastAPI, Postgres, Redis (cache/tasks), Celery/RQ pour jobs async (PDF, emails, Telegram), Alembic migrations, Pydantic, SQLAlchemy. Schemas REST JSON (style JSON:API light).
Frontend: React + Vite + TS + Tailwind + shadcn/ui + React Query + Router.
Infra local: Docker Compose. En prod: images Docker; base Postgres managée (selon cible).
CI/CD: GitHub Actions (backend tests, frontend tests, guards, coverage, SAST).

============================================================
6) MODELE DE DONNEES (EXTRAIT)
============================================================
Organisation(id, name)
User(id, org_id, email, name, role, avatar_url)
Venue(id, org_id, name, address, tech_specs_json)
Project(id, org_id, name, venue_id, start, end, status, notes)
Person(id, org_id, name, roles[], rate, photo_url, docs)
Mission(id, project_id, venue_id, role, person_id?, start, end, status, checklist_json)
Availability(id, person_id, date, slot, status)
Equipment(id, org_id, name, type, specs, qty)
RentalOrder(id, project_id, supplier, items_json, status, cost_est, cost_real)
Timesheet(id, mission_id, person_id, hours, rate, approved)
BudgetLine(id, project_id, category, estimate, actual)
Notification(id, org_id, type, target, payload_json, sent_at)
AuditLog(id, org_id, user_id, entity, entity_id, action, ts)

Indices: par org, par projet, par personne/date.

============================================================
7) API (EXEMPLES D ENDPOINTS)
============================================================
GET /api/v1/projects?status=active
POST /api/v1/projects
GET /api/v1/projects/{id}
PATCH /api/v1/projects/{id}

GET /api/v1/missions?project_id=...&date=...
POST /api/v1/missions
PATCH /api/v1/missions/{id}
POST /api/v1/missions/{id}/assign { person_id }

GET /api/v1/planning?from=...&to=...&groupBy=person
GET /api/v1/people
POST /api/v1/people

POST /api/v1/exports/day-sheet.pdf?project_id=...&date=...
POST /api/v1/exports/planning.ics?person_id=...

POST /api/v1/notifications/test

============================================================
8) FRONTEND (PAGES & COMPOSANTS)
============================================================
- Auth (mock step initial): Login, Logout.
- Dashboard: KPIs, prochains evenements, alertes conflits.
- Projets: liste, creation, detail (onglets: planning, missions, equipe, materiel, budget, docs).
- Planning: vues Day/Week/Month/Timeline, drag-drop, filtres, export.
- Missions: table + drawer edition, statut, assignations.
- Equipes: fiches, pool par role, disponibilites.
- Materiel: catalogue, affectations, commandes.
- Budgets/Analytics: graphes, ecarts, rapport PDF/CSV.
- Notifications: regles, historique.
- Parametres: lieux, templates, roles, webhooks.

Composants UI clefs: Calendar, TimelineBar, MissionCard, PersonAvatar, RoleBadge, ConflictPill, ExportButtons, DrawerForm, DataTable, BudgetChart.

============================================================
9) WORKFLOWS CLEFS
============================================================
W1 Creation projet -> importer lieu -> ajouter equipe -> ajouter missions -> planifier -> envoyer convocations -> exporter feuille de route -> saisir heures -> exporter paie.
W2 Remplacement express -> marquer indispo -> suggerer rempla par role -> notifier.
W3 Demande materiel -> composer liste -> envoyer fournisseurs -> recevoir devis -> confirmer -> lier au budget.

============================================================
10) GENERATION DE DOCUMENTS
============================================================
- PDF A4 paysage (feuille de route, plan journee, bons materiel). Moteur: WeasyPrint/WKHTMLTOPDF ou HTML-to-PDF headless.
- ICS: par personne/projet; timezone Europe/Paris.
- CSV/Excel: heures, budgets, materiel.

============================================================
11) SECURITE & PERMISSIONS
============================================================
- Auth JWT; refresh token; roles (Admin, DT, Prod, Chef, Tech, RO).
- Scopes par projet; separation organisations; audit trail obligatoire.
- Rate limiting basique; CORS controle; validation Pydantic stricte.

============================================================
12) QUALITE, TESTS, CI/CD
============================================================
- Backend: pytest, coverage >= 85%; tests API; tests migrations.
- Frontend: vitest + testing-library; e2e Playwright basique.
- Guards: docs_guard, roadmap_guard, commit_guard, agents_guard; GH_TOKEN set.
- Pipelines: install (npm ci / pip install -r), lint, typecheck, test, build, trivy, gitleaks.

============================================================
13) ENVIRONNEMENTS & DEVOPS
============================================================
- .env examples: backend/.env.example, frontend/.env.example.
- Docker Compose: postgres, redis, backend, frontend, worker, scheduler.
- Seeds demo (personas, lieu Bobino, gabarits Josefine Baker, roles standard).
- Backups DB; migrations Alembic; rollbacks scripts.

============================================================
14) SCRIPTS POWERSHELL (WINDOWS-FIRST)
============================================================
- tools/init_repo.ps1: clone deps, pre-commit hooks, check versions Node/Python.
- tools/dev_up.ps1: docker compose up, wait-for, print URLs.
- tools/run_tests.ps1: run backend and frontend tests, coverage gates.
- tools/gen_day_sheet.ps1: generate sample PDF pour projet demo.
- tools/export_ics.ps1: generate ICS pour personne demo.
- tools/smoke.ps1: health checks (API /healthz, PDF engine, Redis ping).

Tous ASCII-only; messages clairs; exit codes corrects.

============================================================
15) I18N & ACCESSIBILITE
============================================================
- FR par defaut, EN ensuite. Textes externalises.
- A11y: focus order, contrast, labels ARIA, clavier, tailles adaptatives.

============================================================
16) ROADMAP (10 PREMIERS STEPS)
============================================================
01 Backend bootstrap (FastAPI, DB, Alembic, base models, healthz).
02 CI Guards fixes + npm ci policy + pipeline base.
03 Frontend init (React/Vite/Tailwind, Query, Router) + lockfile OK.
04 Design System minimal (palette, tokens, shadcn/ui), Storybook opt.
05 Domain Projects/Venues API + tests + seeds demo (Bobino).
06 People/Teams API + dispo + assignations basiques.
07 Missions API + conflits + planning Day/Week + export ICS.
08 Day-sheet PDF v1 (A4 paysage compact) + templates Josefine Baker.
09 Materiel catalog + bons demandes + fournisseurs (mock) + budget lines.
10 Heures/Paie export CSV + Analytics v1 (couts vs budget).

Chaque step: docs/roadmap/step-XX.md avec objectifs, livrables, scripts, tests, DoD, VALIDATE par Sam.

============================================================
17) CRITERES D ACCEPTATION GLOBALS (DOD GLOBAL)
============================================================
- Monorepo buildable (docker compose) local et CI green.
- RBAC basique actif; audit logs ecrits.
- Exports PDF/ICS fonctionnels sur dataset demo.
- Planning Week drag-drop OK; conflits visibles.
- Niveaux de secrets .env geres; aucune fuite en repo.

============================================================
18) RISQUES & MITIGATIONS
============================================================
- Complexite planning/conflits: commencer simple, ajouter regles iteratives.
- Qualite PDF: set de templates test; fallback wkhtmltopdf si besoin.
- Verrous npm ci: figer Node LTS; valider lockfile a chaque PR.

============================================================
19) ANNEXES (CONVENTIONS)
============================================================
- Conventional Commits.
- Dossiers deterministes; pas d ecriture hors repo.
- Nommage roles: admin, dt, prod, chef, tech, ro.
- Timezone: Europe/Paris partout.
- Sam est l unique validateur: aucune etape n est considerée livree sans VALIDATE: yes.

