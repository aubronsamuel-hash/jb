# Spec Visuelle - Orga (Version Universelle)

Source: brief "Specification visuelle - Application ORGA" fourni par l utilisateur.

============================================================
1) Vision Generale
============================================================
Coulisses Crew vise a centraliser la planification, la coordination et la logistique pour tous les metiers du spectacle vivant, de l evenementiel, du cinema et de l audiovisuel. La plateforme cible producteurs, freelances, collectifs, prestataires, ecoles et lieux culturels avec une experience collaborative fluide.

Objectif principal: reunir planning, ressources humaines, materiel, communication et documents dans un espace visuel partage.

============================================================
2) Tableau de Bord (Accueil)
============================================================
Vue adaptee au profil (technicien, manager, artiste, RH, administrateur). Elements clefs:
- Statut du jour (missions, lieux, horaires, notifications).
- Planning individuel et collectif.
- Indicateurs: heures travaillees, budget, disponibilite des equipes.
- Raccourcis: creer projet, mission, note, export feuille de route.

============================================================
3) Module Projets
============================================================
- Champs: nom, type, lieu, dates, responsable, statut, description libre.
- Planning global (timeline) et budget prevu/reel/variance.
- Ressources rattachees: personnes, materiel, lieux.
- Documents: PDF, devis, plans, fiches techniques.
- Discussion interne (chat) et historique des versions.

============================================================
4) Module Planning
============================================================
- Vue interactive collaborative (Jour/Semaine/Mois/Projet/Multi-sites).
- Drag & drop pour assigner techniciens, artistes, ressources.
- Filtres par role, lieu, projet, client, equipe.
- Export PDF / ICS / CSV.
- Alertes chevauchement et surcharge horaire.
- Synchronisation Google / Outlook / iCal.

============================================================
5) Module Ressources Humaines
============================================================
- Fiches individuelles: identite, photo, contact, role, competences.
- Documents legaux: contrat, CNI, RIB, certificats.
- Disponibilites et preferences horaires.
- Historique projets et missions.
- Statistiques: heures, cachets, presences.

============================================================
6) Module Materiel et Logistique
============================================================
- Inventaire complet (son, lumiere, video, plateau, costumes, vehicules, mobilier, informatique).
- Fiches materiel: type, quantite, etat, localisation.
- Affectation par projet ou mission.
- Alertes maintenance, pret, retour.
- Historique d utilisation.
- Suivi terrain via QR Code ou NFC.

============================================================
7) Feuille de Route
============================================================
Contenu attendu:
- Titre, logo, lieu, date, horaire d appel.
- Liste du personnel et coordonnees.
- Planning detaille horaire par service.
- Notes logistiques: repas, parking, securite, hebergement.
- Codes couleur par service.
- Export PDF A4 (horizontal/vertical).

============================================================
8) Communication et Notifications
============================================================
- Notifications push internes.
- Emails (Mailgun) pour feuilles de route, plannings, convocations.
- Bots Telegram / WhatsApp pour alertes directes.
- Historique et archivage des messages.

============================================================
9) Design et Charte Graphique
============================================================
- Theme clair par defaut, option sombre.
- Couleurs metiers: Jaune (Lumiere), Bleu (Son), Vert (Video), Gris (Plateau), Rose (HMC), Orange (Admin).
- UI fluide responsive (Tailwind + Framer Motion), inspirations Notion / Skello / Asana / Google Agenda.

============================================================
10) API, Securite, Architecture (Rappel)
============================================================
- Backend: FastAPI + PostgreSQL + Redis.
- Frontend: React + Vite + Tailwind + React Query.
- CI/CD: GitHub Actions (tests, lint, coverage).
- Auth: JWT + OAuth2 (Google / Microsoft / Apple).
- Sauvegarde: automatique, journaliere, chiffree.

============================================================
11) Roadmap Fonctionnelle
============================================================
| Version | Objectif | Modules |
| ------- | -------- | ------- |
| v1.0    | Dashboard, Planning, Feuille de route | Base fonctionnelle |
| v1.1    | RH + Documents + Notifications | Telegram + PDF |
| v1.2    | Materiel + Inventaire | QR Scan + Export |
| v2.0    | Mobile / Offline | PWA |
| v3.0    | IA Codex | Auto-planning / Alertes |
| v4.0    | Finances + Analytics | KPI / Graphiques |

============================================================
12) Extensions Futures
============================================================
- Formations et habilitations (CACES, securite, etc.).
- Facturation et paie automatisee.
- Tickets materiel et maintenance.
- CRM (clients, prestataires, lieux).
- Securite / badges / acces evenement.

============================================================
13) Resume Global
============================================================
Orga doit devenir une plateforme universelle pour organiser, planifier et gerer toutes les dimensions du spectacle et de l evenementiel, unifiant communication, logistique et equipes dans un espace visuel professionnel.
