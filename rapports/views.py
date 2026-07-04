from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from accounts.models import Groupe, Filiere, Etudiant
from presences.models import Presence
from cours.models import SessionCours
import io
import openpyxl
from django.http import HttpResponse


@login_required
def rapport_list(request):
    filieres = Filiere.objects.all()
    groupes = Groupe.objects.select_related('filiere').all()
    return render(request, 'rapports/liste.html', {'filieres': filieres, 'groupes': groupes})


@login_required
def generer_rapport(request):
    groupe_id = request.GET.get('groupe')
    filiere_id = request.GET.get('filiere')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    format_export = request.GET.get('format', 'html')

    presences = Presence.objects.select_related('etudiant__user', 'session__cours', 'session__groupe')
    if groupe_id:
        presences = presences.filter(session__groupe_id=groupe_id)
    if filiere_id:
        presences = presences.filter(session__groupe__filiere_id=filiere_id)
    if date_debut:
        presences = presences.filter(session__date_session__gte=date_debut)
    if date_fin:
        presences = presences.filter(session__date_session__lte=date_fin)

    stats = presences.values('etudiant__user__first_name', 'etudiant__user__last_name', 'etudiant__matricule').annotate(
        total=Count('id'),
        presents=Count('id', filter=Q(statut='present')),
        absents=Count('id', filter=Q(statut='absent')),
        retards=Count('id', filter=Q(statut='retard')),
    )

    if format_export == 'excel':
        return export_excel(stats)

    return render(request, 'rapports/rapport.html', {
        'stats': stats,
        'groupe_id': groupe_id,
        'date_debut': date_debut,
        'date_fin': date_fin,
    })


def export_excel(stats):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Rapport Présence'
    headers = ['Matricule', 'Prénom', 'Nom', 'Total', 'Présents', 'Absents', 'Retards', 'Taux (%)']
    ws.append(headers)
    for row in stats:
        taux = round((row['presents'] / row['total']) * 100, 1) if row['total'] else 0
        ws.append([
            row['etudiant__matricule'],
            row['etudiant__user__first_name'],
            row['etudiant__user__last_name'],
            row['total'], row['presents'], row['absents'], row['retards'], taux
        ])
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=rapport_presence.xlsx'
    return response
