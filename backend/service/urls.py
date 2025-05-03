from django.urls import path
from .views import CreateRequestView
from . import views
from .views import send_request_view
from .views import request_panel_view, panel_login

urlpatterns = [
    path('request/', CreateRequestView.as_view(), name='create-request'),
    path('', views.home, name='home'),
    path('send-request/', send_request_view, name='send_request'),
    path('panel/login/', auth_views.LoginView.as_view(template_name='service/panel_login.html'), name='login'),
    path('panel/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('panel/', views.request_panel_view, name='panel'),
    path('panel/update-status/<int:request_id>/', views.update_status_view, name='update_status'),
]
