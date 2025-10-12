# Spec Fonctionnelle v0.1 (Bootstrap)

Objectif: permettre a Codex d ingerer un prompt utilisateur et de produire un step, du code stub, des tests stubs, des workflows CI et une PR verte.

Criteres d acceptation (minimaux):

* Une PR s ouvre avec Ref vers docs/roadmap/step-01.md
* Les workflows CI s executent et ne plantent pas.
* Les scripts PowerShell existent et s executent sans erreurs (dry-run possible).
* Les guards existent (ascii, roadmap, commit) et reussissent sur l etat initial.
