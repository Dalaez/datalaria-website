import os
import google.generativeai as genai

os.environ['API_KEY'] = 'GEMINI_API_KEY'
genai.configure(api_key=os.environ['API_KEY'])
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
