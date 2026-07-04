# Plan d'Implémentation — Application de Gestion de Présence des Étudiants

---

## Table des Matières

1. [Vue d'Ensemble du Projet](#1-vue-densemble-du-projet)
2. [Architecture Technique](#2-architecture-technique)
3. [MCD — Modèle Conceptuel de Données](#3-mcd--modèle-conceptuel-de-données)
4. [MLD — Modèle Logique de Données](#4-mld--modèle-logique-de-données)
5. [Diagramme de Classes UML](#5-diagramme-de-classes-uml)
6. [Diagrammes de Cas d'Utilisation](#6-diagrammes-de-cas-dutilisation)
7. [Diagrammes de Séquence](#7-diagrammes-de-séquence)
8. [Diagramme d'État — Présence](#8-diagramme-détat--présence)
9. [Diagramme de Composants](#9-diagramme-de-composants)
10. [Structure du Projet Django](#10-structure-du-projet-django)
11. [Modèles Django (ORM)](#11-modèles-django-orm)
12. [Plan des URLs & Vues](#12-plan-des-urls--vues)
13. [Phases d'Implémentation](#13-phases-dimplémentation)
14. [Maquettes d'Interface](#14-maquettes-dinterface)

---

## 1. Vue d'Ensemble du Projet

| Élément            | Détail                                      |
|--------------------|---------------------------------------------|
| **Nom**            | GesPresence — Gestion de Présence Étudiants |
| **Stack Backend**  | Django 4.x (Python)                         |
| **Stack Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5        |
| **Base de données**| MySQL 8.x                                   |
| **Style visuel**   | Inspiré du portail OFPPT (myway.ac.ma)      |

### Types d'Utilisateurs & Rôles

| Rôle              | Permissions principales                                                    |
|-------------------|----------------------------------------------------------------------------|
| **Administrateur**| Gestion complète : utilisateurs, filières, groupes, cours, rapports       |
| **Enseignant**    | Marquer la présence, consulter ses cours et sessions                       |
| **Étudiant**      | Consulter son propre historique de présence                                |
| **Parent**        | Consulter la présence de son/ses enfant(s), recevoir des notifications     |

---

## 2. Architecture Technique

```mermaid
graph TB
    subgraph Client["Navigateur Web"]
        HTML["HTML / CSS / JS"]
        BS["Bootstrap 5"]
    end

    subgraph Django["Serveur Django"]
        URLS["urls.py — Routeur"]
        VIEWS["Views — Logique Métier"]
        FORMS["Forms — Validation"]
        MODELS["Models ORM"]
        ADMIN["Django Admin"]
        AUTH["Django Auth"]
        TEMPLATES["Templates Jinja2"]
    end

    subgraph DB["Base de Données"]
        MySQL["MySQL 8"]
    end

    Client -->|HTTP Request| URLS
    URLS --> VIEWS
    VIEWS --> FORMS
    VIEWS --> MODELS
    VIEWS --> TEMPLATES
    MODELS -->|SQL| MySQL
    TEMPLATES -->|HTTP Response| Client
    AUTH --> VIEWS
    ADMIN --> MODELS
```

### Pattern MVT (Model–View–Template)

```mermaid
flowchart LR
    REQ([Requête HTTP]) --> URL[urls.py]
    URL --> VIEW[View]
    VIEW <--> MODEL[Model\nORM Django]
    MODEL <--> MYSQL[(MySQL)]
    VIEW --> TEMPLATE[Template HTML]
    TEMPLATE --> RESP([Réponse HTTP])
```

---

## 3. MCD — Modèle Conceptuel de Données

> Le MCD représente les entités métier et leurs associations sans se préoccuper de l'implémentation physique.

```mermaid
erDiagram
    UTILISATEUR {
        int id PK
        string nom
        string prenom
        string email
        string password_hash
        enum role
        string telephone
        datetime created_at
    }

    ETUDIANT {
        int id PK
        string matricule
        date date_naissance
        string photo
    }

    ENSEIGNANT {
        int id PK
        string specialite
        string grade
        string cin
    }

    ADMINISTRATEUR {
        int id PK
        string departement
    }

    PARENT {
        int id PK
        string adresse
        string telephone_urgence
    }

    FILIERE {
        int id PK
        string nom
        string code
        string description
        int duree_annees
    }

    GROUPE {
        int id PK
        string nom
        int annee_scolaire
        int effectif_max
    }

    COURS {
        int id PK
        string nom
        string code_cours
        string description
        int volume_horaire
    }

    SESSION_COURS {
        int id PK
        date date_session
        time heure_debut
        time heure_fin
        string salle
        string statut
    }

    PRESENCE {
        int id PK
        enum statut
        string justification
        datetime created_at
        bool notif_parent_envoyee
    }

    NOTIFICATION {
        int id PK
        string message
        enum type
        bool lu
        datetime envoyee_le
    }

    UTILISATEUR ||--o| ETUDIANT : "est"
    UTILISATEUR ||--o| ENSEIGNANT : "est"
    UTILISATEUR ||--o| ADMINISTRATEUR : "est"
    UTILISATEUR ||--o| PARENT : "est"

    FILIERE ||--|{ GROUPE : "contient"
    GROUPE ||--|{ ETUDIANT : "regroupe"

    ENSEIGNANT ||--|{ COURS : "enseigne"
    COURS }|--|{ GROUPE : "dispensé à"

    COURS ||--|{ SESSION_COURS : "génère"
    SESSION_COURS ||--|{ PRESENCE : "enregistre"
    ETUDIANT ||--|{ PRESENCE : "a"

    PARENT }|--|{ ETUDIANT : "est tuteur de"
    PARENT ||--|{ NOTIFICATION : "reçoit"
```

---

## 4. MLD — Modèle Logique de Données

> Le MLD traduit le MCD en tables relationnelles avec clés primaires et étrangères.

```mermaid
erDiagram
    utilisateur {
        INT id PK
        VARCHAR nom
        VARCHAR prenom
        VARCHAR email "UNIQUE"
        VARCHAR password_hash
        ENUM role "admin,enseignant,etudiant,parent"
        VARCHAR telephone
        DATETIME created_at
        BOOL is_active
    }

    etudiant {
        INT id PK
        INT user_id FK
        VARCHAR matricule "UNIQUE"
        DATE date_naissance
        VARCHAR photo
        INT groupe_id FK
    }

    enseignant {
        INT id PK
        INT user_id FK
        VARCHAR specialite
        VARCHAR grade
        VARCHAR cin "UNIQUE"
    }

    administrateur {
        INT id PK
        INT user_id FK
        VARCHAR departement
    }

    parent {
        INT id PK
        INT user_id FK
        VARCHAR adresse
        VARCHAR telephone_urgence
    }

    parent_etudiant {
        INT parent_id FK
        INT etudiant_id FK
    }

    filiere {
        INT id PK
        VARCHAR nom
        VARCHAR code "UNIQUE"
        TEXT description
        INT duree_annees
    }

    groupe {
        INT id PK
        VARCHAR nom
        INT annee_scolaire
        INT effectif_max
        INT filiere_id FK
    }

    cours {
        INT id PK
        VARCHAR nom
        VARCHAR code_cours "UNIQUE"
        TEXT description
        INT volume_horaire
        INT enseignant_id FK
    }

    cours_groupe {
        INT cours_id FK
        INT groupe_id FK
    }

    session_cours {
        INT id PK
        DATE date_session
        TIME heure_debut
        TIME heure_fin
        VARCHAR salle
        ENUM statut "planifiee,terminee,annulee"
        INT cours_id FK
        INT groupe_id FK
    }

    presence {
        INT id PK
        ENUM statut "present,absent,retard,justifie"
        TEXT justification
        DATETIME created_at
        BOOL notif_parent_envoyee
        INT etudiant_id FK
        INT session_id FK
    }

    notification {
        INT id PK
        TEXT message
        ENUM type "absence,retard,rapport"
        BOOL lu
        DATETIME envoyee_le
        INT parent_id FK
    }

    utilisateur ||--o| etudiant : "user_id"
    utilisateur ||--o| enseignant : "user_id"
    utilisateur ||--o| administrateur : "user_id"
    utilisateur ||--o| parent : "user_id"

    filiere ||--|{ groupe : "filiere_id"
    groupe ||--|{ etudiant : "groupe_id"

    enseignant ||--|{ cours : "enseignant_id"
    cours ||--|{ cours_groupe : "cours_id"
    groupe ||--|{ cours_groupe : "groupe_id"

    cours ||--|{ session_cours : "cours_id"
    groupe ||--|{ session_cours : "groupe_id"

    session_cours ||--|{ presence : "session_id"
    etudiant ||--|{ presence : "etudiant_id"

    parent ||--|{ parent_etudiant : "parent_id"
    etudiant ||--|{ parent_etudiant : "etudiant_id"
    parent ||--|{ notification : "parent_id"
```

### Schéma SQL Résumé

```sql
-- Tables principales
utilisateur       (id, nom, prenom, email UNIQUE, password_hash, role, telephone, created_at, is_active)
etudiant          (id, user_id FK, matricule UNIQUE, date_naissance, photo, groupe_id FK)
enseignant        (id, user_id FK, specialite, grade, cin UNIQUE)
administrateur    (id, user_id FK, departement)
parent            (id, user_id FK, adresse, telephone_urgence)
parent_etudiant   (parent_id FK, etudiant_id FK)  -- table de jonction

filiere           (id, nom, code UNIQUE, description, duree_annees)
groupe            (id, nom, annee_scolaire, effectif_max, filiere_id FK)

cours             (id, nom, code_cours UNIQUE, description, volume_horaire, enseignant_id FK)
cours_groupe      (cours_id FK, groupe_id FK)      -- table de jonction

session_cours     (id, date_session, heure_debut, heure_fin, salle, statut, cours_id FK, groupe_id FK)
presence          (id, statut, justification, created_at, notif_parent_envoyee, etudiant_id FK, session_id FK)
notification      (id, message, type, lu, envoyee_le, parent_id FK)
```

---

## 5. Diagramme de Classes UML

```mermaid
classDiagram
    class Utilisateur {
        +int id
        +str nom
        +str prenom
        +str email
        +str role
        +str telephone
        +bool is_active
        +login()
        +logout()
        +modifier_profil()
    }

    class Etudiant {
        +str matricule
        +date date_naissance
        +str photo
        +Groupe groupe
        +get_historique_presence()
        +get_taux_presence()
        +get_absences()
    }

    class Enseignant {
        +str specialite
        +str grade
        +str cin
        +list cours
        +marquer_presence(session, etudiants)
        +get_mes_sessions()
        +generer_rapport_cours()
    }

    class Administrateur {
        +str departement
        +gerer_utilisateurs()
        +gerer_filieres()
        +gerer_groupes()
        +generer_rapport_global()
        +voir_statistiques()
    }

    class Parent {
        +str adresse
        +str telephone_urgence
        +list enfants
        +voir_presence_enfant(etudiant)
        +get_notifications()
    }

    class Filiere {
        +int id
        +str nom
        +str code
        +int duree_annees
        +list groupes
        +get_statistiques()
    }

    class Groupe {
        +int id
        +str nom
        +int annee_scolaire
        +int effectif_max
        +Filiere filiere
        +list etudiants
        +list cours
        +get_taux_presence_groupe()
    }

    class Cours {
        +int id
        +str nom
        +str code_cours
        +int volume_horaire
        +Enseignant enseignant
        +list groupes
        +list sessions
        +creer_session(date, heure_debut, heure_fin, salle)
    }

    class SessionCours {
        +int id
        +date date_session
        +time heure_debut
        +time heure_fin
        +str salle
        +str statut
        +Cours cours
        +Groupe groupe
        +list presences
        +demarrer()
        +terminer()
        +get_taux_presence()
    }

    class Presence {
        +int id
        +str statut
        +str justification
        +datetime created_at
        +bool notif_parent_envoyee
        +Etudiant etudiant
        +SessionCours session
        +justifier()
        +envoyer_notification_parent()
    }

    class Notification {
        +int id
        +str message
        +str type
        +bool lu
        +datetime envoyee_le
        +Parent parent
        +marquer_lu()
    }

    Utilisateur <|-- Etudiant
    Utilisateur <|-- Enseignant
    Utilisateur <|-- Administrateur
    Utilisateur <|-- Parent

    Filiere "1" --> "N" Groupe : contient
    Groupe "1" --> "N" Etudiant : regroupe
    Enseignant "1" --> "N" Cours : enseigne
    Cours "N" --> "N" Groupe : dispensé_à
    Cours "1" --> "N" SessionCours : génère
    SessionCours "1" --> "N" Presence : enregistre
    Etudiant "1" --> "N" Presence : a
    Parent "N" --> "N" Etudiant : est_tuteur_de
    Parent "1" --> "N" Notification : reçoit
```

---

## 6. Diagrammes de Cas d'Utilisation

### 6.1 — Vue Globale

```mermaid
flowchart TB
    ADMIN(["👤 Administrateur"])
    ENSEIGNANT(["👤 Enseignant"])
    ETUDIANT(["👤 Étudiant"])
    PARENT(["👤 Parent"])

    subgraph SYS["Système GesPresence"]
        AUTH["Se connecter / Déconnecter"]
        PROFIL["Modifier son profil"]

        subgraph ADM_MOD["Module Administration"]
            GU["Gérer Utilisateurs"]
            GF["Gérer Filières & Groupes"]
            GC["Gérer Cours"]
            STAT["Voir Statistiques Globales"]
            RAPP["Générer Rapports"]
        end

        subgraph ENS_MOD["Module Enseignant"]
            VS["Voir Mes Sessions"]
            MP["Marquer Présence"]
            JA["Justifier une Absence"]
            RC["Rapport Cours"]
        end

        subgraph ETU_MOD["Module Étudiant"]
            HP["Consulter Mon Historique"]
            TP["Voir Mon Taux de Présence"]
        end

        subgraph PAR_MOD["Module Parent"]
            VP["Voir Présence Enfant"]
            NOTIF["Consulter Notifications"]
        end
    end

    ADMIN --> AUTH
    ADMIN --> PROFIL
    ADMIN --> GU
    ADMIN --> GF
    ADMIN --> GC
    ADMIN --> STAT
    ADMIN --> RAPP

    ENSEIGNANT --> AUTH
    ENSEIGNANT --> PROFIL
    ENSEIGNANT --> VS
    ENSEIGNANT --> MP
    ENSEIGNANT --> JA
    ENSEIGNANT --> RC

    ETUDIANT --> AUTH
    ETUDIANT --> PROFIL
    ETUDIANT --> HP
    ETUDIANT --> TP

    PARENT --> AUTH
    PARENT --> PROFIL
    PARENT --> VP
    PARENT --> NOTIF
```

### 6.2 — Cas d'utilisation : Marquer la Présence (Enseignant)

```mermaid
sequenceDiagram
    actor ENS as Enseignant
    participant UI as Interface Web
    participant VIEW as Django View
    participant MODEL as Modèles ORM
    participant DB as MySQL

    ENS->>UI: Accède à "Mes Sessions du jour"
    UI->>VIEW: GET /sessions/today/
    VIEW->>MODEL: SessionCours.objects.filter(date=today, enseignant=user)
    MODEL->>DB: SELECT session WHERE date=today
    DB-->>MODEL: Liste des sessions
    MODEL-->>VIEW: QuerySet sessions
    VIEW-->>UI: Affiche liste des sessions

    ENS->>UI: Sélectionne une session
    UI->>VIEW: GET /sessions/<id>/presence/
    VIEW->>MODEL: Etudiant.objects.filter(groupe=session.groupe)
    MODEL->>DB: SELECT étudiants du groupe
    DB-->>MODEL: Liste des étudiants
    VIEW-->>UI: Affiche feuille de présence

    ENS->>UI: Coche les présents / absents
    ENS->>UI: Clique "Enregistrer"
    UI->>VIEW: POST /sessions/<id>/presence/ {presences:[...]}
    VIEW->>MODEL: Presence.objects.bulk_create(...)
    MODEL->>DB: INSERT INTO presence (...)
    DB-->>MODEL: OK
    VIEW->>MODEL: Envoyer notifications parents (absents)
    VIEW-->>UI: Succès + Récapitulatif
    UI-->>ENS: Confirmation enregistrée
```

---

## 7. Diagrammes de Séquence

### 7.1 — Authentification

```mermaid
sequenceDiagram
    actor USER as Utilisateur
    participant UI as Interface Login
    participant VIEW as LoginView
    participant AUTH as Django Auth
    participant DB as MySQL

    USER->>UI: Saisit email + mot de passe
    UI->>VIEW: POST /login/ {email, password}
    VIEW->>AUTH: authenticate(email, password)
    AUTH->>DB: SELECT utilisateur WHERE email=...
    DB-->>AUTH: Données utilisateur
    AUTH->>AUTH: Vérifie hash du mot de passe
    alt Succès
        AUTH-->>VIEW: Objet utilisateur
        VIEW->>VIEW: Crée session Django
        VIEW-->>UI: Redirect vers dashboard selon rôle
        UI-->>USER: Dashboard personnalisé
    else Échec
        AUTH-->>VIEW: None
        VIEW-->>UI: Erreur "Identifiants incorrects"
        UI-->>USER: Message d'erreur
    end
```

### 7.2 — Consultation Présence par le Parent

```mermaid
sequenceDiagram
    actor PAR as Parent
    participant UI as Interface Parent
    participant VIEW as ParentView
    participant MODEL as ORM
    participant NOTIF as Service Notification

    PAR->>UI: Accède au tableau de bord
    UI->>VIEW: GET /parent/dashboard/
    VIEW->>MODEL: Parent.objects.get(user=request.user)
    MODEL-->>VIEW: Objet parent + enfants liés
    VIEW->>MODEL: Presence.objects.filter(etudiant__in=enfants).recent()
    MODEL-->>VIEW: Historique des présences
    VIEW->>NOTIF: Notification.objects.filter(parent=parent, lu=False)
    NOTIF-->>VIEW: Notifications non lues
    VIEW-->>UI: Dashboard avec historique + alertes
    UI-->>PAR: Affiche données

    PAR->>UI: Clique sur une notification
    UI->>VIEW: POST /notifications/<id>/lire/
    VIEW->>MODEL: notification.lu = True; save()
    MODEL-->>VIEW: OK
    VIEW-->>UI: Notification marquée comme lue
```

### 7.3 — Génération de Rapport (Administrateur)

```mermaid
sequenceDiagram
    actor ADMIN as Administrateur
    participant UI as Interface Admin
    participant VIEW as RapportView
    participant MODEL as ORM
    participant PDF as Service PDF/Export

    ADMIN->>UI: Sélectionne critères (filière, période, groupe)
    UI->>VIEW: POST /rapports/generer/ {filiere_id, date_debut, date_fin, groupe_id}
    VIEW->>MODEL: Filtre sessions + présences selon critères
    MODEL-->>VIEW: DataFrame de données
    VIEW->>VIEW: Calcule statistiques (taux, absences, retards)
    VIEW->>PDF: Génère PDF/Excel
    PDF-->>VIEW: Fichier généré
    VIEW-->>UI: URL de téléchargement
    UI-->>ADMIN: Lien téléchargement rapport
```

---

## 8. Diagramme d'État — Présence

```mermaid
stateDiagram-v2
    [*] --> NonMarquee : Session créée

    NonMarquee --> Present : Enseignant coche "Présent"
    NonMarquee --> Absent : Enseignant coche "Absent"
    NonMarquee --> Retard : Enseignant coche "En retard"

    Absent --> Justifie : Justification soumise\n(enseignant ou admin)
    Retard --> Justifie : Justification soumise

    Present --> [*] : Finalisée
    Justifie --> [*] : Finalisée

    Absent --> Absent : Notification parent envoyée
    Retard --> Retard : Notification parent envoyée
```

---

## 9. Diagramme de Composants

```mermaid
graph LR
    subgraph FRONTEND["Frontend (Browser)"]
        LOGIN_UI["Page Login"]
        DASH_UI["Dashboard"]
        PRESENCE_UI["Feuille Présence"]
        RAPPORT_UI["Rapports"]
        NOTIF_UI["Notifications"]
    end

    subgraph DJANGO_APP["Application Django"]
        subgraph APPS["Django Apps"]
            AUTH_APP["accounts/\n(Authentification)"]
            ETUDIANT_APP["etudiants/\n(Gestion Étudiants)"]
            ENSEIGNANT_APP["enseignants/\n(Gestion Enseignants)"]
            PRESENCE_APP["presences/\n(Gestion Présences)"]
            COURS_APP["cours/\n(Gestion Cours)"]
            RAPPORT_APP["rapports/\n(Rapports & Stats)"]
            NOTIF_APP["notifications/\n(Alertes Parents)"]
        end

        ADMIN_SITE["Django Admin\nSite"]
        STATIC["Static Files\n(CSS/JS/Images)"]
        MEDIA["Media Files\n(Photos)"]
    end

    subgraph DB_LAYER["Couche Données"]
        MYSQL_DB[("MySQL 8\nBase de Données")]
        DJANGO_ORM["Django ORM"]
    end

    FRONTEND <--> DJANGO_APP
    DJANGO_APP --> DJANGO_ORM
    DJANGO_ORM --> MYSQL_DB
```

---

## 10. Structure du Projet Django

```
gespresence/
├── manage.py
├── requirements.txt
├── .env                          # Variables d'environnement (DB, SECRET_KEY)
│
├── gespresence/                  # Projet principal
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                     # App : Authentification & Utilisateurs
│   ├── models.py                 # Utilisateur, Etudiant, Enseignant, Parent, Admin
│   ├── views.py                  # login, logout, register, profil
│   ├── forms.py
│   ├── urls.py
│   └── templates/accounts/
│       ├── login.html
│       ├── register.html
│       └── profil.html
│
├── etudiants/                    # App : Gestion des Étudiants
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/etudiants/
│       ├── liste.html
│       ├── detail.html
│       └── form.html
│
├── enseignants/                  # App : Gestion des Enseignants
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/enseignants/
│
├── cours/                        # App : Cours, Filières, Groupes, Sessions
│   ├── models.py                 # Cours, Filiere, Groupe, SessionCours
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/cours/
│
├── presences/                    # App : Marquage & Historique Présence
│   ├── models.py                 # Presence
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/presences/
│       ├── feuille_presence.html
│       └── historique.html
│
├── rapports/                     # App : Statistiques & Exports
│   ├── views.py
│   ├── utils.py                  # Génération PDF/Excel
│   ├── urls.py
│   └── templates/rapports/
│
├── notifications/                # App : Alertes & Notifications Parents
│   ├── models.py
│   ├── signals.py                # Envoi auto sur absence
│   ├── views.py
│   └── urls.py
│
├── static/
│   ├── css/
│   │   ├── main.css              # Style global inspiré OFPPT
│   │   └── dashboard.css
│   ├── js/
│   │   ├── presence.js           # Logique feuille présence
│   │   └── charts.js             # Graphiques statistiques
│   └── img/
│       └── logo.png
│
├── media/                        # Fichiers uploadés (photos profil)
│
└── templates/
    ├── base.html                 # Template de base avec navbar
    ├── dashboard_admin.html
    ├── dashboard_enseignant.html
    ├── dashboard_etudiant.html
    └── dashboard_parent.html
```

---

## 11. Modèles Django (ORM)

```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    ROLES = [('admin','Administrateur'),('enseignant','Enseignant'),
             ('etudiant','Étudiant'),('parent','Parent')]
    role      = models.CharField(max_length=20, choices=ROLES)
    telephone = models.CharField(max_length=20, blank=True)

class Filiere(models.Model):
    nom          = models.CharField(max_length=100)
    code         = models.CharField(max_length=20, unique=True)
    description  = models.TextField(blank=True)
    duree_annees = models.IntegerField(default=2)

class Groupe(models.Model):
    nom            = models.CharField(max_length=50)
    annee_scolaire = models.IntegerField()
    effectif_max   = models.IntegerField(default=30)
    filiere        = models.ForeignKey(Filiere, on_delete=models.CASCADE,
                                       related_name='groupes')

class Etudiant(models.Model):
    user           = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    matricule      = models.CharField(max_length=20, unique=True)
    date_naissance = models.DateField()
    photo          = models.ImageField(upload_to='etudiants/', blank=True)
    groupe         = models.ForeignKey(Groupe, on_delete=models.SET_NULL,
                                       null=True, related_name='etudiants')

class Enseignant(models.Model):
    user       = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    specialite = models.CharField(max_length=100)
    grade      = models.CharField(max_length=50)
    cin        = models.CharField(max_length=20, unique=True)

class Parent(models.Model):
    user               = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    adresse            = models.TextField(blank=True)
    telephone_urgence  = models.CharField(max_length=20)
    enfants            = models.ManyToManyField(Etudiant, related_name='parents')

# cours/models.py
class Cours(models.Model):
    nom           = models.CharField(max_length=100)
    code_cours    = models.CharField(max_length=20, unique=True)
    description   = models.TextField(blank=True)
    volume_horaire = models.IntegerField()
    enseignant    = models.ForeignKey(Enseignant, on_delete=models.SET_NULL,
                                      null=True, related_name='cours')
    groupes       = models.ManyToManyField(Groupe, related_name='cours')

class SessionCours(models.Model):
    STATUTS = [('planifiee','Planifiée'),('terminee','Terminée'),('annulee','Annulée')]
    date_session = models.DateField()
    heure_debut  = models.TimeField()
    heure_fin    = models.TimeField()
    salle        = models.CharField(max_length=50)
    statut       = models.CharField(max_length=20, choices=STATUTS, default='planifiee')
    cours        = models.ForeignKey(Cours, on_delete=models.CASCADE,
                                     related_name='sessions')
    groupe       = models.ForeignKey(Groupe, on_delete=models.CASCADE)

# presences/models.py
class Presence(models.Model):
    STATUTS = [('present','Présent'),('absent','Absent'),
               ('retard','En retard'),('justifie','Justifié')]
    statut                = models.CharField(max_length=20, choices=STATUTS)
    justification         = models.TextField(blank=True)
    created_at            = models.DateTimeField(auto_now_add=True)
    notif_parent_envoyee  = models.BooleanField(default=False)
    etudiant              = models.ForeignKey(Etudiant, on_delete=models.CASCADE,
                                              related_name='presences')
    session               = models.ForeignKey(SessionCours, on_delete=models.CASCADE,
                                              related_name='presences')
    class Meta:
        unique_together = ['etudiant', 'session']
```

---

## 12. Plan des URLs & Vues

| URL                                    | Vue                        | Rôle requis       |
|----------------------------------------|----------------------------|-------------------|
| `/`                                    | `HomeView`                 | Tous              |
| `/login/`                              | `LoginView`                | Anonyme           |
| `/logout/`                             | `LogoutView`               | Authentifié       |
| `/admin/`                              | Django Admin               | Admin             |
| `/dashboard/`                          | `DashboardView`            | Tous              |
| `/etudiants/`                          | `EtudiantListView`         | Admin             |
| `/etudiants/<id>/`                     | `EtudiantDetailView`       | Admin, Enseignant |
| `/etudiants/<id>/presence/`            | `EtudiantPresenceView`     | Étudiant, Parent  |
| `/enseignants/`                        | `EnseignantListView`       | Admin             |
| `/cours/`                              | `CoursListView`            | Admin, Enseignant |
| `/cours/<id>/sessions/`                | `SessionListView`          | Enseignant        |
| `/sessions/<id>/presence/`             | `MarquerPresenceView`      | Enseignant        |
| `/presences/historique/`               | `HistoriquePresenceView`   | Tous              |
| `/rapports/`                           | `RapportListView`          | Admin             |
| `/rapports/generer/`                   | `GenererRapportView`       | Admin             |
| `/parent/dashboard/`                   | `ParentDashboardView`      | Parent            |
| `/notifications/`                      | `NotificationListView`     | Parent            |

---

## 13. Phases d'Implémentation

```mermaid
gantt
    title Planning d'Implémentation GesPresence
    dateFormat  YYYY-MM-DD
    section Phase 1 — Setup
    Initialisation Django & MySQL       :p1a, 2026-07-07, 2d
    Configuration settings.py & .env   :p1b, after p1a, 1d
    Création des apps Django            :p1c, after p1b, 1d

    section Phase 2 — Modèles & BDD
    Modèles Utilisateur & Auth          :p2a, after p1c, 2d
    Modèles Filière, Groupe, Cours      :p2b, after p2a, 2d
    Modèles Session & Présence          :p2c, after p2b, 2d
    Migrations & fixtures de test       :p2d, after p2c, 1d

    section Phase 3 — Authentification
    Login / Logout / Middleware rôles   :p3a, after p2d, 3d
    Dashboards par rôle                 :p3b, after p3a, 2d

    section Phase 4 — Modules Métier
    CRUD Étudiants                      :p4a, after p3b, 3d
    CRUD Enseignants & Cours            :p4b, after p4a, 3d
    Gestion Sessions & Groupes          :p4c, after p4b, 3d

    section Phase 5 — Présence
    Feuille de présence (Enseignant)    :p5a, after p4c, 4d
    Historique & taux de présence       :p5b, after p5a, 2d
    Notifications parents (absences)    :p5c, after p5b, 2d

    section Phase 6 — Rapports & Stats
    Statistiques globales (Admin)       :p6a, after p5c, 3d
    Export PDF / Excel                  :p6b, after p6a, 3d

    section Phase 7 — UI/UX
    Thème OFPPT (CSS/Bootstrap)         :p7a, after p6b, 4d
    Responsive & accessibilité          :p7b, after p7a, 2d

    section Phase 8 — Tests & Déploiement
    Tests unitaires & intégration       :p8a, after p7b, 4d
    Déploiement (serveur / Docker)      :p8b, after p8a, 3d
```

### Résumé des Phases

| Phase | Description                          | Durée estimée |
|-------|--------------------------------------|---------------|
| 1     | Setup Django + MySQL                 | ~4 jours      |
| 2     | Modèles & Base de données            | ~7 jours      |
| 3     | Authentification & Dashboards        | ~5 jours      |
| 4     | Modules CRUD (Étudiants, Cours…)     | ~9 jours      |
| 5     | Présence & Notifications             | ~8 jours      |
| 6     | Rapports & Statistiques              | ~6 jours      |
| 7     | Interface & Thème OFPPT              | ~6 jours      |
| 8     | Tests & Déploiement                  | ~7 jours      |
| **Total** |                                 | **~52 jours** |

---

## 14. Maquettes d'Interface

### Navigation principale (Sidebar — style OFPPT)

```
┌──────────────────────────────────────────────────────────┐
│  🏫  GesPresence                        [Photo Profil]   │
├──────────────────────────────────────────────────────────┤
│  SIDEBAR            │  CONTENU PRINCIPAL                 │
│  ─────────────────  │  ────────────────────────────────  │
│  📊 Tableau de bord │                                    │
│  👥 Étudiants       │   [Widget Stats]  [Widget Stats]  │
│  👨‍🏫 Enseignants    │                                    │
│  📚 Cours           │   [Tableau des dernières          │
│  ✅ Présences       │    sessions + présences]          │
│  📈 Rapports        │                                    │
│  🔔 Notifications   │   [Graphique taux présence]       │
│  ⚙️ Paramètres      │                                    │
│                     │                                    │
└──────────────────────────────────────────────────────────┘
```

### Feuille de Présence (Vue Enseignant)

```
┌─────────────────────────────────────────────────────────┐
│  Feuille de Présence — Cours: [Nom Cours]               │
│  Groupe: [Nom Groupe]  |  Date: [JJ/MM/AAAA]  |  Salle  │
├──────┬──────────────────┬───────────┬────────┬──────────┤
│  N°  │  Nom & Prénom    │  Présent  │ Absent │  Retard  │
├──────┼──────────────────┼───────────┼────────┼──────────┤
│  01  │  Ahmed BENAISSA  │    ✅     │        │          │
│  02  │  Sara ALAMI      │           │   ❌   │          │
│  03  │  Karim ZIDANE    │           │        │   ⏰     │
│ ...  │  ...             │   ...     │  ...   │  ...     │
├──────┴──────────────────┴───────────┴────────┴──────────┤
│  [Tout Présent]  [Tout Absent]       [💾 Enregistrer]   │
└─────────────────────────────────────────────────────────┘
```

---

## Dépendances Python (requirements.txt)

```txt
Django>=4.2
mysqlclient>=2.2
Pillow>=10.0          # Upload photos
django-crispy-forms   # Formulaires stylisés
crispy-bootstrap5
reportlab             # Génération PDF
openpyxl              # Export Excel
django-filter         # Filtres avancés
python-decouple       # Variables .env
whitenoise            # Static files en production
```

---

*Document généré le 2026-07-04 — Projet : Gestion de Présence des Étudiants*
