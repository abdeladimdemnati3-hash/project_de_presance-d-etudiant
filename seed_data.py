"""
Seed script: creates filières, groupes, enseignants, cours, and sessions (emploi du temps).
Run: .\venv\Scripts\python.exe seed_data.py
"""
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gespresence.settings')
django.setup()

from django.db import transaction
from accounts.models import Utilisateur, Enseignant, Filiere, Groupe, Etudiant
from cours.models import Cours, SessionCours
from datetime import date, time, timedelta

# ─────────────────────────────────────────────
# 1. FILIÈRES
# ─────────────────────────────────────────────
FILIERES = [
    {'code': 'DEV',  'nom': 'Développement Digital',          'duree': 2},
    {'code': 'RESEAU','nom': 'Réseaux Informatiques',          'duree': 2},
    {'code': 'COMPTA','nom': 'Technicien Comptable',            'duree': 2},
    {'code': 'MECA',  'nom': 'Technicien en Mécatronique',      'duree': 2},
]

# ─────────────────────────────────────────────
# 2. GROUPES  (2 groupes par filière)
# ─────────────────────────────────────────────
GROUPES = [
    {'nom': 'DEV-101',    'filiere': 'DEV',    'annee': 2026},
    {'nom': 'DEV-102',    'filiere': 'DEV',    'annee': 2026},
    {'nom': 'RES-101',    'filiere': 'RESEAU', 'annee': 2026},
    {'nom': 'RES-102',    'filiere': 'RESEAU', 'annee': 2026},
    {'nom': 'COMPTA-101', 'filiere': 'COMPTA', 'annee': 2026},
    {'nom': 'MECA-101',   'filiere': 'MECA',   'annee': 2026},
]

# ─────────────────────────────────────────────
# 3. ENSEIGNANTS
# ─────────────────────────────────────────────
ENSEIGNANTS = [
    {'username': 'prof_karim',   'first_name': 'Karim',   'last_name': 'Bennani',   'email': 'karim@gespresence.ma',   'cin': 'BK100001', 'specialite': 'Développement Web',          'grade': 'Formateur Principal'},
    {'username': 'prof_sara',    'first_name': 'Sara',    'last_name': 'Alaoui',    'email': 'sara@gespresence.ma',    'cin': 'BK100002', 'specialite': 'Base de données & Python',   'grade': 'Formateur'},
    {'username': 'prof_youssef', 'first_name': 'Youssef', 'last_name': 'Idrissi',   'email': 'youssef@gespresence.ma', 'cin': 'BK100003', 'specialite': 'Réseaux & Cybersécurité',   'grade': 'Formateur Principal'},
    {'username': 'prof_fatima',  'first_name': 'Fatima',  'last_name': 'Zahra',     'email': 'fatima@gespresence.ma',  'cin': 'BK100004', 'specialite': 'Comptabilité & Finance',    'grade': 'Formateur'},
    {'username': 'prof_amine',   'first_name': 'Amine',   'last_name': 'Tazi',      'email': 'amine@gespresence.ma',   'cin': 'BK100005', 'specialite': 'Mécatronique & Automatisme','grade': 'Formateur'},
    {'username': 'prof_nadia',   'first_name': 'Nadia',   'last_name': 'Chraibi',   'email': 'nadia@gespresence.ma',   'cin': 'BK100006', 'specialite': 'Mathématiques & Algorithmique','grade': 'Formateur'},
]

