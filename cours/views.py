from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cours, SessionCours
from accounts.models import Groupe


@login_required
def cours_list(request):
    cours_qs = Cours.objects.select_related('enseignant__user').prefetch_related('groupes').all()
    return render(request, 'cours/liste.html', {'cours_list': cours_qs})


@login_required
def cours_detail(request, pk):
    cours = get_object_or_404(Cours, pk=pk)
    sessions = cours.sessions.select_related('groupe').order_by('-date_session')
    return render(request, 'cours/detail.html', {'cours': cours, 'sessions': sessions})


@login_required
def session_list(request, cours_pk):
    cours = get_object_or_404(Cours, pk=cours_pk)
    sessions = cours.sessions.select_related('groupe').order_by('-date_session')
    return render(request, 'cours/sessions.html', {'cours': cours, 'sessions': sessions})
