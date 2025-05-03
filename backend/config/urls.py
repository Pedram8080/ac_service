from django.contrib import admin
from django.urls import path, include
from service.views import home
from django.contrib.sitemaps.views import sitemap
from service.sitemaps import StaticViewSitemap
from service.views import robots_txt
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
import os


sitemaps_dict = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('service.urls')),
    # path('sms/', include('service.urls')), comment
    path('', home, name='home'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', serve, {'path': 'sitemap.xml', 'document_root': os.path.join(settings.BASE_DIR, 'static')}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

