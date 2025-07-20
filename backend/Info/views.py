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

    for line in plan.splitlines():
        line = line.strip()
        if not line:
            continue

        # Detect section headers
        match = re.match(r"\*\*?(Phase\s+\d+.*?|Additional Components|Goals|Support System|Triggers|Other Information|Evaluation)\**?:?", line, re.IGNORECASE)
        if match:
            if buffer:
                sections[current_section] = buffer
                buffer = []
            current_section = match.group(1).strip()
            continue

        # Remove bullets, markdown, leading garbage
        cleaned = re.sub(r"^[\*\-•\d\.\s]+", '', line)        # remove bullets
        cleaned = re.sub(r'\*\*+', '', cleaned)               # remove **
        cleaned = re.sub(r'\s*:\s*$', '', cleaned)            # remove trailing :
        cleaned = cleaned.strip()

        if cleaned:
            buffer.append(cleaned)

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
        general_info = [
            f"Username: {user_data.get('username', 'N/A')}",
            f"Email: {user_data.get('email', 'N/A')}",
        ]
        general_section = "**General:**\n" + "\n".join(f"* {line}" for line in general_info) + "\n\n"
        full_plan = general_section + raw_plan
        structured_plan = format_raw_plan(full_plan)

        return JsonResponse({'rehab_plan': structured_plan})
    
    return JsonResponse({'error': 'Unauthorized'}, status=401)


def progress(request):
    if 'userid' in request.session:
        user_id = request.session['userid']
        return render(request, 'progress.html')  
    else:
        return HttpResponseRedirect('https://sudhaar-personalizedaddictionrehabilitationsu-production.up.railway.app/login?nouser=true')