from django.urls import path
from . import views

urlpatterns = [
    path('', views.cours_list, name='cours_list'),
    path('<int:pk>/', views.cours_detail, name='cours_detail'),
    path('<int:cours_pk>/sessions/', views.session_list, name='session_list'),
]
