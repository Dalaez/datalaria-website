"""Test with SEARCH key specifically"""
from algoliasearch.search.client import SearchClientSync
import os

app_id = 'C4NV3SCYAM'
search_key = '0130e86396a12b79b35c8cf37b692258'  # The Search API Key

print(f"Testing with SEARCH API Key: {search_key[:8]}...")

client = SearchClientSync(app_id, search_key)

# Test search
print("\nSearching for 'outliers'...")
try:
    results = client.search_single_index('datalaria_posts', {
        'query': 'outliers',
        'hitsPerPage': 5
    })
    print(f"Found {len(results.hits)} hits")
    for hit in results.hits:
        print(f"  - {hit.title}")
except Exception as e:
    print(f"ERROR: {e}")
