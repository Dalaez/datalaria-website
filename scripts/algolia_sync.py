"""
Algolia Sync Script for Datalaria
==================================
Exports Hugo blog posts to Algolia for RAG-powered search.

Usage:
    python algolia_sync.py              # Sync all posts to Algolia
    python algolia_sync.py --dry-run    # Preview without uploading
    python algolia_sync.py --lang en    # Only sync English posts
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import frontmatter
from bs4 import BeautifulSoup
from markdown import markdown
from algoliasearch.search.client import SearchClientSync
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CONTENT_BASE = Path(__file__).parent.parent / "content"
SUPPORTED_LANGS = ["en", "es"]


class AlgoliaExporter:
    """
    Exports Hugo markdown posts to Algolia-compatible JSON records.
    Designed for RAG (Retrieval Augmented Generation) use cases.
    """

    def __init__(self, app_id: str, api_key: str, index_name: str):
        self.client = SearchClientSync(app_id, api_key)
        self.index_name = index_name
        
    def clean_markdown(self, content: str) -> str:
        """
        Remove Hugo shortcodes and convert markdown to plain text.
        Preserves meaningful content for semantic search.
        """
        # Remove Hugo shortcodes like {{< youtube ... >}}, {{< mermaid >}}, etc.
        content = re.sub(r'\{\{[<>%].*?[%>]\}\}', '', content, flags=re.DOTALL)
        
        # Remove code blocks (keep description, not implementation details)
        content = re.sub(r'```[\s\S]*?```', '[code block]', content)
        
        # Convert markdown to HTML, then extract text
        html = markdown(content)
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_post_data(self, file_path: Path, lang: str) -> dict | None:
        """
        Parse a Hugo markdown file and extract structured data for Algolia.
        
        Returns:
            dict with Algolia record structure, or None if post is draft/invalid
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
            return None
        
        # Skip drafts
        if post.metadata.get('draft', False):
            return None
        
        # Extract slug from directory name (Hugo page bundle pattern)
        if file_path.name.lower() == 'index.md':
            slug = file_path.parent.name
        else:
            slug = file_path.stem
        
        # Build canonical URL
        base_url = "https://datalaria.com"
        url = f"{base_url}/{lang}/posts/{slug}/"
        
        # Clean content for search
        clean_content = self.clean_markdown(post.content)
        
        # Limit content length (Algolia recommends < 10KB per record)
        # Keep first 5000 chars for relevance while staying within limits
        content_preview = clean_content[:5000]
        
        # Extract categories and tags
        categories = post.metadata.get('categories', [])
        tags = post.metadata.get('tags', [])
        
        # Parse date
        date_raw = post.metadata.get('date', '')
        if isinstance(date_raw, datetime):
            date_str = date_raw.strftime('%Y-%m-%d')
            timestamp = int(date_raw.timestamp())
        elif isinstance(date_raw, str):
            date_str = date_raw[:10]  # YYYY-MM-DD
            try:
                timestamp = int(datetime.fromisoformat(date_str).timestamp())
            except:
                timestamp = 0
        else:
            date_str = str(date_raw)[:10] if date_raw else ''
            timestamp = 0
        
        # Determine content domain (for Operations Engineering pillars)
        domain = self._classify_domain(categories, tags, post.metadata.get('title', ''))
        
        return {
            "objectID": f"{lang}_{slug}",  # Unique ID per language
            "title": post.metadata.get('title', 'Untitled'),
            "description": post.metadata.get('description', ''),
            "content": content_preview,
            "url": url,
            "slug": slug,
            "lang": lang,
            "categories": categories if isinstance(categories, list) else [categories],
            "tags": tags if isinstance(tags, list) else [tags],
            "date": date_str,
            "timestamp": timestamp,
            "domain": domain,  # S&OP, Product, Projects, People
            "image": post.metadata.get('image', ''),
        }
    
    def _classify_domain(self, categories: list, tags: list, title: str) -> str:
        """
        Classify post into one of the 4 Operations Engineering pillars.
        """
        all_keywords = ' '.join(categories + tags + [title]).lower()
        
        # S&OP keywords
        if any(kw in all_keywords for kw in ['s&op', 'sop', 'supply chain', 'demand', 'forecast', 'hygiene', 'outlier']):
            return 'S&OP'
        
        # Projects keywords
        if any(kw in all_keywords for kw in ['project', 'devops', 'automation', 'pipeline', 'github', 'ci/cd', 'agile']):
            return 'Projects'
        
        # People keywords
        if any(kw in all_keywords for kw in ['team', 'onboarding', 'meeting', 'collaboration', 'people', 'hiring']):
            return 'People'
        
        # Product keywords
        if any(kw in all_keywords for kw in ['product', 'feature', 'roadmap', 'user', 'customer', 'design']):
            return 'Product'
        
        # Default to general if no specific domain
        return 'General'
    
    def collect_posts(self, langs: list[str] = None) -> list[dict]:
        """
        Traverse content directories and collect all valid posts.
        
        Args:
            langs: List of language codes to process. If None, process all.
        """
        if langs is None:
            langs = SUPPORTED_LANGS
        
        records = []
        
        for lang in langs:
            posts_dir = CONTENT_BASE / lang / "posts"
            
            if not posts_dir.exists():
                print(f"⚠️  Posts directory not found: {posts_dir}")
                continue
            
            # Find all index.md files in page bundles
            for post_path in posts_dir.glob("*/index.md"):
                record = self.extract_post_data(post_path, lang)
                if record:
                    records.append(record)
                    print(f"✅ [{lang}] {record['title'][:50]}...")
            
            # Also check for standalone .md files (non-bundle pattern)
            for post_path in posts_dir.glob("*.md"):
                if post_path.name.startswith('_'):  # Skip _index.md
                    continue
                record = self.extract_post_data(post_path, lang)
                if record:
                    records.append(record)
                    print(f"✅ [{lang}] {record['title'][:50]}...")
        
        return records
    
    def sync_to_algolia(self, records: list[dict]) -> dict:
        """
        Upload records to Algolia index.
        Uses saveObjects which handles both create and update.
        
        Returns:
            Algolia response with task info
        """
        if not records:
            print("⚠️  No records to sync")
            return {}
        
        print(f"\n📤 Uploading {len(records)} records to Algolia...")
        
        response = self.client.save_objects(
            index_name=self.index_name,
            objects=records
        )
        
        print(f"✅ Sync complete!")
        return response
    
    def configure_index(self):
        """
        Configure Algolia index settings for optimal search.
        Should be run once during initial setup.
        """
        print("⚙️  Configuring index settings...")
        
        settings = {
            # Searchable attributes (in priority order)
            "searchableAttributes": [
                "title",
                "description", 
                "content",
                "categories",
                "tags"
            ],
            # Attributes for faceting/filtering
            "attributesForFaceting": [
                "searchable(lang)",
                "searchable(domain)",
                "searchable(categories)",
                "searchable(tags)"
            ],
            # Attributes to retrieve
            "attributesToRetrieve": [
                "title",
                "description",
                "url",
                "lang",
                "domain",
                "categories",
                "tags",
                "date",
                "image"
            ],
            # Attributes for snippeting (content preview in results)
            "attributesToSnippet": [
                "content:50"
            ],
            # Ranking and sorting
            "customRanking": [
                "desc(timestamp)"  # Newer posts first
            ],
            # Highlighting
            "highlightPreTag": "<mark>",
            "highlightPostTag": "</mark>",
        }
        
        self.client.set_settings(
            index_name=self.index_name,
            index_settings=settings
        )
        
        print("✅ Index configured!")


