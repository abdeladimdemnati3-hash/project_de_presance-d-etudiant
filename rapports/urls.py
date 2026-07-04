from django.urls import path
from . import views

urlpatterns = [
    path('', views.rapport_list, name='rapports'),
    path('generer/', views.generer_rapport, name='generer_rapport'),
]
