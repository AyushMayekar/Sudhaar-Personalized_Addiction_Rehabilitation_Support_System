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
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=403)

        try:
            data = json.loads(request.body)
            user_message = data.get("message")
            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)
            bot_response = get_chatbot_response(user_message, request)
            return JsonResponse({"response": bot_response})

        except Exception as e:
            # Log the exception and return a generic error response
            print(f"Error in chat_view: {e}")
            return JsonResponse({"error": "An error occurred"}, status=500)