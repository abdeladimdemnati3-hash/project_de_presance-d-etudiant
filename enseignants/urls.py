from django.urls import path
from . import views

urlpatterns = [
    path('', views.enseignant_list, name='enseignant_list'),
    path('<int:pk>/', views.enseignant_detail, name='enseignant_detail'),
    path('mes-sessions/', views.mes_sessions, name='mes_sessions'),
]