# ─────────────────────────────────────────────
# 4. COURS  (module → enseignant → groupes)
# ─────────────────────────────────────────────
COURS = [
    # DEV modules
    {'code': 'DEV-HTML',  'nom': 'HTML/CSS & Bootstrap',        'vh': 80,  'prof': 'prof_karim',   'groupes': ['DEV-101', 'DEV-102']},
    {'code': 'DEV-JS',    'nom': 'JavaScript & React',          'vh': 100, 'prof': 'prof_karim',   'groupes': ['DEV-101', 'DEV-102']},
    {'code': 'DEV-PY',    'nom': 'Python & Django',             'vh': 120, 'prof': 'prof_sara',    'groupes': ['DEV-101', 'DEV-102']},
    {'code': 'DEV-DB',    'nom': 'Base de Données MySQL',        'vh': 80,  'prof': 'prof_sara',    'groupes': ['DEV-101', 'DEV-102']},
    {'code': 'MATH-DEV',  'nom': 'Mathématiques pour Dev',      'vh': 60,  'prof': 'prof_nadia',   'groupes': ['DEV-101', 'DEV-102']},
    # RESEAU modules
    {'code': 'RES-CISCO', 'nom': 'Cisco CCNA',                  'vh': 120, 'prof': 'prof_youssef', 'groupes': ['RES-101', 'RES-102']},
    {'code': 'RES-SECU',  'nom': 'Cybersécurité & Ethical Hack','vh': 100, 'prof': 'prof_youssef', 'groupes': ['RES-101', 'RES-102']},
    {'code': 'RES-LINUX', 'nom': 'Administration Linux',        'vh': 80,  'prof': 'prof_youssef', 'groupes': ['RES-101', 'RES-102']},
    {'code': 'MATH-RES',  'nom': 'Mathématiques Réseaux',       'vh': 60,  'prof': 'prof_nadia',   'groupes': ['RES-101', 'RES-102']},
    # COMPTA modules
    {'code': 'CPT-GEN',   'nom': 'Comptabilité Générale',       'vh': 120, 'prof': 'prof_fatima',  'groupes': ['COMPTA-101']},
    {'code': 'CPT-ANA',   'nom': 'Comptabilité Analytique',     'vh': 80,  'prof': 'prof_fatima',  'groupes': ['COMPTA-101']},
    {'code': 'CPT-FISC',  'nom': 'Fiscalité Marocaine',         'vh': 80,  'prof': 'prof_fatima',  'groupes': ['COMPTA-101']},
    # MECA modules
    {'code': 'MEC-AUTO',  'nom': 'Automatisme Industriel',      'vh': 120, 'prof': 'prof_amine',   'groupes': ['MECA-101']},
    {'code': 'MEC-ELEC',  'nom': 'Électronique',                'vh': 100, 'prof': 'prof_amine',   'groupes': ['MECA-101']},
    {'code': 'MEC-MATH',  'nom': 'Mathématiques Appliquées',    'vh': 60,  'prof': 'prof_nadia',   'groupes': ['MECA-101']},
]

# ─────────────────────────────────────────────
# 5. EMPLOI DU TEMPS  (sessions sur 4 semaines)
# start_date = lundi 07/07/2026
# ─────────────────────────────────────────────
# Format: cours_code, groupe, day_offset(0=Mon..4=Fri), heure_debut, heure_fin, salle
SCHEDULE = [
    # DEV-101
    ('DEV-HTML', 'DEV-101', 0, '08:30', '10:30', 'Salle A1'),
    ('DEV-JS',   'DEV-101', 1, '08:30', '10:30', 'Salle A1'),
    ('DEV-PY',   'DEV-101', 2, '08:30', '10:30', 'Labo Info 1'),
    ('DEV-DB',   'DEV-101', 3, '08:30', '10:30', 'Labo Info 1'),
    ('MATH-DEV', 'DEV-101', 4, '08:30', '10:30', 'Salle A1'),
    # DEV-102
    ('DEV-HTML', 'DEV-102', 0, '10:45', '12:45', 'Salle A2'),
    ('DEV-JS',   'DEV-102', 1, '10:45', '12:45', 'Salle A2'),
    ('DEV-PY',   'DEV-102', 2, '10:45', '12:45', 'Labo Info 2'),
    ('DEV-DB',   'DEV-102', 3, '10:45', '12:45', 'Labo Info 2'),
    ('MATH-DEV', 'DEV-102', 4, '10:45', '12:45', 'Salle A2'),
    # RES-101
    ('RES-CISCO', 'RES-101', 0, '08:30', '10:30', 'Labo Réseau'),
    ('RES-SECU',  'RES-101', 1, '08:30', '10:30', 'Labo Réseau'),
    ('RES-LINUX', 'RES-101', 2, '08:30', '10:30', 'Labo Info 1'),
    ('MATH-RES',  'RES-101', 4, '08:30', '10:30', 'Salle B1'),
    # RES-102
    ('RES-CISCO', 'RES-102', 0, '10:45', '12:45', 'Labo Réseau'),
    ('RES-SECU',  'RES-102', 1, '10:45', '12:45', 'Labo Réseau'),
    ('RES-LINUX', 'RES-102', 2, '10:45', '12:45', 'Labo Info 2'),
    ('MATH-RES',  'RES-102', 4, '10:45', '12:45', 'Salle B2'),
    # COMPTA-101
    ('CPT-GEN',  'COMPTA-101', 0, '14:00', '16:00', 'Salle C1'),
    ('CPT-ANA',  'COMPTA-101', 2, '14:00', '16:00', 'Salle C1'),
    ('CPT-FISC', 'COMPTA-101', 4, '14:00', '16:00', 'Salle C1'),
    # MECA-101
    ('MEC-AUTO', 'MECA-101', 0, '08:30', '10:30', 'Atelier Meca'),
    ('MEC-ELEC', 'MECA-101', 2, '08:30', '10:30', 'Labo Elec'),
    ('MEC-MATH', 'MECA-101', 4, '08:30', '10:30', 'Salle D1'),
]

