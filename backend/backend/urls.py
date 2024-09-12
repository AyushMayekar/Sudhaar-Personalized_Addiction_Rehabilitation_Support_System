from django.contrib import admin
from django.urls import path, include
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views 

urlpatterns = [
    path("admin/", admin.site.urls),
    path ('', views.landing, name= 'landing'),
    path('', include('api.urls')),
    path('', include('Chatbot.urls')),
    path ('', include('Info.urls')),
    path('Rehab/', include('Rehab.urls')),
    path('emer/', include('emergency.urls')),
]