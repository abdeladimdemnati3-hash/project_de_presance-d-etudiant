from django.db import models
from accounts.models import Etudiant
from cours.models import SessionCours


class Presence(models.Model):
    STATUTS = [
        ('present', 'Présent'),
        ('absent', 'Absent'),
        ('retard', 'En retard'),
        ('justifie', 'Justifié'),
    ]
    statut = models.CharField(max_length=20, choices=STATUTS, default='absent')
    justification = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notif_parent_envoyee = models.BooleanField(default=False)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='presences')
    session = models.ForeignKey(SessionCours, on_delete=models.CASCADE, related_name='presences')

    def __str__(self):
        return f"{self.etudiant} — {self.session.date_session} — {self.get_statut_display()}"

    class Meta:
        verbose_name = "Présence"
        unique_together = ['etudiant', 'session']
        ordering = ['-session__date_session']
