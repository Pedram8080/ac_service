from django.contrib import admin
from .models import Request, ServiceRequest, Article, ArticleSection


class ArticleSectionInline(admin.StackedInline):
    model = ArticleSection
    extra = 1
    fields = ('title', 'slug', 'content', 'image', 'order')


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
    list_display = ('id', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    fields = ('is_active',)
    inlines = [ArticleSectionInline]
