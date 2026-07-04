from django.db import models
from accounts.models import Parent


class Notification(models.Model):
    TYPES = [
        ('absence', 'Absence'),
        ('retard', 'Retard'),
        ('rapport', 'Rapport'),
        ('info', 'Information'),
    ]
    message = models.TextField()
    type = models.CharField(max_length=20, choices=TYPES, default='info')
    lu = models.BooleanField(default=False)
    envoyee_le = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f"[{self.get_type_display()}] {self.parent} — {self.envoyee_le.date()}"

    class Meta:
        verbose_name = "Notification"
        ordering = ['-envoyee_le']
