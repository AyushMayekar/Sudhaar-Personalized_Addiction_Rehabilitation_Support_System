from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import os

load_dotenv()
@csrf_exempt
def send_emergency_message(request):
    if 'userid' in request.session:
        if request.method == 'POST':
            account_sid = os.getenv('account_sid')
            auth_token = os.getenv('auth_token')
            client = Client(account_sid, auth_token)
            print(account_sid, auth_token)

            message = client.messages.create(
                body="Urgent: Please contact [Emergency Services Number] immediately. [Patient's Name] is in a critical situation at [Location], experiencing [brief description of the emergency, e.g., severe withdrawal symptoms/unconsciousness]. Your immediate presence and assistance are needed. For more details, please call [Your Phone Number].",
                from_='+15108764218',
                to='+918675153773'
            )

            return JsonResponse({'sid': message.sid})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)
    else :
            return HttpResponseRedirect('http://127.0.0.1:8000/login?nouser=true')