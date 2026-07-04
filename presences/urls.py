from django.urls import path
from . import views

urlpatterns = [
    path('', views.historique_presence, name='presences'),
    path('session/<int:session_pk>/', views.feuille_presence, name='feuille_presence'),
]
