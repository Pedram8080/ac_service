from django.contrib import admin
from django.urls import path, include
from service.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('service.urls')),
    # path('sms/', include('service.urls')),
    path('', home, name='home'),
]
