from django.urls import path
from .views import CreateRequestView
from . import views
from .views import send_request_view
from .views import request_panel_view, update_status_view, panel_login, panel_logout

urlpatterns = [
    path('request/', CreateRequestView.as_view(), name='create-request'),
    path('', views.home, name='home'),
    path('send-request/', send_request_view, name='send_request'),
    path('panel/', request_panel_view, name='request_panel'),
    path('panel/', request_panel_view, name='request_panel'),
    path('panel/login/', panel_login, name='panel_login'),
    path('panel/logout/', panel_logout, name='panel_logout'),
    path('panel/status/<int:pk>/', update_status_view, name='update_status'),
]
