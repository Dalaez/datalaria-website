import os
from litellm import completion

os.environ['GEMINI_API_KEY'] = 'AIzaSyApj8dOGf1vKSHahb1dVx5O8pKhXUP7Y48'

try:
    response = completion(
        model='gemini/gemini-1.5-flash',
        messages=[{ 'content': 'Hello', 'role': 'user'}]
    )
    print('gemini/gemini-1.5-flash works!')
except Exception as e:
    print('Error with flash:', e)

try:
    response = completion(
        model='gemini/gemini-pro',
        messages=[{ 'content': 'Hello', 'role': 'user'}]
    )
    print('gemini/gemini-pro works!')
except Exception as e:
    print('Error with pro:', e)

