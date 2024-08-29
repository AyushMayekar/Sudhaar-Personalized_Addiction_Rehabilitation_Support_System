# from django.contrib import admin
# from api import views
# from django.urls import path, include
# from api.views import CreateUserView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("api/user/signup/", views.SignUp, name="register"),
#     path("api/user/login/", views.Login, name="Login"),
#     # path("api/user/register/", CreateUserView.as_view(), name="register"),
#     path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
#     path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
#     path("api-auth/", include("rest_framework.urls")),
#     # path("api/", include("api.urls")),
# ]

from django.contrib import admin
from django.urls import path, include
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/signup/", views.SignUp, name="register"),
    path("api/user/login/", views.Login, name="Login"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
]