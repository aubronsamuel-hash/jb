# Step 01 - Bootstrap autonome Codex

## Contexte

But: Installer toute l infrastructure Codex pour ingestion de prompts -> steps -> CI -> PR -> archivage.

## Backlog cible

| Tache | Description | Livrable |
| ----- | ----------- | -------- |
| S1-T1 | Formaliser la procedure step pour l agent. | Documentation roadmap mise a jour. |
| S1-T2 | Verifier que les stubs backend/frontend et tests de fumee existent. | Inventaire dans .codex. |
| S1-T3 | Garantir la presence des workflows CI (tests, security, guards). | Revue et checklist. |
| S1-T4 | Mettre en place l archivage local des actions. | Dossier `.codex/sessions/step-01`. |

## Definition of Done

Deliverables:

* Arborescence de base + fichiers tools/scripts.
* Workflows CI (tests, security, guards).
* Stubs backend/frontend + tests pour CI verte.
* AGENT.codex.md rempli.
* Archive .codex de la session.

Acceptance Criteria:

* PR ouverte: "chore(codex): bootstrap autonome v1"
* CI verte: tests, guards, security.
* ASCII only valide.
* Bloc final VALIDATE? yes/no present dans sortie d execution.

## Notes de travail

* Prompt utilisateur: "GO STEP 1".
* Cette step initialise l execution autonome et journalise les decisions clefs.
* Voir `.codex/sessions/step-01/notes.md` pour les evidences et journaux detailles.
