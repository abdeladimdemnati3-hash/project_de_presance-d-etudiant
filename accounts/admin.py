from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Etudiant, Enseignant, Parent, Administrateur, Filiere, Groupe


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Supplémentaires', {'fields': ('role', 'telephone')}),
    )


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'duree_annees')
    search_fields = ('code', 'nom')


@admin.register(Groupe)
class GroupeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'filiere', 'annee_scolaire', 'effectif_max')
    list_filter = ('filiere', 'annee_scolaire')


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'get_nom', 'groupe', 'get_taux_presence')
    list_filter = ('groupe__filiere', 'groupe')
    search_fields = ('matricule', 'user__first_name', 'user__last_name')

    def get_nom(self, obj):
        return obj.user.get_full_name()
    get_nom.short_description = 'Nom complet'

    def get_taux_presence(self, obj):
        return f"{obj.get_taux_presence()}%"
    get_taux_presence.short_description = 'Taux présence'


@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('cin', 'get_nom', 'specialite', 'grade')
    search_fields = ('cin', 'user__first_name', 'user__last_name')

    def get_nom(self, obj):
        return obj.user.get_full_name()
    get_nom.short_description = 'Nom complet'


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('get_nom', 'telephone_urgence')
    filter_horizontal = ('enfants',)

    def get_nom(self, obj):
        return obj.user.get_full_name()
    get_nom.short_description = 'Nom complet'


admin.site.register(Administrateur)
