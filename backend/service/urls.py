from django.urls import path
from .views import CreateRequestView
from . import views
from .views import request_specialist
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('request/', CreateRequestView.as_view(), name='create-request'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sms/send-request/', request_specialist, name='request_specialist'),
    path('panel/login/', auth_views.LoginView.as_view(template_name='service/panel_login.html'), name='login'),
    path('panel/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('panel/', views.request_panel_view, name='panel'),
    path('panel/update-status/<int:request_id>/', views.update_status_view, name='update_status'),
    path('panel/delete-request/<int:request_id>/', views.delete_request_view, name='delete_request'),
    path('panel/delete-selected/', views.delete_selected_requests_view, name='delete_selected'),
    path('article/', views.article_view, name='article'),
    path('article/<str:slug>/', views.article_detail_view, name='article_detail'),
    
]
