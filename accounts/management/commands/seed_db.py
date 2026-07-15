"""
Management command: seed_db
Creates: 4 filières, 6 groupes, 10 enseignants, 20 cours, 30 étudiants
Run: python manage.py seed_db
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.models import Utilisateur, Enseignant, Filiere, Groupe, Etudiant
from cours.models import Cours, SessionCours
from datetime import date, time, timedelta


FILIERES = [
    {'code': 'DEV',    'nom': 'Développement Digital',       'duree': 2},
    {'code': 'RESEAU', 'nom': 'Réseaux Informatiques',       'duree': 2},
    {'code': 'COMPTA', 'nom': 'Technicien Comptable',         'duree': 2},
    {'code': 'MECA',   'nom': 'Technicien en Mécatronique',   'duree': 2},
]

GROUPES = [
    {'nom': 'DEV-101',    'filiere': 'DEV',    'annee': 2026},
    {'nom': 'DEV-102',    'filiere': 'DEV',    'annee': 2026},
    {'nom': 'RES-101',    'filiere': 'RESEAU', 'annee': 2026},
    {'nom': 'RES-102',    'filiere': 'RESEAU', 'annee': 2026},
    {'nom': 'COMPTA-101', 'filiere': 'COMPTA', 'annee': 2026},
    {'nom': 'MECA-101',   'filiere': 'MECA',   'annee': 2026},
]

ENSEIGNANTS = [
    {'username': 'prof_karim',   'first_name': 'Karim',   'last_name': 'Bennani',  'email': 'karim@gespresence.ma',   'cin': 'BK100001', 'specialite': 'Développement Web',             'grade': 'Formateur Principal'},
    {'username': 'prof_sara',    'first_name': 'Sara',    'last_name': 'Alaoui',   'email': 'sara@gespresence.ma',    'cin': 'BK100002', 'specialite': 'Base de données & Python',      'grade': 'Formateur'},
    {'username': 'prof_youssef', 'first_name': 'Youssef', 'last_name': 'Idrissi',  'email': 'youssef@gespresence.ma', 'cin': 'BK100003', 'specialite': 'Réseaux & Cybersécurité',      'grade': 'Formateur Principal'},
    {'username': 'prof_fatima',  'first_name': 'Fatima',  'last_name': 'Zahra',    'email': 'fatima@gespresence.ma',  'cin': 'BK100004', 'specialite': 'Comptabilité & Finance',       'grade': 'Formateur'},
    {'username': 'prof_amine',   'first_name': 'Amine',   'last_name': 'Tazi',     'email': 'amine@gespresence.ma',   'cin': 'BK100005', 'specialite': 'Mécatronique & Automatisme',   'grade': 'Formateur'},
    {'username': 'prof_nadia',   'first_name': 'Nadia',   'last_name': 'Chraibi',  'email': 'nadia@gespresence.ma',   'cin': 'BK100006', 'specialite': 'Mathématiques & Algorithmique','grade': 'Formateur'},
    {'username': 'prof_omar',    'first_name': 'Omar',    'last_name': 'Mansouri', 'email': 'omar@gespresence.ma',    'cin': 'BK100007', 'specialite': 'Infrastructure Cloud',         'grade': 'Formateur'},
    {'username': 'prof_laila',   'first_name': 'Laila',   'last_name': 'Berrada',  'email': 'laila@gespresence.ma',   'cin': 'BK100008', 'specialite': 'Gestion de Projet',            'grade': 'Formateur'},
    {'username': 'prof_hassan',  'first_name': 'Hassan',  'last_name': 'Ouali',    'email': 'hassan@gespresence.ma',  'cin': 'BK100009', 'specialite': 'Électronique Industrielle',    'grade': 'Formateur Principal'},
    {'username': 'prof_zineb',   'first_name': 'Zineb',   'last_name': 'Kabbaj',   'email': 'zineb@gespresence.ma',   'cin': 'BK100010', 'specialite': 'Communication & Soft Skills',  'grade': 'Formateur'},
]

COURS = [
    # DEV — 7 modules
    {'code': 'DEV-HTML',  'nom': 'HTML/CSS & Bootstrap',         'vh': 80,  'prof': 'prof_karim',   'groupes': ['DEV-101', 'DEV-102']},
    {'code': 'DEV-JS',    'nom': 'JavaScript & React',           'vh': 100, 'prof': 'prof_karim',   'groupes': ['DEV-101', 'DEV-102']},
    {'code': 'DEV-PY',    'nom': 'Python & Django',              'vh': 120, 'prof': 'prof_sara',    'groupes': ['DEV-101', 'DEV-102']},
    {'code': 'DEV-DB',    'nom': 'Base de Données MySQL',         'vh': 80,  'prof': 'prof_sara',    'groupes': ['DEV-101', 'DEV-102']},
    {'code': 'DEV-CLOUD', 'nom': 'Cloud & DevOps',               'vh': 60,  'prof': 'prof_omar',    'groupes': ['DEV-101', 'DEV-102']},
    {'code': 'DEV-GP',    'nom': 'Gestion de Projet Agile',      'vh': 40,  'prof': 'prof_laila',   'groupes': ['DEV-101', 'DEV-102']},
    {'code': 'MATH-DEV',  'nom': 'Mathématiques pour Dev',       'vh': 60,  'prof': 'prof_nadia',   'groupes': ['DEV-101', 'DEV-102']},
    # RESEAU — 5 modules
    {'code': 'RES-CISCO', 'nom': 'Cisco CCNA',                   'vh': 120, 'prof': 'prof_youssef', 'groupes': ['RES-101', 'RES-102']},
    {'code': 'RES-SECU',  'nom': 'Cybersécurité & Ethical Hack', 'vh': 100, 'prof': 'prof_youssef', 'groupes': ['RES-101', 'RES-102']},
    {'code': 'RES-LINUX', 'nom': 'Administration Linux',         'vh': 80,  'prof': 'prof_youssef', 'groupes': ['RES-101', 'RES-102']},
    {'code': 'RES-CLOUD', 'nom': 'Cloud & Virtualisation',       'vh': 60,  'prof': 'prof_omar',    'groupes': ['RES-101', 'RES-102']},
    {'code': 'MATH-RES',  'nom': 'Mathématiques Réseaux',        'vh': 60,  'prof': 'prof_nadia',   'groupes': ['RES-101', 'RES-102']},
    # COMPTA — 4 modules
    {'code': 'CPT-GEN',   'nom': 'Comptabilité Générale',        'vh': 120, 'prof': 'prof_fatima',  'groupes': ['COMPTA-101']},
    {'code': 'CPT-ANA',   'nom': 'Comptabilité Analytique',      'vh': 80,  'prof': 'prof_fatima',  'groupes': ['COMPTA-101']},
    {'code': 'CPT-FISC',  'nom': 'Fiscalité Marocaine',          'vh': 80,  'prof': 'prof_fatima',  'groupes': ['COMPTA-101']},
    {'code': 'CPT-GP',    'nom': 'Gestion et Communication',     'vh': 40,  'prof': 'prof_laila',   'groupes': ['COMPTA-101']},
    # MECA — 4 modules
    {'code': 'MEC-AUTO',  'nom': 'Automatisme Industriel',       'vh': 120, 'prof': 'prof_amine',   'groupes': ['MECA-101']},
    {'code': 'MEC-ELEC',  'nom': 'Électronique',                 'vh': 100, 'prof': 'prof_hassan',  'groupes': ['MECA-101']},
    {'code': 'MEC-CAO',   'nom': 'Conception Assistée (CAO)',    'vh': 80,  'prof': 'prof_hassan',  'groupes': ['MECA-101']},
    {'code': 'MEC-MATH',  'nom': 'Mathématiques Appliquées',     'vh': 60,  'prof': 'prof_nadia',   'groupes': ['MECA-101']},
]

# 30 étudiants — 5 per group
ETUDIANTS = [
    # DEV-101 (5)
    {'username': 'etud_adam',     'first_name': 'Adam',     'last_name': 'Benali',    'matricule': 'ETU-2026-001', 'ddn': '2004-03-12', 'groupe': 'DEV-101'},
    {'username': 'etud_imane',    'first_name': 'Imane',    'last_name': 'Tazi',      'matricule': 'ETU-2026-002', 'ddn': '2004-07-25', 'groupe': 'DEV-101'},
    {'username': 'etud_yassir',   'first_name': 'Yassir',   'last_name': 'Moussaoui', 'matricule': 'ETU-2026-003', 'ddn': '2003-11-08', 'groupe': 'DEV-101'},
    {'username': 'etud_hafsa',    'first_name': 'Hafsa',    'last_name': 'Rachidi',   'matricule': 'ETU-2026-004', 'ddn': '2004-01-19', 'groupe': 'DEV-101'},
    {'username': 'etud_badr',     'first_name': 'Badr',     'last_name': 'Idrissi',   'matricule': 'ETU-2026-005', 'ddn': '2003-09-30', 'groupe': 'DEV-101'},
    # DEV-102 (5)
    {'username': 'etud_salma',    'first_name': 'Salma',    'last_name': 'Alami',     'matricule': 'ETU-2026-006', 'ddn': '2004-05-14', 'groupe': 'DEV-102'},
    {'username': 'etud_karim2',   'first_name': 'Karim',    'last_name': 'Bouzidi',   'matricule': 'ETU-2026-007', 'ddn': '2003-12-02', 'groupe': 'DEV-102'},
    {'username': 'etud_nour',     'first_name': 'Nour',     'last_name': 'Cherkaoui', 'matricule': 'ETU-2026-008', 'ddn': '2004-08-21', 'groupe': 'DEV-102'},
    {'username': 'etud_rida',     'first_name': 'Rida',     'last_name': 'El Fassi',  'matricule': 'ETU-2026-009', 'ddn': '2003-06-17', 'groupe': 'DEV-102'},
    {'username': 'etud_sarah2',   'first_name': 'Sarah',    'last_name': 'Lahlou',    'matricule': 'ETU-2026-010', 'ddn': '2004-02-28', 'groupe': 'DEV-102'},
    # RES-101 (5)
    {'username': 'etud_mehdi',    'first_name': 'Mehdi',    'last_name': 'Bensouda',  'matricule': 'ETU-2026-011', 'ddn': '2003-10-05', 'groupe': 'RES-101'},
    {'username': 'etud_samira',   'first_name': 'Samira',   'last_name': 'Kettani',   'matricule': 'ETU-2026-012', 'ddn': '2004-04-11', 'groupe': 'RES-101'},
    {'username': 'etud_anas',     'first_name': 'Anas',     'last_name': 'Sebti',     'matricule': 'ETU-2026-013', 'ddn': '2003-08-23', 'groupe': 'RES-101'},
    {'username': 'etud_widad',    'first_name': 'Widad',    'last_name': 'Tahiri',    'matricule': 'ETU-2026-014', 'ddn': '2004-06-09', 'groupe': 'RES-101'},
    {'username': 'etud_fouad',    'first_name': 'Fouad',    'last_name': 'Benjelloun','matricule': 'ETU-2026-015', 'ddn': '2003-03-27', 'groupe': 'RES-101'},
    # RES-102 (5)
    {'username': 'etud_zineb2',   'first_name': 'Zineb',    'last_name': 'Hamidi',    'matricule': 'ETU-2026-016', 'ddn': '2004-09-16', 'groupe': 'RES-102'},
    {'username': 'etud_tariq',    'first_name': 'Tariq',    'last_name': 'Benkirane', 'matricule': 'ETU-2026-017', 'ddn': '2003-07-04', 'groupe': 'RES-102'},
    {'username': 'etud_loubna',   'first_name': 'Loubna',   'last_name': 'Ouazzani',  'matricule': 'ETU-2026-018', 'ddn': '2004-11-22', 'groupe': 'RES-102'},
    {'username': 'etud_ilias',    'first_name': 'Ilias',    'last_name': 'Benmoussa', 'matricule': 'ETU-2026-019', 'ddn': '2003-05-13', 'groupe': 'RES-102'},
    {'username': 'etud_amina',    'first_name': 'Amina',    'last_name': 'Gharbi',    'matricule': 'ETU-2026-020', 'ddn': '2004-10-07', 'groupe': 'RES-102'},
    # COMPTA-101 (5)
    {'username': 'etud_houda',    'first_name': 'Houda',    'last_name': 'Sekkat',    'matricule': 'ETU-2026-021', 'ddn': '2003-02-18', 'groupe': 'COMPTA-101'},
    {'username': 'etud_khalid',   'first_name': 'Khalid',   'last_name': 'Amrani',    'matricule': 'ETU-2026-022', 'ddn': '2004-12-01', 'groupe': 'COMPTA-101'},
    {'username': 'etud_aicha',    'first_name': 'Aicha',    'last_name': 'Bouhali',   'matricule': 'ETU-2026-023', 'ddn': '2003-04-29', 'groupe': 'COMPTA-101'},
    {'username': 'etud_youssef2', 'first_name': 'Youssef',  'last_name': 'Naciri',    'matricule': 'ETU-2026-024', 'ddn': '2004-07-15', 'groupe': 'COMPTA-101'},
    {'username': 'etud_kenza',    'first_name': 'Kenza',    'last_name': 'Alaoui',    'matricule': 'ETU-2026-025', 'ddn': '2003-09-03', 'groupe': 'COMPTA-101'},
    # MECA-101 (5)
    {'username': 'etud_rachid',   'first_name': 'Rachid',   'last_name': 'Bennani',   'matricule': 'ETU-2026-026', 'ddn': '2003-01-24', 'groupe': 'MECA-101'},
    {'username': 'etud_fatima2',  'first_name': 'Fatima',   'last_name': 'Zouiten',   'matricule': 'ETU-2026-027', 'ddn': '2004-03-08', 'groupe': 'MECA-101'},
    {'username': 'etud_nabil',    'first_name': 'Nabil',    'last_name': 'Chami',     'matricule': 'ETU-2026-028', 'ddn': '2003-06-20', 'groupe': 'MECA-101'},
    {'username': 'etud_hind',     'first_name': 'Hind',     'last_name': 'Berrada',   'matricule': 'ETU-2026-029', 'ddn': '2004-08-14', 'groupe': 'MECA-101'},
    {'username': 'etud_said',     'first_name': 'Said',     'last_name': 'El Idrissi','matricule': 'ETU-2026-030', 'ddn': '2003-11-11', 'groupe': 'MECA-101'},
]

# Sessions: 4 weeks starting from 2026-07-07 (Monday)
SCHEDULE = [
    ('DEV-HTML',  'DEV-101', 0, '08:30', '10:30', 'Salle A1'),
    ('DEV-JS',    'DEV-101', 1, '08:30', '10:30', 'Salle A1'),
    ('DEV-PY',    'DEV-101', 2, '08:30', '10:30', 'Labo Info 1'),
    ('DEV-DB',    'DEV-101', 3, '08:30', '10:30', 'Labo Info 1'),
    ('MATH-DEV',  'DEV-101', 4, '08:30', '10:30', 'Salle A1'),
    ('DEV-HTML',  'DEV-102', 0, '10:45', '12:45', 'Salle A2'),
    ('DEV-JS',    'DEV-102', 1, '10:45', '12:45', 'Salle A2'),
    ('DEV-PY',    'DEV-102', 2, '10:45', '12:45', 'Labo Info 2'),
    ('DEV-DB',    'DEV-102', 3, '10:45', '12:45', 'Labo Info 2'),
    ('MATH-DEV',  'DEV-102', 4, '10:45', '12:45', 'Salle A2'),
    ('RES-CISCO', 'RES-101', 0, '08:30', '10:30', 'Labo Réseau'),
    ('RES-SECU',  'RES-101', 1, '08:30', '10:30', 'Labo Réseau'),
    ('RES-LINUX', 'RES-101', 2, '08:30', '10:30', 'Labo Info 1'),
    ('MATH-RES',  'RES-101', 4, '08:30', '10:30', 'Salle B1'),
    ('RES-CISCO', 'RES-102', 0, '10:45', '12:45', 'Labo Réseau'),
    ('RES-SECU',  'RES-102', 1, '10:45', '12:45', 'Labo Réseau'),
    ('RES-LINUX', 'RES-102', 2, '10:45', '12:45', 'Labo Info 2'),
    ('MATH-RES',  'RES-102', 4, '10:45', '12:45', 'Salle B2'),
    ('CPT-GEN',   'COMPTA-101', 0, '14:00', '16:00', 'Salle C1'),
    ('CPT-ANA',   'COMPTA-101', 2, '14:00', '16:00', 'Salle C1'),
    ('CPT-FISC',  'COMPTA-101', 4, '14:00', '16:00', 'Salle C1'),
    ('MEC-AUTO',  'MECA-101', 0, '08:30', '10:30', 'Atelier Meca'),
    ('MEC-ELEC',  'MECA-101', 2, '08:30', '10:30', 'Labo Elec'),
    ('MEC-MATH',  'MECA-101', 4, '08:30', '10:30', 'Salle D1'),
]

NB_WEEKS = 4


class Command(BaseCommand):
    help = 'Seed the database: 6 groupes, 10 enseignants, 20 cours, 30 étudiants'

    def handle(self, *args, **options):
        with transaction.atomic():
            self._seed_filieres()
            self._seed_groupes()
            self._seed_enseignants()
            self._seed_cours()
            self._seed_etudiants()
            self._seed_sessions()
        self.stdout.write(self.style.SUCCESS(
            '\nSeeding terminé :\n'
            f'  Filières  : {Filiere.objects.count()}\n'
            f'  Groupes   : {Groupe.objects.count()}\n'
            f'  Enseignants: {Enseignant.objects.count()}\n'
            f'  Cours     : {Cours.objects.count()}\n'
            f'  Étudiants : {Etudiant.objects.count()}\n'
            f'  Sessions  : {SessionCours.objects.count()}\n'
        ))

    def _seed_filieres(self):
        self.filiere_map = {}
        for f in FILIERES:
            obj, created = Filiere.objects.get_or_create(
                code=f['code'],
                defaults={'nom': f['nom'], 'duree_annees': f['duree']}
            )
            self.filiere_map[f['code']] = obj
            self.stdout.write(f"  {'[+]' if created else '[=]'} Filière: {obj}")

    def _seed_groupes(self):
        self.groupe_map = {}
        for g in GROUPES:
            obj, created = Groupe.objects.get_or_create(
                nom=g['nom'], annee_scolaire=g['annee'],
                defaults={'filiere': self.filiere_map[g['filiere']], 'effectif_max': 30}
            )
            self.groupe_map[g['nom']] = obj
            self.stdout.write(f"  {'[+]' if created else '[=]'} Groupe: {obj}")

    def _seed_enseignants(self):
        self.ens_map = {}
        for e in ENSEIGNANTS:
            u, created = Utilisateur.objects.get_or_create(
                username=e['username'],
                defaults={
                    'email': e['email'],
                    'first_name': e['first_name'],
                    'last_name': e['last_name'],
                    'role': 'enseignant',
                }
            )
            if created:
                u.set_password('prof1234')
                u.save()
            ens, _ = Enseignant.objects.get_or_create(
                user=u,
                defaults={'specialite': e['specialite'], 'grade': e['grade'], 'cin': e['cin']}
            )
            self.ens_map[e['username']] = ens
            self.stdout.write(f"  {'[+]' if created else '[=]'} Enseignant: {u.get_full_name()}")

    def _seed_cours(self):
        self.cours_map = {}
        for c in COURS:
            ens = self.ens_map[c['prof']]
            obj, created = Cours.objects.get_or_create(
                code_cours=c['code'],
                defaults={'nom': c['nom'], 'volume_horaire': c['vh'], 'enseignant': ens}
            )
            for gnom in c['groupes']:
                obj.groupes.add(self.groupe_map[gnom])
            self.cours_map[c['code']] = obj
            self.stdout.write(f"  {'[+]' if created else '[=]'} Cours: {obj}")

    def _seed_etudiants(self):
        from datetime import date as d
        for e in ETUDIANTS:
            u, created = Utilisateur.objects.get_or_create(
                username=e['username'],
                defaults={
                    'email': f"{e['username']}@etud.gespresence.ma",
                    'first_name': e['first_name'],
                    'last_name': e['last_name'],
                    'role': 'etudiant',
                }
            )
            if created:
                u.set_password('etud1234')
                u.save()
            etud, _ = Etudiant.objects.get_or_create(
                user=u,
                defaults={
                    'matricule': e['matricule'],
                    'date_naissance': d.fromisoformat(e['ddn']),
                    'groupe': self.groupe_map[e['groupe']],
                }
            )
            self.stdout.write(f"  {'[+]' if created else '[=]'} Étudiant: {u.get_full_name()} ({e['groupe']})")

    def _seed_sessions(self):
        start_date = date(2026, 7, 7)  # Monday
        created_count = 0
        for week in range(NB_WEEKS):
            for (code, gnom, day_offset, hd, hf, salle) in SCHEDULE:
                session_date = start_date + timedelta(weeks=week, days=day_offset)
                cours = self.cours_map.get(code)
                groupe = self.groupe_map.get(gnom)
                if not cours or not groupe:
                    continue
                _, created = SessionCours.objects.get_or_create(
                    cours=cours, groupe=groupe,
                    date_session=session_date,
                    heure_debut=time.fromisoformat(hd),
                    defaults={'heure_fin': time.fromisoformat(hf), 'salle': salle}
                )
                if created:
                    created_count += 1
        self.stdout.write(f"  [+] {created_count} sessions créées")
