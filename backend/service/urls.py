from django.urls import path
from .views import CreateRequestView
from . import views
from .views import send_request_view
from .views import request_panel_view, panel_login

urlpatterns = [
    path('request/', CreateRequestView.as_view(), name='create-request'),
    path('', views.home, name='home'),
    path('send-request/', send_request_view, name='send_request'),
    path('panel/', views.request_panel_view, name='panel'),
    path('mark-done/<int:request_id>/', views.mark_done_view, name='mark_done'),
]
