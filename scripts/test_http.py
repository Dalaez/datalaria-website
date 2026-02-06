"""Test HTTP request exactly as browser does it"""
import requests
import json

app_id = 'C4NV3SCYAM'
search_key = '0130e86396a12b79b35c8cf37b692258'
index = 'datalaria_posts'

url = f'https://{app_id}-dsn.algolia.net/1/indexes/{index}/query'

headers = {
    'Content-Type': 'application/json',
    'X-Algolia-API-Key': search_key,
    'X-Algolia-Application-Id': app_id
}

body = {
    'query': 'outliers',
    'hitsPerPage': 5
}

print(f"URL: {url}")
print(f"Headers: {json.dumps(headers, indent=2)}")
print(f"Body: {json.dumps(body)}")

response = requests.post(url, headers=headers, json=body)

print(f"\nStatus: {response.status_code}")
data = response.json()
print(f"Hits: {len(data.get('hits', []))}")

if data.get('hits'):
    for hit in data['hits']:
        print(f"  - {hit.get('title', 'No title')}")
else:
    print("Response:", json.dumps(data, indent=2)[:500])
