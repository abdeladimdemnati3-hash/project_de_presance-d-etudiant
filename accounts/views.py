from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from .models import Etudiant, Enseignant, Filiere, Groupe
from cours.models import Cours, SessionCours
from presences.models import Presence
from notifications.models import Notification
from django.utils import timezone


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    role = request.user.role
    context = {}

    if role == 'admin':
        context = {
            'nb_etudiants': Etudiant.objects.count(),
            'nb_enseignants': Enseignant.objects.count(),
            'nb_cours': Cours.objects.count(),
            'nb_absences_today': Presence.objects.filter(
                statut='absent',
                session__date_session=timezone.localdate()
            ).count(),
            'dernieres_sessions': SessionCours.objects.select_related(
                'cours', 'groupe'
            ).order_by('-date_session')[:5],
        }
        template = 'dashboard_admin.html'

    elif role == 'enseignant':
        from .models import Enseignant as E
        try:
            ens = request.user.enseignant_profile
            sessions_today = SessionCours.objects.filter(
                cours__enseignant=ens,
                date_session=timezone.localdate()
            ).select_related('cours', 'groupe')
            context = {
                'sessions_today': sessions_today,
                'nb_cours': ens.cours.count(),
            }
        except Exception:
            pass
        template = 'dashboard_enseignant.html'

    elif role == 'etudiant':
        try:
            etudiant = request.user.etudiant_profile
            context = {
                'taux': etudiant.get_taux_presence(),
                'nb_absences': etudiant.presences.filter(statut='absent').count(),
                'nb_presents': etudiant.presences.filter(statut='present').count(),
            }
        except Exception:
            pass
        template = 'dashboard_etudiant.html'

    elif role == 'parent':
        try:
            parent = request.user.parent_profile
            context = {
                'enfants': parent.enfants.select_related('user', 'groupe').all(),
                'nb_notifs': Notification.objects.filter(parent=parent, lu=False).count(),
            }
        except Exception:
            pass
        template = 'dashboard_parent.html'

    else:
        template = 'dashboard_admin.html'

    return render(request, template, context)


@login_required
def profil_view(request):
    return render(request, 'accounts/profil.html', {'user': request.user})
