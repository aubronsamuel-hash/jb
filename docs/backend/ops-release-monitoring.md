# Ops - Release Monitoring

Ce guide deploiement Step 13 decrit comment collecter en ASCII la sante de l API avant go/no-go.

## Endpoint `/api/ops/status`

* Fournit `release.status` (`ok` attendu) et `release.version`.
* Resume dashboard (`missions`, `projects`, `alerts`) et planning (`pageInfo`, `summary`, `sample`).
* Payload garantit des identifiants ASCII et des ratios arrondis.

## Script `monitor_release.py`

```ps1
python -m scripts.monitor_release --limit 3
```

Sortie exemple (ASCII):

```
Release version: 0.2.0
Status: ok
Generated at: 2024-05-06T08:00:00Z
Missions total: 4 (confirmed 25.0%)
Alerts: Conflit planning: mission Soundcheck groupe A overlap avec repetition video, Budget depasse: Festival Aurora +2800 EUR, Disponibilite critique: role video sous 60%
Sample assignments: asg-aurora-light-1, asg-aurora-sound-1, asg-riverside-video-1
```

Mode JSON pour journalisation:

```ps1
python -m scripts.monitor_release --limit 2 --format json > .codex/sessions/step-13/ops-status.json
```

## Archivage `.codex`

* Deposer la sortie ASCII ou JSON dans `.codex/sessions/step-13/`.
* Nommer les fichiers `ops-status.txt` ou `ops-status.json` selon le format.
