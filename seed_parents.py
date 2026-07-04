import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gespresence.settings')
django.setup()

from django.db import transaction
from accounts.models import Utilisateur, Etudiant, Parent

PRENOMS = ['Hassan','Rachid','Fatima','Omar','Khadija','Mustapha','Said','Latifa',
           'Brahim','Nour','Ahmed','Karima','Youssef','Samira','Abderahim','Zineb',
           'Driss','Meryem','Khalid','Soumia','Fouad','Hajar','Nadia','Rachida',
           'Aziz','Ilham','Tarik','Naima','Samir','Fatna','Hicham','Aicha',
           'Abdelkrim','Rajae','Noureddine']

NOMS = ['Alami','Benaissa','Chraibi','Douiri','Ennaji','Fahim','Ghali','Hamidi',
        'Idrissi','Jalil','Amrani','Kadiri','Lahlou','Mansouri','Naciri','Ouali',
        'Rifai','Saidi','Tahiri','Uali','Wazzani','Slaoui','Yacoubi','Zahri',
        'Abdi','Belkadi','Chakiri','Benali','Daoudi','Elouafi','Farsi','Ghallab',
        'Hajji','Kabbaj','Lamrani']

etudiants = list(
    Etudiant.objects.filter(parents__isnull=True)
    .distinct().select_related('user')
)

print(f"Students without parents: {len(etudiants)}")
created = 0

with transaction.atomic():
    for i, etudiant in enumerate(etudiants):
        prenom   = PRENOMS[i % len(PRENOMS)]
        nom      = NOMS[i % len(NOMS)]
        slug     = etudiant.matricule.lower().replace('-', '').replace(' ', '')[:15]
        username = 'par_' + slug
        email    = username + '@gespresence.ma'

        if not Utilisateur.objects.filter(username=username).exists():
            u = Utilisateur.objects.create_user(
                username=username, email=email, password='parent1234',
                first_name=prenom, last_name=nom, role='parent',
                telephone='066100' + str(i + 1).zfill(4),
            )
            parent = Parent.objects.create(
                user=u,
                telephone_urgence='066100' + str(i + 1).zfill(4),
                adresse='Casablanca, Maroc',
            )
        else:
            u = Utilisateur.objects.get(username=username)
            parent, _ = Parent.objects.get_or_create(user=u)

        parent.enfants.add(etudiant)
        created += 1
        print(f"  [+] {prenom} {nom} ({username}) -> {etudiant.user.get_full_name()}")

print(f"\nTotal: {created} parents created.")
print("Password for all parents: parent1234")
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gespresence.settings')
django.setup()

from django.db import transaction
from accounts.models import Utilisateur, Etudiant, Parent

