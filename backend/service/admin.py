from django.contrib import admin
from .models import ServiceRequest


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service_type', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone')
