from django.contrib import admin
from .models import Request, ServiceRequest, Article


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service_type', 'created_at')
    search_fields = ('name', 'phone')
    list_filter = ('service_type', 'created_at')


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service_type', 'status', 'created_at')
    search_fields = ('name', 'phone')
    list_filter = ('service_type', 'status', 'created_at')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    fields = ('title', 'slug', 'image', 'content', 'is_active')
