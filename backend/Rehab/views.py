from django.shortcuts import render
from pymongo import MongoClient 
from .Rehab_logic import generate_rehabilitation_plan
from django.http import JsonResponse


# Connecting to Mongo
client = MongoClient("mongodb://localhost:27017/")
db = client["employees"]
convo = db["NFC"]


# Create your views here.
def analytics(request):
    if request.method == "POST":
        addiction = request.POST.getlist("addiction")
        start_date = request.POST.get("start-date")
        frequency = request.POST.get("frequency")
        impact = request.POST.get("impact")
        attempts = request.POST.get("attempts")
        support = request.POST.get("support")
        triggers = request.POST.get("triggers")
        current_status = request.POST.get("current-status")
        goals = request.POST.get("goals")
        other_info = request.POST.get("other-info")
        emergency_contact1 = request.POST.get("emergency-contact1")
        emergency_contact2 = request.POST.get("emergency-contact2")
        # Analytics = analytics(name = name, start_date = start_date, frequency = frequency,
        #                         impact = impact, attempts = attempts, support = support, triggers = triggers, 
        #                         current_status = current_status, goals= goals, other_info = other_info,
        #                         emergency_contact1 = emergency_contact1, emergency_contact2 = emergency_contact2)
        # Analytics.save()

        # Retrieve conversation data from MongoDB
        all_conversations = convo.find()

        # Initialize a list to hold all messages
        all_messages = []

        # Iterate over each document and extract the 'messages' field
        for conversation in all_conversations:
            messages = conversation.get('messages', [])
            all_messages.extend(messages)  # Add all messages to the list

        # Prepare data for LLM
        form_data = {
            "addiction": addiction,
            "start_date": start_date,
            "frequency": frequency,
            "impact": impact,
            "attempts": attempts,
            "support": support,
            "triggers": triggers,
            "current_status": current_status,
            "goals": goals,
            "other_info": other_info,
            "emergency_contact1": emergency_contact1,
            "emergency_contact2": emergency_contact2
        }

        # Generate a personalized rehabilitation plan using LLM
        rehabilitation_plan = generate_rehabilitation_plan(form_data, all_messages)
        return JsonResponse({"rehabilitation_plan": rehabilitation_plan})
        
        # redirect after submitting
        # return HttpResponseRedirect('')
    return(render(request, 'form.html'))
