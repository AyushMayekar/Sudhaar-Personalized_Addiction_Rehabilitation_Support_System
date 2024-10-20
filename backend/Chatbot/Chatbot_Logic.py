from pymongo import MongoClient 
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Loading gemini
load_dotenv()
gemini_api_key = os.getenv("google_gemini_api")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-pro")


# Connecting to Mongo
Mongo_url = os.getenv('mongo')
client = MongoClient(Mongo_url)
db = client["NFC"]
convo = db["USER DATA"]


def get_chatbot_response(user_message, user_id,  is_first_message=False):
    user_data = convo.find_one({'userid': user_id})
    if 'conversation_log' not in user_data:
        convo.update_one(
        {'userid': user_id},  
        {'$set': {'conversation_log': []}}  
        )
    convo_log = user_data.get('conversation_log', [])
    if is_first_message:
        prompt = "Ask the content given in the backticks `Hello! How can I assist you today?`"
    else:
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

    convo_log.append({
        "user_message": user_message,
        "bot_response": bot_response
    })
    convo.update_one(
        {'userid': user_id},
        {'$set': {'conversation_log': convo_log}}
    )

    return bot_response