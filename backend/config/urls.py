from django.contrib import admin
from django.urls import path, include
from service.views import home
from django.contrib.sitemaps.views import sitemap
from service.sitemaps import StaticViewSitemap

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('service.urls')),
    # path('sms/', include('service.urls')), comment
    path('', home, name='home'),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

sitemaps = {
    'static': StaticViewSitemap,
}