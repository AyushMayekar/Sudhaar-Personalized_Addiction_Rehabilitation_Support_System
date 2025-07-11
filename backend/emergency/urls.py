from django.urls import path
from .views import send_emergency_message

urlpatterns = [
    path('sem/', send_emergency_message, name='send_emergency_message'),
]