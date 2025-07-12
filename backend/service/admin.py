from django.contrib import admin
from .models import ServiceRequest, Article, ArticleSection, ArticleImage


class ArticleSectionInline(admin.StackedInline):
    model = ArticleSection
    extra = 1
    fields = ('title', 'slug', 'content', 'image', 'order')
    readonly_fields = ('slug',)


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1
    fields = ('image',)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service_type', 'status', 'created_at')
    search_fields = ('name', 'phone')
    list_filter = ('service_type', 'status', 'created_at')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    fields = ('title', 'slug', 'image', 'is_active')
    inlines = [ArticleSectionInline, ArticleImageInline]
    readonly_fields = ('slug',)
