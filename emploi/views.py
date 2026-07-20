from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from accounts.models import Groupe, Etudiant
from .models import EmploiDuTemps


@login_required
def emploi_list(request):
    """All authenticated users can view timetables."""
    user = request.user
    groupes = Groupe.objects.all().prefetch_related('emplois_du_temps')

    # For students: only show their group
    if user.role == 'etudiant':
        try:
            etudiant = user.etudiant
            groupes = Groupe.objects.filter(pk=etudiant.groupe.pk).prefetch_related('emplois_du_temps')
        except Exception:
            groupes = Groupe.objects.none()

    # For parents: show groups of their children
    elif user.role == 'parent':
        try:
            enfants = user.parent.enfants.select_related('groupe')
            groupe_ids = [e.groupe_id for e in enfants if e.groupe]
            groupes = Groupe.objects.filter(pk__in=groupe_ids).prefetch_related('emplois_du_temps')
        except Exception:
            groupes = Groupe.objects.none()

    annee_scolaire = request.GET.get('annee', '')
    groupe_filter = request.GET.get('groupe', '')

    all_groupes = Groupe.objects.all()
    annees = EmploiDuTemps.objects.values_list('annee_scolaire', flat=True).distinct()

    emplois = EmploiDuTemps.objects.select_related('groupe').order_by('-date_upload')
    if annee_scolaire:
        emplois = emplois.filter(annee_scolaire=annee_scolaire)
    if groupe_filter:
        emplois = emplois.filter(groupe_id=groupe_filter)
    if user.role == 'etudiant':
        try:
            emplois = emplois.filter(groupe=user.etudiant.groupe)
        except Exception:
            emplois = emplois.none()
    elif user.role == 'parent':
        try:
            enfants = user.parent.enfants.select_related('groupe')
            groupe_ids = [e.groupe_id for e in enfants if e.groupe]
            emplois = emplois.filter(groupe_id__in=groupe_ids)
        except Exception:
            emplois = emplois.none()

    return render(request, 'emploi/liste.html', {
        'emplois': emplois,
        'all_groupes': all_groupes,
        'annees': annees,
        'annee_filter': annee_scolaire,
        'groupe_filter': groupe_filter,
    })


@login_required
@role_required('admin')
def emploi_upload(request):
    """Only admin can upload a timetable."""
    groupes = Groupe.objects.all()
    if request.method == 'POST':
        groupe_id = request.POST.get('groupe')
        titre = request.POST.get('titre', '').strip()
        annee_scolaire = request.POST.get('annee_scolaire', '2025-2026').strip()
        fichier = request.FILES.get('fichier')

        if not groupe_id or not fichier:
            messages.error(request, "Veuillez sélectionner un groupe et un fichier.")
        else:
            groupe = get_object_or_404(Groupe, pk=groupe_id)
            EmploiDuTemps.objects.create(
                groupe=groupe,
                titre=titre or f"Emploi du temps — {groupe.nom}",
                fichier=fichier,
                annee_scolaire=annee_scolaire,
            )
            messages.success(request, "Emploi du temps uploadé avec succès.")
            return redirect('emploi_list')

    return render(request, 'emploi/upload.html', {'groupes': groupes})


@login_required
@role_required('admin')
def emploi_delete(request, pk):
    """Only admin can delete a timetable."""
    emploi = get_object_or_404(EmploiDuTemps, pk=pk)
    if request.method == 'POST':
        emploi.fichier.delete(save=False)
        emploi.delete()
        messages.success(request, "Emploi du temps supprimé.")
    return redirect('emploi_list')

