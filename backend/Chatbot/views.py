from django.shortcuts import render, HttpResponseRedirect
import json
from django.http import JsonResponse
from .Chatbot_Logic import get_chatbot_response

# Create your views here.

def chat_view(request):
    if request.method == "GET":
        if 'userid' in request.session:
            return render(request, 'indexcb.html')
        else :
            return HttpResponseRedirect('http://127.0.0.1:8000/login?nouser=true')
    elif request.method == "POST":
        if 'userid' in request.session:
            user_id = request.session['userid']
            data = json.loads(request.body)
            user_message = data.get("message")
            bot_response = get_chatbot_response(user_message, user_id)
            return JsonResponse({"response": bot_response})
        else :
            return HttpResponseRedirect('http://127.0.0.1:8000/login?nouser=true')
