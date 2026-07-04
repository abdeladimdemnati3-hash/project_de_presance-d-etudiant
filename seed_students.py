"""
Seed: create students per group + sample presence records for all sessions.
"""
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gespresence.settings')
django.setup()

from django.db import transaction
from accounts.models import Utilisateur, Etudiant, Groupe
from cours.models import SessionCours
from presences.models import Presence
from datetime import date
import random

STUDENTS = {
    'DEV-101':    [('Ahmed','Benaissa','2004-03-12'),('Sara','Alami','2004-07-25'),
                   ('Karim','Zidane','2003-11-05'),('Fatima','Chraibi','2004-01-18'),
                   ('Yassine','Benali','2004-05-30'),('Nora','Tahiri','2003-09-14')],
    'DEV-102':    [('Omar','Hajji','2004-02-20'),('Layla','Idrissi','2003-12-08'),
                   ('Amine','Fennich','2004-06-17'),('Hind','Moussaoui','2003-10-22'),
                   ('Rachid','Berrada','2004-04-09'),('Zineb','Amrani','2004-08-03')],
    'RES-101':    [('Mehdi','Ouali','2003-05-16'),('Soukaina','Fassi','2004-09-28'),
                   ('Bilal','Naciri','2003-07-11'),('Hajar','Tazi','2004-03-24'),
                   ('Adil','Cherkaoui','2003-11-30'),('Rania','Lamrani','2004-06-05')],
    'RES-102':    [('Hamza','Benkirane','2004-01-07'),('Meriem','Qadiri','2003-08-19'),
                   ('Saad','Bouhaja','2004-07-14'),('Kawtar','Mekki','2003-04-26'),
                   ('Issam','Radi','2004-10-02'),('Samira','Hajjam','2003-12-15')],
    'COMPTA-101': [('Khalid','Bensouda','2004-02-28'),('Asmaa','Rifai','2003-06-10'),
                   ('Tariq','Filali','2004-09-03'),('Nawal','Sekkat','2003-03-17'),
                   ('Zakaria','Mansouri','2004-05-21')],
    'MECA-101':   [('Nabil','Aziz','2003-08-07'),('Ghita','Bousfiha','2004-11-19'),
                   ('Iliyas','Kasmi','2003-05-04'),('Douaa','Rhazi','2004-02-13'),
                   ('Walid','Ennaji','2003-10-28')],
}

random.seed(42)
created_etu = 0

with transaction.atomic():
    # --- 1. Create students ---
    for groupe_nom, eleves in STUDENTS.items():
        try:
            groupe = Groupe.objects.get(nom=groupe_nom)
        except Groupe.DoesNotExist:
            continue
        fc = groupe.filiere.code.lower()[:3]
        for i, (prenom, nom, dob) in enumerate(eleves, 1):
            uname = f"etu_{fc}_{groupe_nom[-3:].lower()}_{i:02d}"
            if Utilisateur.objects.filter(username=uname).exists():
                continue
            u = Utilisateur.objects.create_user(
                username=uname, email=f"{uname}@gespresence.ma",
                password="etu1234", first_name=prenom, last_name=nom,
                role='etudiant',
            )
            Etudiant.objects.create(
                user=u, matricule=f"{fc.upper()}-{groupe_nom[-3:]}-{i:02d}",
                date_naissance=date.fromisoformat(dob), groupe=groupe,
            )
            created_etu += 1

    print(f"[+] {created_etu} etudiants crees")

    # --- 2. Create presence records for past sessions ---
    past_sessions = SessionCours.objects.filter(
        statut='planifiee'
    ).select_related('groupe').prefetch_related('groupe__etudiants')

    created_pres = 0
    statuts_pool = ['present', 'present', 'present', 'present', 'absent', 'retard']

    for session in past_sessions:
        etudiants = list(session.groupe.etudiants.all())
        if not etudiants:
            continue
        for etudiant in etudiants:
            if Presence.objects.filter(etudiant=etudiant, session=session).exists():
                continue
            Presence.objects.create(
                etudiant=etudiant,
                session=session,
                statut=random.choice(statuts_pool),
            )
            created_pres += 1

    print(f"[+] {created_pres} presences creees")

# --- 3. Summary ---
print("\nGroupe              | Etudiants | Sessions")
print("-" * 45)
for g in Groupe.objects.select_related('filiere').all().order_by('nom'):
    nb_etu = g.etudiants.count()
    nb_ses = SessionCours.objects.filter(groupe=g).count()
    print(f"{g.nom:20}| {nb_etu:9} | {nb_ses}")

print("\nMot de passe etudiants: etu1234")
print("Format username: etu_<filiere>_<groupe>_<n>  ex: etu_dev_101_01")
