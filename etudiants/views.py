from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Etudiant, Groupe, Filiere
from presences.models import Presence


@login_required
def etudiant_list(request):
    etudiants = Etudiant.objects.select_related('user', 'groupe__filiere').all()
    groupes = Groupe.objects.all()
    groupe_id = request.GET.get('groupe')
    if groupe_id:
        etudiants = etudiants.filter(groupe_id=groupe_id)
    return render(request, 'etudiants/liste.html', {
        'etudiants': etudiants,
        'groupes': groupes,
        'groupe_selectionne': groupe_id,
    })


@login_required
def etudiant_detail(request, pk):
    etudiant = get_object_or_404(Etudiant.objects.select_related('user', 'groupe__filiere'), pk=pk)
    presences = Presence.objects.filter(etudiant=etudiant).select_related('session__cours').order_by('-session__date_session')[:20]
    return render(request, 'etudiants/detail.html', {
        'etudiant': etudiant,
        'presences': presences,
        'taux': etudiant.get_taux_presence(),
    })
