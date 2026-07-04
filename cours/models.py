from django.db import models
from accounts.models import Enseignant, Groupe


class Cours(models.Model):
    nom = models.CharField(max_length=100)
    code_cours = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    volume_horaire = models.IntegerField(default=0)
    enseignant = models.ForeignKey(
        Enseignant, on_delete=models.SET_NULL, null=True, blank=True, related_name='cours'
    )
    groupes = models.ManyToManyField(Groupe, related_name='cours', blank=True)

    def __str__(self):
        return f"{self.code_cours} — {self.nom}"

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ['nom']


class SessionCours(models.Model):
    STATUTS = [
        ('planifiee', 'Planifiée'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]
    date_session = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    salle = models.CharField(max_length=50)
    statut = models.CharField(max_length=20, choices=STATUTS, default='planifiee')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='sessions')
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='sessions')

    def __str__(self):
        return f"{self.cours.nom} — {self.date_session} {self.heure_debut} ({self.groupe})"

    def get_taux_presence(self):
        total = self.presences.count()
        if total == 0:
            return 0
        presents = self.presences.filter(statut='present').count()
        return round((presents / total) * 100, 1)

    class Meta:
        verbose_name = "Session de cours"
        verbose_name_plural = "Sessions de cours"
        ordering = ['-date_session', 'heure_debut']
