from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import os

load_dotenv()
twilio_number = os.getenv('twilio_number')
@csrf_exempt
def send_emergency_message(request):
    if 'userid' in request.session:
        if request.method == 'POST':
            account_sid = os.getenv('account_sid')
            auth_token = os.getenv('auth_token')
            client = Client(account_sid, auth_token)
            print(account_sid, auth_token)

            message = client.messages.create(
                from_= +13374694211,
                body="Urgent: Please contact 8657153773 immediately. Ayush Mayekar is in a critical situation. Your immediate presence and assistance are needed. For more details, please call 8657153773.",
                to='+919892496621'
            )

            return JsonResponse({'Message sent - sid': message.sid})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)
    else :
            return HttpResponseRedirect('https://sudhaar-personalizedaddictionrehabilitationsu-production.up.railway.app/login?nouser=true')