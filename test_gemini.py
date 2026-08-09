import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

try:
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Hello, this is a test. Just say OK if you hear me.")
    print("Success! Response from model:", response.text)
except Exception as e:
    print("Error:", e)
