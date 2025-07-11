from django.urls import path
from .views import Community, com

urlpatterns = [
    path('community', Community, name='community'),
    path('com', com, name='com'), 
]