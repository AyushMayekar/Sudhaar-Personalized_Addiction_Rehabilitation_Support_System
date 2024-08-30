from pymongo import MongoClient 
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime
# Loading gemini
load_dotenv()
gemini_api_key = os.getenv("google_gemini_api")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-pro")


# Connecting to Mongo
mongo_uri = os.getenv("mongo1")
client = MongoClient(mongo_uri)
db = client["django"]
convo = db["users"]


def get_chatbot_response(user_message, request, is_first_message=False):

    user_id = request.user.id if request.user.is_authenticated else None
    if user_id is None:
        raise ValueError("User is not authenticated")
    
    convo_log = convo.find_one({"user_id": user_id})
    
    if convo_log is None:
        # Create a new conversation document if it does not exist
        convo_log = {
            "user_id": user_id,
            "messages": [],
            "created_at": datetime.now()
        }

    if is_first_message:
        prompt = "Ask the content given in the backticks `Hello! How can I assist you today?`"
    else:
        convo_log.clear()
        prompt = f"""Role: "You are a compassionate and skilled counselor.

Objective: Engage in a thoughtful and supportive conversation with the user. Guide them toward improvement based on their responses. Follow the 6 rules outlined below.

Guidelines:
Conversational Flow: Ask one open-ended question at a time, and provide thoughtful guidance based on the user's last response.
Feedback Integration: After every two main questions, subtly incorporate a feedback question. Use the feedback to refine your subsequent questions and guidance.
Focused Interaction: Limit the conversation to 12 carefully chosen questions. Aim to gather as much useful information as possible within this scope.
Personalized Plan: Based on the information gathered, suggest a personalized rehabilitation plan by the end of the conversation. Encourage the user to follow it.
Sequential Engagement: Do not generate the entire conversation at once. Respond only with the next appropriate question or statement.
Progressive Dialogue: Continue the conversation until you have asked approximately 10 questions and gathered enough information to provide tailored advice.
User's Response: "{user_message}".
        """

    response = model.generate_content(prompt)
    bot_response = response.text

    # Append the new user message and bot response to the conversation log
    convo_log['messages'].append({
        "user_message": user_message,
        "bot_response": bot_response
    })

    # Update the conversation document with the new messages
    convo.update_one(
        {"user_id": user_id},
        {"$set": convo_log},
        upsert=True
    )

    return bot_response