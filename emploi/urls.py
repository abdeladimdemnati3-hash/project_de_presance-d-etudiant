from django.urls import path
from . import views

urlpatterns = [
    path('', views.emploi_list, name='emploi_list'),
    path('upload/', views.emploi_upload, name='emploi_upload'),
    path('delete/<int:pk>/', views.emploi_delete, name='emploi_delete'),
]
