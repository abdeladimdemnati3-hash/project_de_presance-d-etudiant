from django.contrib import admin
from .models import Cours, SessionCours


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('code_cours', 'nom', 'get_enseignant', 'volume_horaire')
    list_filter = ('groupes__filiere',)
    search_fields = ('code_cours', 'nom')
    filter_horizontal = ('groupes',)

    def get_enseignant(self, obj):
        return obj.enseignant.user.get_full_name() if obj.enseignant else '—'
    get_enseignant.short_description = 'Enseignant'


@admin.register(SessionCours)
class SessionCoursAdmin(admin.ModelAdmin):
    list_display = ('cours', 'groupe', 'date_session', 'heure_debut', 'heure_fin', 'salle', 'statut')
    list_filter = ('statut', 'cours__groupes__filiere', 'date_session')
    date_hierarchy = 'date_session'
    search_fields = ('cours__nom', 'salle')
