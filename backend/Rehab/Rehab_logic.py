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
You are a rehabilitation planning expert.
Based on the following client details and conversation history, 
generate a **personalized rehabilitation plan**. 
Format the output cleanly and consistently with clear headings and bullet points. 
Do not include any markdown formatting like ** or *.

Client Details:
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

Conversation Context:
{conversation_messages}

---

Your output must include the following sections in **this exact order**:

1. Phase 1: Assessment and Stabilization
2. Phase 2: Treatment
3. Phase 3: Maintenance
4. Phase 4: Aftercare
5. Goals
6. Support System
7. Triggers
8. Additional Components
9. Evaluation
10. Other Information

---

**Format Instructions**:
- Each section title must start with the name above, without markdown.
- Use plain bullet points for steps.
- Keep each bullet as one action/idea.
- Avoid repeating user input blindly.
- Avoid using symbols like `*`, `**`, `-`, or `:` at the start or end.
- Be concise but clinically complete.
"""

    response = model.generate_content(prompt)
    bot_response = response.text
    return bot_response