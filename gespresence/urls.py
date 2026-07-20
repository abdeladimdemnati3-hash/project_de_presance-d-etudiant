"""
URL configuration for gespresence project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from gespresence.chatbot_views import widget_js, chat_api

urlpatterns = [
    path('widget.js', widget_js, name='widget_js'),
    path('api/widget/chat', chat_api, name='widget_chat'),
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard'), name='root'),
    path('accounts/', include('accounts.urls')),
    path('', include('etudiants.urls')),
    path('enseignants/', include('enseignants.urls')),
    path('cours/', include('cours.urls')),
    path('presences/', include('presences.urls')),
    path('rapports/', include('rapports.urls')),
    path('notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
