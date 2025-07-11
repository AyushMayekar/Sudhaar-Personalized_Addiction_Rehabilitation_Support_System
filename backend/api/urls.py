from django.urls import path
from  .views import signup,userlogin,userlogout, forgot_password, reset_password

urlpatterns = [
    path('signup',signup, name="signup"),
    path('login', userlogin, name="login"),
    path('userlogout', userlogout, name="userlogout"),
    path("forgot_password", forgot_password, name="forgot password"),
    path("reset_password", reset_password, name="reset password"),
]
