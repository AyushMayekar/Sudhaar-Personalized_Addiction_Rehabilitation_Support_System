from django.urls import path
from .views import addictions, Aboutus

urlpatterns = [
    path('addiction', addictions, name='addiction'),
    path ('abs', Aboutus, name= 'About Us'),
]
