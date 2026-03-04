import os
import google.generativeai as genai

os.environ['API_KEY'] = 'AIzaSyApj8dOGf1vKSHahb1dVx5O8pKhXUP7Y48'
genai.configure(api_key=os.environ['API_KEY'])
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
