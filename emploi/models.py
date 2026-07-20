from django.db import models
from accounts.models import Groupe


class EmploiDuTemps(models.Model):
    groupe = models.ForeignKey(
        Groupe, on_delete=models.CASCADE, related_name='emplois_du_temps'
    )
    titre = models.CharField(max_length=150, blank=True)
    fichier = models.FileField(upload_to='emploi_du_temps/')
    annee_scolaire = models.CharField(max_length=20, default='2025-2026')
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emploi — {self.groupe} ({self.annee_scolaire})"

    class Meta:
        verbose_name = "Emploi du temps"
        verbose_name_plural = "Emplois du temps"
        ordering = ['-date_upload']

