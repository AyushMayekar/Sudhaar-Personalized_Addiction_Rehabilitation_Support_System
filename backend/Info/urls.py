from django.urls import path
from .views import addictions, Aboutus, progress, get_rehabilitation_plan_api

urlpatterns = [
    path('addiction', addictions, name='addiction'),
    path ('abs', Aboutus, name= 'About Us'),
    path('pro', progress, name='progress'),
    path ('rehab_plan', get_rehabilitation_plan_api, name = 'Rehab Plan')
]
