from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from accounts.models import Parent


@login_required
def notification_list(request):
    parent = get_object_or_404(Parent, user=request.user)
    notifications = Notification.objects.filter(parent=parent).order_by('-envoyee_le')
    return render(request, 'notifications/liste.html', {
        'notifications': notifications,
        'non_lues': notifications.filter(lu=False).count()
    })


@login_required
def marquer_lu(request, pk):
    parent = get_object_or_404(Parent, user=request.user)
    notif = get_object_or_404(Notification, pk=pk, parent=parent)
    notif.lu = True
    notif.save(update_fields=['lu'])
    return redirect('notifications')


@login_required
def marquer_toutes_lues(request):
    parent = get_object_or_404(Parent, user=request.user)
    Notification.objects.filter(parent=parent, lu=False).update(lu=True)
    return redirect('notifications')