def main():
    parser = argparse.ArgumentParser(
        description="Sync Datalaria posts to Algolia for RAG search"
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help="Preview records without uploading to Algolia"
    )
    parser.add_argument(
        '--lang',
        choices=['en', 'es', 'all'],
        default='all',
        help="Language to sync (default: all)"
    )
    parser.add_argument(
        '--configure',
        action='store_true',
        help="Configure index settings (run once during setup)"
    )
    parser.add_argument(
        '--output',
        type=str,
        help="Save records to JSON file (for debugging)"
    )
    
    args = parser.parse_args()
    
    # Validate environment
    app_id = os.getenv('ALGOLIA_APP_ID')
    api_key = os.getenv('ALGOLIA_WRITE_API_KEY')
    index_name = os.getenv('ALGOLIA_INDEX_NAME', 'datalaria_posts')
    
    if not app_id or not api_key:
        print("❌ Missing ALGOLIA_APP_ID or ALGOLIA_WRITE_API_KEY in environment")
        print("   Copy scripts/.env.example to scripts/.env and fill in your credentials")
        sys.exit(1)
    
    print(f"🔍 Algolia App: {app_id}")
    print(f"📚 Index: {index_name}")
    print(f"📁 Content: {CONTENT_BASE}")
    print()
    
    # Initialize exporter
    exporter = AlgoliaExporter(app_id, api_key, index_name)
    
    # Configure index if requested
    if args.configure:
        exporter.configure_index()
        return
    
    # Determine languages to process
    langs = SUPPORTED_LANGS if args.lang == 'all' else [args.lang]
    
    # Collect posts
    print(f"📖 Collecting posts ({', '.join(langs)})...\n")
    records = exporter.collect_posts(langs)
    
    print(f"\n📊 Found {len(records)} posts total")
    
    # Group by domain for summary
    domains = {}
    for r in records:
        d = r['domain']
        domains[d] = domains.get(d, 0) + 1
    
    print("\n🏷️  By Domain:")
    for domain, count in sorted(domains.items()):
        print(f"   {domain}: {count}")
    
    # Save to JSON if requested
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Saved to {args.output}")
    
    # Dry run mode
    if args.dry_run:
        print("\n🚧 DRY RUN - No changes made to Algolia")
        print("\n📋 Sample record:")
        if records:
            sample = records[0].copy()
            sample['content'] = sample['content'][:200] + '...'
            print(json.dumps(sample, indent=2, ensure_ascii=False))
        return
    
    # Sync to Algolia
    exporter.sync_to_algolia(records)
    
    print(f"\n🎉 Successfully synced {len(records)} posts to Algolia!")
    print(f"   View in dashboard: https://dashboard.algolia.com/apps/{app_id}/explorer/browse/{index_name}")


if __name__ == "__main__":
    main()
