from django.contrib import admin
from .models import EmploiDuTemps

@admin.register(EmploiDuTemps)
class EmploiDuTempsAdmin(admin.ModelAdmin):
    list_display = ['groupe', 'titre', 'annee_scolaire', 'date_upload']
    list_filter = ['groupe', 'annee_scolaire']

