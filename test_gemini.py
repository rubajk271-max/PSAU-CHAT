import google.generativeai as genai
import sys

api_key = "AIzaSyCs5lLRHXQpYV4ZebvRcYyfJhfeZpAx79o"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

try:
    response = model.generate_content("Hello! Are you working?")
    print("SUCCESS:", response.text)
except Exception as e:
    print("ERROR:", str(e))
