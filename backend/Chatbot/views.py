from django.shortcuts import render
import json
from django.http import JsonResponse
from .Chatbot_Logic import get_chatbot_response

# Create your views here.

def chat_view(request):
    if request.method == "GET":
    # Renders the chat interface
        return render(request, 'indexcb.html')
    elif request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message")
        bot_response = get_chatbot_response(user_message)
        return JsonResponse({"response": bot_response})