PARENTS_DATA = [
    # (etudiant_matricule, parent_username, first_name, last_name, telephone)
    ('STU-2026-001', 'parent_alami',    'Hassan',    'Alami',    '0661000001'),
    ('DEV-101-01',   'parent_benaissa', 'Rachid',    'Benaissa', '0661000002'),
    ('DEV-101-02',   'parent_alami2',   'Fatima',    'Alami',    '0661000003'),
    ('DEV-101-03',   'parent_chraibi',  'Omar',      'Chraibi',  '0661000004'),
    ('DEV-101-04',   'parent_douiri',   'Khadija',   'Douiri',   '0661000005'),
    ('DEV-101-05',   'parent_ennaji',   'Mustapha',  'Ennaji',   '0661000006'),
    ('DEV-102-01',   'parent_fahim',    'Said',      'Fahim',    '0661000007'),
    ('DEV-102-02',   'parent_ghali',    'Latifa',    'Ghali',    '0661000008'),
    ('DEV-102-03',   'parent_hamidi',   'Brahim',    'Hamidi',   '0661000009'),
    ('DEV-102-04',   'parent_idrissi',  'Nour',      'Idrissi',  '0661000010'),
    ('DEV-102-05',   'parent_jalil',    'Ahmed',     'Jalil',    '0661000011'),
    ('DEV-102-06',   'parent_amrani',   'Karima',    'Amrani',   '0661000012'),
    ('RES-101-01',   'parent_kadiri',   'Youssef',   'Kadiri',   '0661000013'),
    ('RES-101-02',   'parent_lahlou',   'Samira',    'Lahlou',   '0661000014'),
    ('RES-101-03',   'parent_mansouri', 'Abderahim', 'Mansouri', '0661000015'),
    ('RES-101-04',   'parent_naciri',   'Zineb',     'Naciri',   '0661000016'),
    ('RES-101-05',   'parent_ouali',    'Driss',     'Ouali',    '0661000017'),
    ('RES-102-01',   'parent_rifai',    'Meryem',    'Rifai',    '0661000018'),
    ('RES-102-02',   'parent_saidi',    'Khalid',    'Saidi',    '0661000019'),
    ('RES-102-03',   'parent_tahiri',   'Soumia',    'Tahiri',   '0661000020'),
    ('RES-102-04',   'parent_uali',     'Fouad',     'Uali',     '0661000021'),
    ('RES-102-05',   'parent_wazzani',  'Hajar',     'Wazzani',  '0661000022'),
    ('COM-101-01',   'parent_xalil',    'Nadia',     'Xalil',    '0661000023'),
    ('COM-101-02',   'parent_yacoubi',  'Rachida',   'Yacoubi',  '0661000024'),
    ('COM-101-03',   'parent_zahri',    'Aziz',      'Zahri',    '0661000025'),
    ('COM-101-04',   'parent_abdi',     'Ilham',     'Abdi',     '0661000026'),
    ('COM-101-05',   'parent_belkadi',  'Tarik',     'Belkadi',  '0661000027'),
    ('COM-101-06',   'parent_chakiri',  'Naima',     'Chakiri',  '0661000028'),
    ('MEC-101-01',   'parent_aziz',     'Samir',     'Aziz',     '0661000029'),
    ('MEC-101-02',   'parent_benali',   'Fatna',     'Benali',   '0661000030'),
    ('MEC-101-03',   'parent_chakir',   'Hicham',    'Chakir',   '0661000031'),
    ('MEC-101-04',   'parent_daoudi',   'Aicha',     'Daoudi',   '0661000032'),
    ('MEC-101-05',   'parent_elouafi',  'Abdelkrim', 'Elouafi',  '0661000033'),
    ('MEC-101-06',   'parent_farsi',    'Rajae',     'Farsi',    '0661000034'),
    ('MEC-101-07',   'parent_ghallab',  'Noureddine','Ghallab',  '0661000035'),
]

created_count = 0

with transaction.atomic():
    for (matricule, username, first, last, tel) in PARENTS_DATA:
        # Find the student
        try:
            etudiant = Etudiant.objects.get(matricule=matricule)
        except Etudiant.DoesNotExist:
            # Try to find any student not yet assigned a parent
            existing_parent_etudiants = Parent.objects.values_list('enfants__id', flat=True)
            etudiant = Etudiant.objects.exclude(id__in=existing_parent_etudiants).first()
            if not etudiant:
                print(f"  Skipping {username} - no student available")
                continue

        # Skip if parent already exists
        if Utilisateur.objects.filter(username=username).exists():
            u = Utilisateur.objects.get(username=username)
            parent = Parent.objects.get(user=u)
            parent.enfants.add(etudiant)
            print(f"  [=] {username} already exists, linked to {etudiant.matricule}")
            continue

        # Create user
        u = Utilisateur.objects.create_user(
            username=username,
            email=f"{username}@gespresence.ma",
            password='parent1234',
            first_name=first,
            last_name=last,
            role='parent',
            telephone=tel,
        )
        # Create parent profile
        parent = Parent.objects.create(
            user=u,
            telephone_urgence=tel,
            adresse='Casablanca, Maroc',
        )
        parent.enfants.add(etudiant)
        created_count += 1
        print(f"  [+] {username} ({first} {last}) -> enfant: {etudiant.user.get_full_name()}")

print(f"\n{created_count} parents created.")
print("Password for all parents: parent1234")
