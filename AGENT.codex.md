# AGENT Codex - Bootstrap Autonome v1

ROLE

* Executer les steps de la roadmap a partir de prompts utilisateur.
* Generer code, tests, docs, PR GitHub.
* Archiver toutes les actions (prompts, diffs, logs, rapports CI) dans ./.codex

CONTRAINTES

* ASCII-only, Windows-first (PowerShell 7+), monorepo.
* Conventional Commits. PR avec "Ref: docs/roadmap/step-XX.md".
* Jamais d ecriture hors du repo.

PROCESSUS STANDARD

1. Lire docs/specs et docs/roadmap pour le contexte.
2. Ingestion prompt -> creer docs/roadmap/step-XX.md.
3. Creer branche feat/roadmap/step-XX.
4. Implementer code+tests+docs minimaux.
5. Lancer CI locale (si disponible) puis PR GitHub.
6. Archiver sous ./.codex (logs, diffs, rapports).
7. Stopper avec bloc VALIDATE? yes/no.

SORTIES ATTENDUES PAR STEP

* Liste des fichiers modifies
* Resultats tests
* Lien PR
* Chemins d archives
* Bloc "VALIDATE? yes/no"
