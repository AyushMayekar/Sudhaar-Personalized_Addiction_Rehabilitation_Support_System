from django.shortcuts import render
from .community_logic import message_analysis, display_messages, update_DB
from django.shortcuts import render, HttpResponseRedirect
import json
from django.http import JsonResponse
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

# Connecting to Mongo
Mongo_url = os.getenv('mongo')
client = MongoClient(Mongo_url)
db = client["NFC"]
messages_collection = db["Community"]
users = db["USER DATA"]

def Community(request):
    if 'userid' in request.session:
        return render(request, 'community.html', {"loggedin_username": request.session['username']})
    else:
        return HttpResponseRedirect('https://sudhaar-personalizedaddictionrehabilitationsu-production.up.railway.app/login?nouser=true')

@csrf_exempt
def com(request):
    if request.method == "GET":
        if 'userid' not in request.session:
            return JsonResponse({"detail": "Unauthorized"}, status=401)
        
        update_DB()  # Clean old msgs
        messages = display_messages()
        return JsonResponse(messages, safe=False)

    elif request.method == "POST":
        if 'userid' not in request.session:
            return JsonResponse({"detail": "Unauthorized"}, status=401)

        user_id = request.session['userid']
        user_data = users.find_one({"userid": user_id})

        if not user_data:
            return JsonResponse({"detail": "User not found"}, status=400)

        username = user_data.get("username", "Unknown")

        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()
        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON body"}, status=400)

        if not user_message:
            return JsonResponse({"detail": "Type something Chad!!"}, status=400)

        sentiment = message_analysis(user_message)
        if sentiment == "negative":
            return JsonResponse({"detail": "Follow community guidelines. Negative messages are not allowed."}, status=400)

        message_entry = {
            "sender": username,
            "user id": user_id,
            "message": user_message,
            "timestamp": datetime.utcnow()
        }

        messages_collection.insert_one(message_entry)

        return JsonResponse({
            "message": user_message,
            "sender": username,
            "sentiment": sentiment,
            "success": True
        })

    else:
        return JsonResponse({"detail": "Method not allowed"}, status=405)