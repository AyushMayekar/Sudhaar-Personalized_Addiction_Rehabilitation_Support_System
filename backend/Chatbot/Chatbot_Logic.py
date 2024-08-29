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
client = MongoClient("mongodb://localhost:27017/")
db = client["employees"]
convo = db["NFC"]


def get_chatbot_response(user_message):
    prompt = f"""Act as a Counsellor. Continue the conversation based on the user's response and follow the 5 rules given below, 
    1. Ask one question at a time and also respond or guide the user towards betterment according to the users previous response.
    2. Ask not more than 10 to 12 questions, try to gain as much as you can from these questions.
    3. Suggest a rehabilitation plan to the user based on the information you collected and ask him to follow it.
    4. Do not generate the entire conversation at once. 
    5. Respond only with the next appropriate question or statement, at the end after around 10 questions,
    User's response: '{user_message}'."""

    response = model.generate_content(prompt)
    bot_response = response.text

    return bot_response