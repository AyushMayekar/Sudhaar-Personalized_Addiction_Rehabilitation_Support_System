from django.shortcuts import render, HttpResponseRedirect
from pymongo import MongoClient 
from .Rehab_logic import generate_rehabilitation_plan
import os


# Connecting to Mongo
Mongo_url = os.getenv('mongo')
client = MongoClient(Mongo_url)
db = client["NFC"]
convo = db["USER DATA"]

def format_conversation_log(conversation_log):
    formatted_log = ''
    
    for entry in conversation_log:
        user_message = entry.get('user_message', '').strip()
        bot_response = entry.get('bot_response', '').strip()
        
        if user_message:
            formatted_log += f"User: {user_message}\n"
        if bot_response:
            formatted_log += f"Bot: {bot_response}\n"
    
    return formatted_log

# Create your views here.
def analytics(request):
    if 'userid' in request.session:
        user_id = request.session['userid']
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

        # Retrieve conversation data from MongoDB
            all_conversations = convo.find_one({'userid': user_id},
                                            {'conversation_log': True, '_id' : False})
            Chat = format_conversation_log(all_conversations['conversation_log'])
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

            convo.update_one(
        {'userid': user_id},  
        {'$set': {'form_data' : form_data}}   
            )

        # Generate a personalized rehabilitation plan using LLM
            rehabilitation_plan = generate_rehabilitation_plan(form_data, Chat)
            convo.update_one(
            {'userid': user_id},  
            {'$set': {'Rehab_Plan' : rehabilitation_plan}}   
            )
            return(render(request, 'form.html'))
        
        # redirect after submitting
        return(render(request, 'form.html'))
    else:
        return HttpResponseRedirect('http://127.0.0.1:8000/login?nouser=true')