NB_WEEKS = 4  # Generate sessions for 4 weeks

# ─────────────────────────────────────────────
with transaction.atomic():
    # 1. Filières
    filiere_map = {}
    for f in FILIERES:
        obj, created = Filiere.objects.get_or_create(
            code=f['code'],
            defaults={'nom': f['nom'], 'duree_annees': f['duree']}
        )
        filiere_map[f['code']] = obj
        print(f"  {'[+]' if created else '[=]'} Filière: {obj}")

    # 2. Groupes
    groupe_map = {}
    for g in GROUPES:
        obj, created = Groupe.objects.get_or_create(
            nom=g['nom'], annee_scolaire=g['annee'],
            defaults={'filiere': filiere_map[g['filiere']], 'effectif_max': 30}
        )
        groupe_map[g['nom']] = obj
        print(f"  {'[+]' if created else '[=]'} Groupe: {obj}")

    # 3. Enseignants
    ens_map = {}
    for e in ENSEIGNANTS:
        if Utilisateur.objects.filter(username=e['username']).exists():
            u = Utilisateur.objects.get(username=e['username'])
            print(f"  [=] Enseignant existant: {u.get_full_name()}")
        else:
            u = Utilisateur.objects.create_user(
                username=e['username'], email=e['email'],
                password='prof1234',
                first_name=e['first_name'], last_name=e['last_name'],
                role='enseignant'
            )
            print(f"  [+] Enseignant créé: {u.get_full_name()} / prof1234")

        ens, _ = Enseignant.objects.get_or_create(
            user=u,
            defaults={'specialite': e['specialite'], 'grade': e['grade'], 'cin': e['cin']}
        )
        ens_map[e['username']] = ens

    # 4. Cours
    cours_map = {}
    for c in COURS:
        ens = ens_map[c['prof']]
        obj, created = Cours.objects.get_or_create(
            code_cours=c['code'],
            defaults={'nom': c['nom'], 'volume_horaire': c['vh'], 'enseignant': ens}
        )
        for gnom in c['groupes']:
            obj.groupes.add(groupe_map[gnom])
        cours_map[c['code']] = obj
        print(f"  {'[+]' if created else '[=]'} Cours: {obj} → {ens.user.get_full_name()}")

    # 5. Sessions (emploi du temps)
    start = date(2026, 7, 7)  # Monday
    sessions_created = 0
    for week in range(NB_WEEKS):
        for (cours_code, groupe_nom, day_off, h_start, h_end, salle) in SCHEDULE:
            session_date = start + timedelta(weeks=week, days=day_off)
            hd = time(int(h_start.split(':')[0]), int(h_start.split(':')[1]))
            hf = time(int(h_end.split(':')[0]),   int(h_end.split(':')[1]))
            _, created = SessionCours.objects.get_or_create(
                cours=cours_map[cours_code],
                groupe=groupe_map[groupe_nom],
                date_session=session_date,
                heure_debut=hd,
                defaults={'heure_fin': hf, 'salle': salle, 'statut': 'planifiee'}
            )
            if created:
                sessions_created += 1

    print(f"\n  [+] {sessions_created} sessions créées (emploi du temps 4 semaines)")

print("\n========================================")
print("Données créées avec succès !")
print("========================================")
print("Mot de passe de tous les professeurs : prof1234")
print("")
print("Comptes professeurs :")
for e in ENSEIGNANTS:
    print(f"  {e['username']:20} | {e['first_name']} {e['last_name']:12} | {e['specialite']}")
print("")
print("Filières et groupes :")
for g in GROUPES:
    print(f"  {g['nom']:15} → Filière {g['filiere']}")
