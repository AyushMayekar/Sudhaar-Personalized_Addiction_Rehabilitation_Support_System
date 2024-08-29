from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from requests import request
from .models import Clients



def SignUp(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        print("\n\n", uname, email, pass1, pass2,"\n\n")

        if pass1 != pass2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        user_data = {
            'username': uname,
            'email': email,
            'password': pass1,
        }
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return redirect('/api/user/login/')  # Redirect to the login page
        else:
            return render(request, 'signup.html', {'error': 'Invalid data'})

    return render(request, 'signup.html')


def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            # Store the JWT token in a variable or session as needed
            return render(request, 'login.html', {'token': access_token})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from rest_framework import generics
# from .serializers import UserSerializer
# from rest_framework.permissions import IsAuthenticated, AllowAny


# def SignUp(request):
#     if request.method == 'POST':
#         uname = request.POST.get('username')
#         email = request.POST.get('email')
#         pass1 = request.POST.get('password1')
#         pass2 = request.POST.get('password2')
#         new_user = User.objects.create_user(uname, email, pass1)
#         new_user.save()
#         return redirect('api/user/login')
#     return ( render(request,'signup.html') )

# def Login(request):
#     return (render(request,'login.html'))

# class CreateUserView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]