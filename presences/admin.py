from django.contrib import admin
from .models import Presence


@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ('get_etudiant', 'get_session', 'statut', 'notif_parent_envoyee', 'created_at')
    list_filter = ('statut', 'session__date_session', 'notif_parent_envoyee')
    search_fields = ('etudiant__user__last_name', 'etudiant__matricule')
    date_hierarchy = 'created_at'

    def get_etudiant(self, obj):
        return str(obj.etudiant)
    get_etudiant.short_description = 'Étudiant'

    def get_session(self, obj):
        return f"{obj.session.cours.nom} — {obj.session.date_session}"
    get_session.short_description = 'Session'
