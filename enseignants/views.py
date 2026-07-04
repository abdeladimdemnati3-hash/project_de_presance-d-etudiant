from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Enseignant
from cours.models import SessionCours
from django.utils import timezone


@login_required
def enseignant_list(request):
    enseignants = Enseignant.objects.select_related('user').all()
    return render(request, 'enseignants/liste.html', {'enseignants': enseignants})


@login_required
def enseignant_detail(request, pk):
    enseignant = get_object_or_404(Enseignant.objects.select_related('user'), pk=pk)
    cours = enseignant.cours.prefetch_related('groupes').all()
    return render(request, 'enseignants/detail.html', {'enseignant': enseignant, 'cours': cours})


@login_required
def mes_sessions(request):
    enseignant = get_object_or_404(Enseignant, user=request.user)
    sessions = SessionCours.objects.filter(
        cours__enseignant=enseignant
    ).select_related('cours', 'groupe').order_by('date_session', 'heure_debut')
    return render(request, 'enseignants/mes_sessions.html', {'sessions': sessions})
