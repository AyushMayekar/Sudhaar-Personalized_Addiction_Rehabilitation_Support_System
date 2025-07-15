from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from pymongo import MongoClient
import random
import json
import traceback
from dotenv import load_dotenv
import os
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


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
            hashed_password = make_password(password1)
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
import traceback  # Add this at the top if not already imported

#* Login 
def userlogin(request):
    try:
        print("🟡 LOGIN VIEW HIT")

        if request.method == 'POST':
            print("🟢 POST request received")

            username = request.POST.get('username')
            password = request.POST.get('password')

            print(f"📥 Username: {username}")
            print(f"📥 Password: {password}")

            user = collection.find_one({'username': username})
            print(f"🔍 DB Lookup Result: {user}")

            if user:
                print("✅ User found in DB")

                # Logging stored password info
                print(f"🔐 Stored Password (type: {type(user['password'])}): {user['password']}")

                try:
                    is_valid = check_password(password, user['password'])
                    print(f"🔐 Password Valid: {is_valid}")
                except Exception as pw_err:
                    print("🔥 Error during password verification")
                    print(f"❌ Password error: {pw_err}")
                    print(traceback.format_exc())
                    return JsonResponse({'error': str(pw_err), 'trace': traceback.format_exc()}, status=500)

                if is_valid:
                    print("🎉 Password matched, logging user in...")

                    request.session['is_logged_in'] = True
                    request.session['username'] = username
                    request.session['userid'] = user.get('userid')  
                    
                    print(f"🗝️ Session Set: {request.session.items()}")
                    return redirect('https://sudhaar-personalizedaddictionrehabilitationsu-production.up.railway.app/')
                else:
                    print("❌ Invalid password entered")
                    return render(request, 'login.html', {'logerror': True})

            else:
                print("❌ Username not found in DB")
                return render(request, 'login.html', {'Nouser': True})

        else:
            print("⚠️ Non-POST request received")
            return render(request, 'login.html')

    except Exception as e:
        print("🔥🔥🔥 UNHANDLED LOGIN VIEW ERROR 🔥🔥🔥")
        print(f"🛑 Error: {e}")
        print(traceback.format_exc())
        return JsonResponse({'error': str(e), 'trace': traceback.format_exc()}, status=500)

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
