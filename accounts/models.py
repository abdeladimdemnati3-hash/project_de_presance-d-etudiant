from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    ROLES = [
        ('admin', 'Administrateur'),
        ('enseignant', 'Enseignant'),
        ('etudiant', 'Étudiant'),
        ('parent', 'Parent'),
    ]
    role = models.CharField(max_length=20, choices=ROLES, default='etudiant')
    telephone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    @property
    def is_admin_role(self):
        return self.role == 'admin'

    @property
    def is_enseignant_role(self):
        return self.role == 'enseignant'

    @property
    def is_etudiant_role(self):
        return self.role == 'etudiant'

    @property
    def is_parent_role(self):
        return self.role == 'parent'


class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    duree_annees = models.IntegerField(default=2)

    def __str__(self):
        return f"{self.code} — {self.nom}"

    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        ordering = ['nom']


class Groupe(models.Model):
    nom = models.CharField(max_length=50)
    annee_scolaire = models.IntegerField()
    effectif_max = models.IntegerField(default=30)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='groupes')

    def __str__(self):
        return f"{self.nom} ({self.filiere.code} — {self.annee_scolaire})"

    class Meta:
        verbose_name = "Groupe"
        ordering = ['annee_scolaire', 'nom']


class Etudiant(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='etudiant_profile')
    matricule = models.CharField(max_length=20, unique=True)
    date_naissance = models.DateField()
    photo = models.ImageField(upload_to='etudiants/', blank=True, null=True)
    groupe = models.ForeignKey(Groupe, on_delete=models.SET_NULL, null=True, blank=True, related_name='etudiants')

    def __str__(self):
        return f"{self.matricule} — {self.user.get_full_name()}"

    def get_taux_presence(self):
        total = self.presences.count()
        if total == 0:
            return 0
        presents = self.presences.filter(statut='present').count()
        return round((presents / total) * 100, 1)

    class Meta:
        verbose_name = "Étudiant"
        ordering = ['user__last_name', 'user__first_name']


class Enseignant(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='enseignant_profile')
    specialite = models.CharField(max_length=100)
    grade = models.CharField(max_length=50, blank=True)
    cin = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.specialite})"

    class Meta:
        verbose_name = "Enseignant"
        ordering = ['user__last_name']


class Parent(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='parent_profile')
    adresse = models.TextField(blank=True)
    telephone_urgence = models.CharField(max_length=20, blank=True)
    enfants = models.ManyToManyField(Etudiant, related_name='parents', blank=True)

    def __str__(self):
        return f"Parent: {self.user.get_full_name()}"

    class Meta:
        verbose_name = "Parent"


class Administrateur(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='admin_profile')
    departement = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Admin: {self.user.get_full_name()}"

    class Meta:
        verbose_name = "Administrateur"
