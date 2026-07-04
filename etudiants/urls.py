from django.urls import path
from . import views

urlpatterns = [
    path('etudiants/', views.etudiant_list, name='etudiant_list'),
    path('etudiants/<int:pk>/', views.etudiant_detail, name='etudiant_detail'),
]
