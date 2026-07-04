from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Presence
from cours.models import SessionCours
from accounts.models import Etudiant, Enseignant
from notifications.models import Notification
from accounts.models import Parent


@login_required
def feuille_presence(request, session_pk):
    session = get_object_or_404(
        SessionCours.objects.select_related('cours__enseignant__user', 'groupe'),
        pk=session_pk
    )
    etudiants = Etudiant.objects.filter(groupe=session.groupe).select_related('user')
    presences_existantes = {
        p.etudiant_id: p for p in Presence.objects.filter(session=session)
    }

    if request.method == 'POST':
        with transaction.atomic():
            for etudiant in etudiants:
                statut = request.POST.get(f'statut_{etudiant.pk}', 'absent')
                justification = request.POST.get(f'justif_{etudiant.pk}', '')
                presence, created = Presence.objects.update_or_create(
                    etudiant=etudiant,
                    session=session,
                    defaults={'statut': statut, 'justification': justification},
                )
                # Send notification to parent if absent/retard
                if statut in ('absent', 'retard') and not presence.notif_parent_envoyee:
                    for parent in Parent.objects.filter(enfants=etudiant):
                        Notification.objects.create(
                            parent=parent,
                            type=statut,
                            message=(
                                f"{etudiant.user.get_full_name()} était {dict(Presence.STATUTS)[statut].lower()} "
                                f"lors du cours {session.cours.nom} le {session.date_session}."
                            )
                        )
                    presence.notif_parent_envoyee = True
                    presence.save(update_fields=['notif_parent_envoyee'])

        session.statut = 'terminee'
        session.save(update_fields=['statut'])
        messages.success(request, 'Présences enregistrées avec succès.')
        return redirect('session_list', cours_pk=session.cours_id)

    return render(request, 'presences/feuille_presence.html', {
        'session': session,
        'etudiants': etudiants,
        'presences': presences_existantes,
    })


@login_required
def historique_presence(request):
    user = request.user
    if user.role == 'etudiant':
        etudiant = get_object_or_404(Etudiant, user=user)
        presences = Presence.objects.filter(etudiant=etudiant).select_related('session__cours').order_by('-session__date_session')
        return render(request, 'presences/historique.html', {
            'presences': presences,
            'etudiant': etudiant,
            'taux': etudiant.get_taux_presence()
        })
    presences = Presence.objects.select_related('etudiant__user', 'session__cours').order_by('-session__date_session')[:100]
    return render(request, 'presences/historique.html', {'presences': presences})
