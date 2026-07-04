# 🎓 GesPresence — Application de Gestion de Présence des Étudiants

<div align="center">

![Django](https://img.shields.io/badge/Django-4.2_LTS-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.x-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Application web complète de gestion de présence des étudiants — inspirée du portail OFPPT**

[🚀 Démo](#-démarrage-rapide) • [📐 Architecture](#-architecture) • [🗄️ Base de données](#️-modèle-de-données) • [📋 Fonctionnalités](#-fonctionnalités)

</div>

---

## 📋 Table des Matières

1. [Vue d'ensemble](#-vue-densemble)
2. [Stack Technique](#-stack-technique)
3. [Architecture](#-architecture)
4. [Modèle de Données — MCD](#️-modèle-de-données--mcd)
5. [Modèle Logique — MLD](#-modèle-logique--mld)
6. [Diagramme de Classes UML](#-diagramme-de-classes-uml)
7. [Cas d'Utilisation](#-diagrammes-de-cas-dutilisation)
8. [Diagrammes de Séquence](#-diagrammes-de-séquence)
9. [Diagramme d'État](#-diagramme-détat--présence)
10. [Diagramme de Composants](#-diagramme-de-composants)
11. [Fonctionnalités](#-fonctionnalités)
12. [Structure du Projet](#-structure-du-projet)
13. [Démarrage Rapide](#-démarrage-rapide)
14. [Comptes de Test](#-comptes-de-test)
15. [API des URLs](#-api-des-urls)
16. [Données de Test](#-données-de-test)

---

## 🌟 Vue d'ensemble

**GesPresence** est une application web Django permettant de gérer la présence des étudiants dans un établissement de formation (OFPPT). Elle offre une interface dédiée pour chaque type d'utilisateur, des notifications automatiques aux parents en cas d'absence, et la génération de rapports détaillés.

### Captures d'écran

| Dashboard Admin | Feuille de Présence | Dashboard Enseignant |
|:---:|:---:|:---:|
| Statistiques temps réel | Marquage rapide | Sessions du jour |

---

## 🛠 Stack Technique

| Couche | Technologie | Version |
|--------|-------------|---------|
| **Backend** | Django | 4.2 LTS |
| **Langage** | Python | 3.13 |
| **Base de données** | MySQL (XAMPP/MariaDB) | 10.4+ |
| **Frontend** | Bootstrap + Jinja2 | 5.3 |
| **Icônes** | Bootstrap Icons | 1.11 |
| **Export** | openpyxl, reportlab | latest |
| **Auth** | Django Auth (AbstractUser) | — |
| **Env** | python-decouple | 3.8 |
| **Static** | WhiteNoise | 6.x |

---

## 🏗 Architecture

### Pattern MVT (Model–View–Template)

```mermaid
graph TB
    subgraph Client["🌐 Navigateur Web"]
        HTML["HTML / CSS / JS"]
        BS["Bootstrap 5"]
    end

    subgraph Django["⚙️ Serveur Django"]
        URLS["urls.py — Routeur"]
        VIEWS["Views — Logique Métier"]
        FORMS["Forms — Validation"]
        MODELS["Models ORM"]
        ADMIN["Django Admin"]
        AUTH["Django Auth"]
        TEMPLATES["Templates Jinja2"]
    end

    subgraph DB["🗄️ Base de Données"]
        MySQL["MySQL 8 / MariaDB"]
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

### Flux d'une Requête

```mermaid
flowchart LR
    REQ([📨 Requête HTTP]) --> URL[urls.py]
    URL --> VIEW[View\nLogique métier]
    VIEW <--> MODEL[Model\nORM Django]
    MODEL <--> MYSQL[(MySQL)]
    VIEW --> TEMPLATE[Template\nHTML]
    TEMPLATE --> RESP([📤 Réponse HTTP])
```

---

## 🗂️ Modèle de Données — MCD

> Le MCD représente les entités métier et leurs associations sans implémentation physique.

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

## 📊 Modèle Logique — MLD

> Le MLD traduit le MCD en tables relationnelles avec clés primaires et étrangères.

```mermaid
erDiagram
    utilisateur {
        BIGINT id PK
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
        BIGINT id PK
        BIGINT user_id FK
        VARCHAR matricule "UNIQUE"
        DATE date_naissance
        VARCHAR photo
        BIGINT groupe_id FK
    }

    enseignant {
        BIGINT id PK
        BIGINT user_id FK
        VARCHAR specialite
        VARCHAR grade
        VARCHAR cin "UNIQUE"
    }

    parent {
        BIGINT id PK
        BIGINT user_id FK
        TEXT adresse
        VARCHAR telephone_urgence
    }

    parent_etudiant {
        BIGINT parent_id FK
        BIGINT etudiant_id FK
    }

    filiere {
        BIGINT id PK
        VARCHAR nom
        VARCHAR code "UNIQUE"
        TEXT description
        INT duree_annees
    }

    groupe {
        BIGINT id PK
        VARCHAR nom
        INT annee_scolaire
        INT effectif_max
        BIGINT filiere_id FK
    }

    cours {
        BIGINT id PK
        VARCHAR nom
        VARCHAR code_cours "UNIQUE"
        TEXT description
        INT volume_horaire
        BIGINT enseignant_id FK
    }

    cours_groupe {
        BIGINT cours_id FK
        BIGINT groupe_id FK
    }

    session_cours {
        BIGINT id PK
        DATE date_session
        TIME heure_debut
        TIME heure_fin
        VARCHAR salle
        ENUM statut "planifiee,terminee,annulee"
        BIGINT cours_id FK
        BIGINT groupe_id FK
    }

    presence {
        BIGINT id PK
        ENUM statut "present,absent,retard,justifie"
        TEXT justification
        DATETIME created_at
        BOOL notif_parent_envoyee
        BIGINT etudiant_id FK
        BIGINT session_id FK
    }

    notification {
        BIGINT id PK
        TEXT message
        ENUM type "absence,retard,rapport,info"
        BOOL lu
        DATETIME envoyee_le
        BIGINT parent_id FK
    }

    utilisateur ||--o| etudiant : "user_id"
    utilisateur ||--o| enseignant : "user_id"
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

---

## 🧩 Diagramme de Classes UML

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
        +creer_session(date, debut, fin, salle)
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

## 👥 Diagrammes de Cas d'Utilisation

### Vue Globale

```mermaid
flowchart TB
    ADMIN(["👤 Administrateur"])
    ENSEIGNANT(["👤 Enseignant"])
    ETUDIANT(["👤 Étudiant"])
    PARENT(["👤 Parent"])

    subgraph SYS["🎓 Système GesPresence"]
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

    ADMIN --> AUTH & PROFIL & GU & GF & GC & STAT & RAPP
    ENSEIGNANT --> AUTH & PROFIL & VS & MP & JA & RC
    ETUDIANT --> AUTH & PROFIL & HP & TP
    PARENT --> AUTH & PROFIL & VP & NOTIF
```

---

## 🔄 Diagrammes de Séquence

### 1. Authentification

```mermaid
sequenceDiagram
    actor USER as Utilisateur
    participant UI as Interface Login
    participant VIEW as LoginView
    participant AUTH as Django Auth
    participant DB as MySQL

    USER->>UI: Saisit email + mot de passe
    UI->>VIEW: POST /accounts/login/
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

### 2. Marquer la Présence (Enseignant)

```mermaid
sequenceDiagram
    actor ENS as Enseignant
    participant UI as Interface Web
    participant VIEW as Django View
    participant MODEL as Modèles ORM
    participant DB as MySQL

    ENS->>UI: Accède à "Mes Sessions du jour"
    UI->>VIEW: GET /enseignants/mes-sessions/
    VIEW->>MODEL: SessionCours.objects.filter(date=today, enseignant=user)
    MODEL->>DB: SELECT session WHERE date=today
    DB-->>MODEL: Liste des sessions
    MODEL-->>VIEW: QuerySet sessions
    VIEW-->>UI: Affiche liste des sessions

    ENS->>UI: Sélectionne une session
    UI->>VIEW: GET /presences/session/id/
    VIEW->>MODEL: Etudiant.objects.filter(groupe=session.groupe)
    DB-->>MODEL: Liste des étudiants
    VIEW-->>UI: Affiche feuille de présence

    ENS->>UI: Coche les présents / absents
    ENS->>UI: Clique "Enregistrer"
    UI->>VIEW: POST /presences/session/id/
    VIEW->>MODEL: Presence.objects.update_or_create(...)
    MODEL->>DB: INSERT INTO presence (...)
    DB-->>MODEL: OK
    VIEW->>MODEL: Envoyer notifications parents (absents)
    VIEW-->>UI: Succès + Récapitulatif
    UI-->>ENS: Confirmation enregistrée
```

### 3. Consultation Parent

```mermaid
sequenceDiagram
    actor PAR as Parent
    participant UI as Interface Parent
    participant VIEW as ParentView
    participant MODEL as ORM

    PAR->>UI: Accède au tableau de bord
    UI->>VIEW: GET /accounts/dashboard/
    VIEW->>MODEL: Parent.objects.get(user=request.user)
    MODEL-->>VIEW: Objet parent + enfants liés
    VIEW->>MODEL: Presence.objects.filter(etudiant__in=enfants).recent()
    MODEL-->>VIEW: Historique des présences
    VIEW-->>UI: Dashboard avec historique + alertes
    UI-->>PAR: Affiche données

    PAR->>UI: Clique sur une notification
    UI->>VIEW: POST /notifications/id/lire/
    VIEW->>MODEL: notification.lu = True; save()
    VIEW-->>UI: Notification marquée comme lue
```

### 4. Génération de Rapport

```mermaid
sequenceDiagram
    actor ADMIN as Administrateur
    participant UI as Interface Admin
    participant VIEW as RapportView
    participant MODEL as ORM
    participant EXCEL as openpyxl

    ADMIN->>UI: Sélectionne critères (filière, période, groupe)
    UI->>VIEW: GET /rapports/generer/?groupe=1&date_debut=...
    VIEW->>MODEL: Filtre sessions + présences selon critères
    MODEL-->>VIEW: QuerySet de données
    VIEW->>VIEW: Calcule statistiques (taux, absences, retards)

    alt Format HTML
        VIEW-->>UI: Tableau HTML
        UI-->>ADMIN: Affiche rapport
    else Format Excel
        VIEW->>EXCEL: Génère fichier .xlsx
        EXCEL-->>VIEW: Fichier prêt
        VIEW-->>UI: Téléchargement automatique
        UI-->>ADMIN: Fichier Excel téléchargé
    end
```

---

## 🔁 Diagramme d'État — Présence

```mermaid
stateDiagram-v2
    [*] --> NonMarquee : Session créée

    NonMarquee --> Present : Enseignant coche "Présent"
    NonMarquee --> Absent : Enseignant coche "Absent"
    NonMarquee --> Retard : Enseignant coche "En retard"

    Absent --> Justifie : Justification soumise
    Retard --> Justifie : Justification soumise

    Present --> [*] : Finalisée
    Justifie --> [*] : Finalisée

    Absent --> Absent : Notification parent envoyée
    Retard --> Retard : Notification parent envoyée
```

---

## 🧱 Diagramme de Composants

```mermaid
graph LR
    subgraph FRONTEND["🌐 Frontend"]
        LOGIN_UI["Page Login"]
        DASH_UI["Dashboard"]
        PRESENCE_UI["Feuille Présence"]
        RAPPORT_UI["Rapports"]
        NOTIF_UI["Notifications"]
    end

    subgraph DJANGO["⚙️ Application Django"]
        subgraph APPS["Django Apps"]
            AUTH_APP["accounts/\nAuthentification"]
            ETUDIANT_APP["etudiants/\nGestion Étudiants"]
            ENSEIGNANT_APP["enseignants/\nGestion Enseignants"]
            PRESENCE_APP["presences/\nGestion Présences"]
            COURS_APP["cours/\nGestion Cours"]
            RAPPORT_APP["rapports/\nRapports & Stats"]
            NOTIF_APP["notifications/\nAlertes Parents"]
        end
        ADMIN_SITE["Django Admin"]
        STATIC["Static Files\nCSS/JS/Images"]
        MEDIA["Media Files\nPhotos"]
    end

    subgraph DB_LAYER["🗄️ Données"]
        MYSQL_DB[("MySQL\nBase de Données")]
        DJANGO_ORM["Django ORM"]
    end

    FRONTEND <--> DJANGO
    DJANGO --> DJANGO_ORM
    DJANGO_ORM --> MYSQL_DB
```

---

## ✨ Fonctionnalités

### Par Rôle

| Fonctionnalité | Admin | Enseignant | Étudiant | Parent |
|---|:---:|:---:|:---:|:---:|
| Dashboard personnalisé | ✅ | ✅ | ✅ | ✅ |
| Gestion utilisateurs | ✅ | ❌ | ❌ | ❌ |
| Gestion filières/groupes | ✅ | ❌ | ❌ | ❌ |
| Gestion cours | ✅ | ❌ | ❌ | ❌ |
| Marquer présence | ❌ | ✅ | ❌ | ❌ |
| Consulter historique | ✅ | ✅ | ✅ | ✅ |
| Notifications parents | auto | auto | ❌ | ✅ |
| Rapports & statistiques | ✅ | ❌ | ❌ | ❌ |
| Export Excel | ✅ | ❌ | ❌ | ❌ |
| Django Admin | ✅ | ❌ | ❌ | ❌ |

### Statuts de Présence

```
● Présent   — Cours suivi normalement
● Absent    — Non présent + notification parent
● Retard    — Arrivée tardive + notification parent
● Justifié  — Absence avec justificatif accepté
```

---

## 📁 Structure du Projet

```
gespresence/
├── manage.py
├── requirements.txt
├── .env                          # Variables d'environnement
├── seed_data.py                  # Script données initiales
├── seed_parents.py               # Script parents
│
├── gespresence/                  # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                     # Auth & Utilisateurs
│   ├── models.py                 # Utilisateur, Etudiant, Enseignant, Parent...
│   ├── views.py                  # login, logout, dashboard, profil
│   ├── forms.py                  # LoginForm
│   ├── urls.py
│   ├── admin.py
│   └── decorators.py             # role_required
│
├── etudiants/                    # Gestion Étudiants
├── enseignants/                  # Gestion Enseignants
│
├── cours/                        # Cours, Sessions, Emploi du temps
│   ├── models.py                 # Cours, SessionCours
│   ├── admin.py
│   ├── views.py
│   └── urls.py
│
├── presences/                    # Marquage & Historique
│   ├── models.py                 # Presence
│   ├── views.py                  # feuille_presence, historique
│   ├── urls.py
│   └── templatetags/
│       └── presence_filters.py   # get_item, get_statut
│
├── rapports/                     # Statistiques & Exports
│   └── views.py                  # export Excel via openpyxl
│
├── notifications/                # Alertes Parents
│   └── models.py                 # Notification
│
├── static/
│   ├── css/
│   │   └── main.css              # Thème OFPPT
│   └── js/
│
├── media/                        # Fichiers uploadés
│
└── templates/
    ├── base.html                 # Layout principal + sidebar
    ├── dashboard_admin.html
    ├── dashboard_enseignant.html
    ├── dashboard_etudiant.html
    ├── dashboard_parent.html
    ├── accounts/
    ├── etudiants/
    ├── enseignants/
    ├── cours/
    ├── presences/
    ├── rapports/
    └── notifications/
```

---

## 🚀 Démarrage Rapide

### Prérequis

- Python 3.10+
- MySQL 8 / MariaDB 10.4+ (XAMPP recommandé)
- Git

### Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/abdeladimdemnati3-hash/project_de_presance-d-etudiant.git
cd "project_de_presance-d-etudiant"

# 2. Créer l'environnement virtuel
python -m venv venv
.\venv\Scripts\activate          # Windows
# source venv/bin/activate       # Linux/Mac

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env : DB_NAME, DB_USER, DB_PASSWORD
```

### Configuration `.env`

```ini
SECRET_KEY=votre-clé-secrète-longue-et-aléatoire
DJANGO_DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=gespresence_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

### Base de données & Migrations

```bash
# Créer la base de données MySQL
mysql -u root -e "CREATE DATABASE gespresence_db CHARACTER SET utf8mb4;"

# Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# Créer le superutilisateur
python manage.py createsuperuser
```

### Données de Démonstration

```bash
# Créer filières, groupes, professeurs, cours, 96 sessions
python seed_data.py

# Créer 35 étudiants + 35 parents (un par étudiant)
python seed_parents.py
```

### Lancer le Serveur

```bash
python manage.py runserver 8000
```

🌐 Ouvrir [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔑 Comptes de Test

| Rôle | Username | Mot de passe | Description |
|------|----------|-------------|-------------|
| **Administrateur** | `admin` | `admin1234` | Accès complet |
| **Enseignant** | `prof_karim` | `prof1234` | Développement Web |
| **Enseignant** | `prof_sara` | `prof1234` | Python & Django |
| **Enseignant** | `prof_youssef` | `prof1234` | Réseaux & Cybersécurité |
| **Enseignant** | `prof_fatima` | `prof1234` | Comptabilité |
| **Enseignant** | `prof_amine` | `prof1234` | Mécatronique |
| **Enseignant** | `prof_nadia` | `prof1234` | Mathématiques |
| **Étudiant** | `etudiant1` | `etudiant1234` | Mohammed Alami — DEV-101 |
| **Parent** | `par_stu2026001` | `parent1234` | Parent de Mohammed Alami |

---

## 🗺 API des URLs

| URL | Vue | Rôle requis | Description |
|-----|-----|-------------|-------------|
| `/` | Redirect | Tous | → Dashboard |
| `/accounts/login/` | `LoginView` | Anonyme | Connexion |
| `/accounts/logout/` | `LogoutView` | Auth | Déconnexion |
| `/accounts/dashboard/` | `DashboardView` | Auth | Dashboard selon rôle |
| `/accounts/profil/` | `ProfilView` | Auth | Mon profil |
| `/etudiants/` | `EtudiantListView` | Admin/Ens | Liste étudiants |
| `/etudiants/<id>/` | `EtudiantDetailView` | Admin/Ens | Détail étudiant |
| `/enseignants/` | `EnseignantListView` | Admin | Liste enseignants |
| `/enseignants/<id>/` | `EnseignantDetailView` | Admin | Détail enseignant |
| `/enseignants/mes-sessions/` | `MesSessionsView` | Enseignant | Sessions du prof |
| `/cours/` | `CoursListView` | Admin/Ens | Liste cours |
| `/cours/<id>/sessions/` | `SessionListView` | Admin/Ens | Sessions d'un cours |
| `/presences/` | `HistoriqueView` | Tous | Historique présences |
| `/presences/session/<id>/` | `FeuillePresenceView` | Enseignant | Marquer présence |
| `/rapports/` | `RapportListView` | Admin | Page rapports |
| `/rapports/generer/` | `GenererRapportView` | Admin | Générer rapport |
| `/notifications/` | `NotificationListView` | Parent | Mes notifications |
| `/admin/` | Django Admin | Superuser | Administration |

---

## 📊 Données de Test

### Filières & Groupes

| Filière | Code | Groupes | Étudiants |
|---------|------|---------|-----------|
| Développement Digital | `DEV` | DEV-101, DEV-102 | ~12 |
| Réseaux Informatiques | `RESEAU` | RES-101, RES-102 | ~12 |
| Technicien Comptable | `COMPTA` | COMPTA-101 | ~6 |
| Mécatronique | `MECA` | MECA-101 | ~7 |

### Emploi du Temps (4 semaines)

| Cours | Professeur | Groupes | Jour | Horaire |
|-------|-----------|---------|------|---------|
| HTML/CSS & Bootstrap | prof_karim | DEV-101, DEV-102 | Lundi | 08:30 / 10:45 |
| JavaScript & React | prof_karim | DEV-101, DEV-102 | Mardi | 08:30 / 10:45 |
| Python & Django | prof_sara | DEV-101, DEV-102 | Mercredi | 08:30 / 10:45 |
| Base de Données MySQL | prof_sara | DEV-101, DEV-102 | Jeudi | 08:30 / 10:45 |
| Cisco CCNA | prof_youssef | RES-101, RES-102 | Lundi | 08:30 / 10:45 |
| Comptabilité Générale | prof_fatima | COMPTA-101 | Lundi | 14:00 |
| Automatisme Industriel | prof_amine | MECA-101 | Lundi | 08:30 |

**Total : 96 sessions planifiées sur 4 semaines**

---

## 📦 Dépendances

```txt
Django>=4.2,<5.0
mysqlclient>=2.2
Pillow>=12.0
django-crispy-forms>=2.0
crispy-bootstrap5
reportlab>=5.0
openpyxl>=3.1
django-filter>=25.0
python-decouple>=3.8
whitenoise>=6.0
python-pptx>=1.0
```

---

## 🔒 Sécurité

- ✅ Protection CSRF sur tous les formulaires
- ✅ Mots de passe hashés (PBKDF2)
- ✅ `@login_required` sur toutes les vues protégées
- ✅ Décorateur `role_required` pour contrôle d'accès par rôle
- ✅ Variables sensibles dans `.env` (jamais dans le code)
- ✅ `DJANGO_DEBUG` séparé de `DEBUG` système
- ✅ SQL via ORM uniquement (pas d'injection SQL)
- ✅ `X-Frame-Options: DENY` activé

---

## 🤝 Contribution

```bash
# Fork → Clone → Branch → Commit → Pull Request
git checkout -b feature/ma-fonctionnalite
git commit -m "feat: description de la fonctionnalité"
git push origin feature/ma-fonctionnalite
```

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir [LICENSE](LICENSE) pour plus de détails.

---

<div align="center">

**Fait avec ❤️ — Django 4.2 LTS • Python 3.13 • Bootstrap 5**

🌐 [http://127.0.0.1:8000/](http://127.0.0.1:8000/) | 🔑 admin / admin1234

</div>
