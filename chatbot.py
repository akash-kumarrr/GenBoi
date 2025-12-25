import google.generativeai as genai
import os 
import os  
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('CONNECTION_API_KEY'))

model = genai.GenerativeModel("gemini-2.5-flash")

import re
def gemini_to_html(text: str) -> str:
    if not text:
        return ""

    text = text.strip()
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    for token in ("**", "*", "`", "###", "##", "#"):
        text = text.replace(token, "")
    for b in ("•", "–", "—"):
        text = text.replace(b, "-")

    return text.replace("\n", "<br>")


def gemini_response(user_prompt):
    response = model.generate_content(user_prompt)
    return gemini_to_html(response.text)
