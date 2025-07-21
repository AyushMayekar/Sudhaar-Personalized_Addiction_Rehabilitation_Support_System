from django.shortcuts import render,HttpResponseRedirect
from pymongo import MongoClient
import os
from django.http import JsonResponse
import re

# Connecting to Mongo
Mongo_url = os.getenv('mongo')
client = MongoClient(Mongo_url)
db = client["NFC"]
convo = db["USER DATA"]


def addictions(request):
    if 'userid' in request.session:
            return render(request, 'Addictions.html')
    else :
            return HttpResponseRedirect('https://sudhaar-personalizedaddictionrehabilitationsu-production.up.railway.app/login?nouser=true')
    

def Aboutus(request):
    return render(request, 'Aboutus.html')


# Utility function to clean and format LLM response
def format_raw_plan(plan):
    sections = {}
    current_section = "General"
    buffer = []

    # Define the expected section headers (clean, no markdown)
    section_headers = [
        "Phase 1: Assessment and Stabilization",
        "Phase 2: Treatment",
        "Phase 3: Maintenance",
        "Phase 4: Aftercare",
        "Goals",
        "Support System",
        "Triggers",
        "Additional Components",
        "Evaluation",
        "Other Information"
    ]

    for line in plan.splitlines():
        line = line.strip()
        if not line:
            continue

        # Check if the line matches one of the section headers exactly
        if any(line.lower().startswith(header.lower()) for header in section_headers):
            if buffer:
                sections[current_section] = buffer
                buffer = []
            current_section = line.strip()
            continue

        # Clean bullets or noise (if any)
        cleaned = re.sub(r"^[\*\-•\d\.\s]+", '', line).strip()

        if cleaned:
            buffer.append(cleaned)

    # Add the last section
    if buffer:
        sections[current_section] = buffer

    return sections

# API to get structured rehab plan
def get_rehabilitation_plan_api(request):
    if 'userid' in request.session: 
        user_id = request.session['userid']
        user_data = convo.find_one({'userid': user_id}, {'Rehab_Plan': True, 'username': True, 'email': True, '_id': False})
        if not user_data or 'Rehab_Plan' not in user_data:
            return JsonResponse({'error': 'Rehabilitation plan not found.'}, status=404)

        raw_plan = user_data['Rehab_Plan']
        general_info = {
        "Username": user_data.get('username', 'N/A'),
        "Email": user_data.get('email', 'N/A')
    }

        structured_plan = format_raw_plan(raw_plan)

        return JsonResponse({'rehab_plan': structured_plan, 'general_info': general_info})    
    return JsonResponse({'error': 'Unauthorized'}, status=401)


def progress(request):
    if 'userid' in request.session:
        user_id = request.session['userid']
        return render(request, 'progress.html')  
    else:
        return HttpResponseRedirect('https://sudhaar-personalizedaddictionrehabilitationsu-production.up.railway.app/login?nouser=true')