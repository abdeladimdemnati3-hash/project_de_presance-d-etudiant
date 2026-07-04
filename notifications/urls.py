from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notifications'),
    path('<int:pk>/lire/', views.marquer_lu, name='notif_lire'),
    path('tout-lire/', views.marquer_toutes_lues, name='notif_tout_lire'),
]
