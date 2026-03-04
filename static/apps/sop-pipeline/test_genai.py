import os
import google.generativeai as genai

os.environ['API_KEY'] = 'GEMINI_API_KEY'
genai.configure(api_key=os.environ['API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash')
try:
    response = model.generate_content('Hello')
    print('SUCCESS:', response.text)
except Exception as e:
    print('ERROR:', e)
