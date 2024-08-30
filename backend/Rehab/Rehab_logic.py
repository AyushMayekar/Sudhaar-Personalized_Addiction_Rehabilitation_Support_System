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



def generate_rehabilitation_plan(form_data, conversation_messages):

    prompt = f"""
    Based on the following information:
    - Addiction Type: {form_data['addiction']}
    - Start Date: {form_data['start_date']}
    - Frequency: {form_data['frequency']}
    - Impact: {form_data['impact']}
    - Attempts: {form_data['attempts']}
    - Support: {form_data['support']}
    - Triggers: {form_data['triggers']}
    - Current Status: {form_data['current_status']}
    - Goals: {form_data['goals']}
    - Other Info: {form_data['other_info']}
    - Emergency Contacts: {form_data['emergency_contact1']}, {form_data['emergency_contact2']}
    
    And the conversation history:
    {''.join([f"User: {msg['text']}\n" if msg['sender'] == 'user' else f"Bot: {msg['text']}\n" for msg in conversation_messages])}
    
    Provide a detailed personalized rehabilitation plan.
    """

    response = model.generate_content(prompt)
    bot_response = response.text
    return bot_response