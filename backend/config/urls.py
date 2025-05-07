from django.contrib import admin
from django.urls import path, include
from service.views import home
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
import os
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from service.models import ServiceRequest
from service.sitemaps import ArticleSitemap


class ServiceSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return ServiceRequest.objects.all()

    def location(self, item):
        return f"/sms/panel/{item.pk}/"  # یا هر آدرسی که نمایش می‌دی


sitemaps = {
    'services': ServiceSitemap,
    'articles': ArticleSitemap,
}

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('service.urls')),
                  path('', home, name='home'),
                  path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
                  path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
              ]

# اضافه کردن تنظیمات static و media
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # در حالت production، فایل‌های media را از طریق Nginx سرو می‌کنیم
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
