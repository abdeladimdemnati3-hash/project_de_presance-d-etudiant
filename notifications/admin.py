from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('parent', 'type', 'lu', 'envoyee_le')
    list_filter = ('type', 'lu')
    date_hierarchy = 'envoyee_le'
