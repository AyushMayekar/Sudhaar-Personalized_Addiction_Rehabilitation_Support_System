from django.urls import path
from .views import addictions, Aboutus, progress

urlpatterns = [
    path('addiction', addictions, name='addiction'),
    path ('abs', Aboutus, name= 'About Us'),
    path('pro', progress, name='progress'),
]
