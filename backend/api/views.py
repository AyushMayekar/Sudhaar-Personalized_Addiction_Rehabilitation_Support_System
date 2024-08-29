from django.shortcuts import render, redirect
from requests import request
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from bson import ObjectId
from dotenv import load_dotenv
import os
from .serializers import UserSerializer

load_dotenv()

DB_URI = os.getenv("url")
DB_NAME = os.getenv("dbname")
COLLECTION_NAME = os.getenv("collectionname")

def SignUp(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        print("\n\n", uname, email, pass1, pass2, "\n\n")

        if pass1 != pass2:
            print("password did not match")
            render(request, 'signup.html', {'error': 'Passwords do not match'})
            pass
            # return render(request, 'signup.html', {'error': 'Passwords do not match'})

        # Create the user document
        user_data = {
            'username': uname,
            'email': email,
            'password': generate_password_hash(pass1),  # Hash the password before storing
            #'jwt_token': '',  # Placeholder for JWT token
        }

        # Initialize MongoDB client
        client = MongoClient(DB_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Check if the username already exists
        if collection.find_one({"username": uname}):
            print("\n\nUSER NAME ALREADY EXIST")
            return render(request, 'signup.html', {'error': 'Username already exists'})

        try:
            # Insert the new user document
            result = collection.insert_one(user_data)
            print("NEW USER REGISTERED")
            serializer = UserSerializer(data=user_data)
            if serializer.is_valid():
                serializer.save()
            return redirect('/api/user/login/')
            #if result.inserted_id:
                # # Generate JWT token
                # user = {'username': uname}  # Mock user for token generation
                # refresh = RefreshToken.for_user(user)
                # access_token = str(refresh.access_token)
                # print("ACCESS TOKENS: ", access_token)
                
                # # Update the document with the JWT token
                # # collection.update_one({'_id': result.inserted_id}, {'$set': {'jwt_token': access_token}})

        except Exception as e:
            print(e)
            return render(request, 'signup.html', {'error': 'Failed to create user'})

    return render(request, 'signup.html')


# def SignUp(request):
#     if request.method == 'POST':
#         uname = request.POST.get('username')
#         email = request.POST.get('email')
#         pass1 = request.POST.get('password1')
#         pass2 = request.POST.get('password2')
#         print("\n\n", uname, email, pass1, pass2,"\n\n")
#         if pass1 != pass2:

#             return render(request, 'signup.html', {'error': 'Passwords do not match'})
#         user_data = {
#             'username': uname,
#             'email': email,
#             'password': pass1,
#         }
#         serializer = UserSerializer(data=user_data)
#         if serializer.is_valid():
#             serializer.save()
#             return redirect('/api/user/login/')  # Redirect to the login page
#         else:
#             return render(request, 'signup.html', {'error': 'Invalid data'})

#     return render(request, 'signup.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("\n\n", username, password,"\n\n")
        # Use the custom backend to authenticate with email
        client = MongoClient(DB_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        user = collection.find_one({"username": username})
        if user:
        # Check the password
            if check_password_hash(user['password'], password):
                print("\n\nUSER MATCHED")
                return render(request, 'login.html')
            else:
                print("PASSWORD INCORRECT")
                return render(request, 'login.html')
        else:
            print("USER NOT FOUND")
            return render(request, 'login.html')
    return render(request, 'login.html')

