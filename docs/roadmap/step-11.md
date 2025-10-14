# Step 11 - Coulisses Crew API Contract v1

But

* Publier la spec API front <-> backend v1 couvrant authentification, missions, planning, paie et inventaire.
* Synchroniser les expectations frontend (queries React, Zod schemas) avec les reponses FastAPI.
* Documenter les workflows clefs (login, planning, assignations) et les guardrails de securite/perf.

Contexte

* Les squads frontend et backend doivent aligner leurs contrats avant les sprints features.
* La spec v0.x couvrait surtout le backend; cette iteration introduit les flux complets cote client.
* Les contraintes Windows-first, ASCII-only et JWT short-lived imposent des intercepteurs robustes.

Taches

1. Documentation API

   * Rediger `docs/specs/api_front-backend-schema-v1.md` avec endpoints, payloads, codes erreurs et exemples ASCII.
   * Preciser pagination par curseur, idempotence, headers communs et RBAC.
   * Ajouter sections annexes (OpenAPI extrait, mapping roles, statuts metiers).

2. Guidelines frontend

   * Lister les sequences reseau critiques (login->dashboard, DnD planning, assignation rapide).
   * Noter les clefs React Query, conventions Zod, refresh token retry unique.
   * Documenter le flow d upload (presign -> PUT S3 -> PATCH ressource).

3. Qualite et archivage

   * Verifier coherence ASCII et compatibilite Windows/PowerShell pour les commandes.
   * Archiver notes et logs sous `.codex/sessions/step-11/` (prompt, diff, tests).
   * Mettre a jour la roadmap avec ce step et preparer la prochaine validation.

Deliverables

* Spec API v1 accessible dans `docs/specs`.
* Roadmap et archives `.codex` mises a jour.
* Instructions integration frontend consolidees.

Acceptance Criteria

* Les endpoints critiques (auth, missions, planning, paie, inventaire) sont decrits avec request/response JSON clairs.
* Les conventions de pagination, tri, filtres, erreurs et idempotence sont explicites.
* La checklist integration front couvre auth refresh, headers, queries, uploader.

VALIDATE? yes/no
