from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from pymongo import MongoClient
import bcrypt
import random
import json
from dotenv import load_dotenv
import os
from django.contrib.auth.hashers import make_password


load_dotenv()
# Connecting Mongo
Mongo_url = os.getenv('mongo')
client = MongoClient(Mongo_url)
db = client['NFC']
collection = db['USER DATA']


def generate_user_id(username):
    prefix = username[:3].upper()
    random_number = str(random.randint(1000, 9999))
    user_id = f"USR-{prefix}-{random_number}"
    return user_id

def signup(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')
        existing = collection.find_one({'username': username})

        if existing :
            return render(request, 'signup.html', {'existing' : True})

        if password1 == password2:
            hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
            userinfo={
            'userid' : generate_user_id(username), 
            'username' : request.POST.get('username'),
            'email' : request.POST.get('email'),
            'password': hashed_password,
        }
            collection.insert_one(userinfo)
            return redirect('/login')
        else :
            return render(request, 'signup.html', {'password_error' : True })
    return render(request, 'signup.html')

#* Login 
def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = collection.find_one({'username': username})

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                request.session['is_logged_in'] = True
                request.session['username'] = username
                request.session['userid'] = user.get('userid')  
                return redirect('https://sudhaar-personalizedaddictionrehabilitationsu-production.up.railway.app/')
            else:
                # Invalid password
                return render(request, 'login.html', {'logerror': True})
        else:
            # User not found
            return render(request, 'login.html', {'Nouser': True})

    # GET request or invalid form submission
    return render(request, 'login.html')

def userlogout(request):
    request.session.flush() 
    logout(request)
    return redirect('/login')

@csrf_exempt
def forgot_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")

        user = collection.find_one({ "email": email })
        return JsonResponse({ "exists": user is not None })

@csrf_exempt
def reset_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        new_password = data.get("new_password")

        hashed_password = make_password(new_password)

        result = collection.update_one(
            { "email": email },
            { "$set": { "password": hashed_password } }
        )

        if result.modified_count == 1:
            return JsonResponse({ "success": True })
        else:
            return JsonResponse({ "success": False, "message": "Failed to update password" })