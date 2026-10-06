import json

with open('scratch/posts_for_mockup.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

# Let's verify we have the posts
print(f"Loaded {len(posts)} posts for the mockup template.")
