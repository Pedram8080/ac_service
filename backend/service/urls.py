from django.urls import path
from .views import CreateRequestView
from . import views
from .views import send_request_view

urlpatterns = [
    path('request/', CreateRequestView.as_view(), name='create-request'),
    path('', views.home, name='home'),
    path('send-request/', send_request_view, name='send_request'),
]
