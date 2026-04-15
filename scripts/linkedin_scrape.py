"""
LinkedIn scraper — 3 passes in priority order.

Pass 1: Expert profiles      → resources/LinkedIn-posts/[expert-slug]/
Pass 2: Topic + expert name  → resources/LinkedIn-posts/search-results/
Pass 3: Topic keywords only  → resources/other/linkedin-topic-search/

Usage:
    python scripts/linkedin_scrape.py --pass 1
    python scripts/linkedin_scrape.py --pass 2
    python scripts/linkedin_scrape.py --pass 3
    python scripts/linkedin_scrape.py --pass all
"""

import argparse
import os
import re
import json
import sys
from datetime import date, datetime
from pathlib import Path
from dotenv import load_dotenv
from apify_client import ApifyClient

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

load_dotenv()
APIFY_API_KEY = os.getenv("APIFY_API_KEY")
if not APIFY_API_KEY:
    sys.exit("ERROR: APIFY_API_KEY not found in .env")

TODAY = date.today().isoformat()
BASE = Path(__file__).parent.parent  # repo root

# Apify actor IDs
ACTOR_PROFILE  = "harvestapi/linkedin-profile-posts"   # Pass 1
ACTOR_SEARCH   = "harvestapi/linkedin-post-search"     # Pass 2 & 3

EXPERTS = [
    {"name": "Russell Brunson",  "slug": "russell-brunson",  "url": "https://www.linkedin.com/in/russellbrunson/"},
    {"name": "Jason Fladlien",   "slug": "jason-fladlien",   "url": "https://www.linkedin.com/in/jasonfladlien/"},
    {"name": "Alex Hormozi",     "slug": "alex-hormozi",      "url": "https://www.linkedin.com/in/alexhormozi/"},
    {"name": "Mariah Coz",       "slug": "mariah-coz",        "url": "https://www.linkedin.com/in/mariahcoz/"},
    {"name": "Melissa Kwan",     "slug": "melissa-kwan",      "url": "https://www.linkedin.com/in/melissakwan/"},
    {"name": "Pat Flynn",        "slug": "pat-flynn",         "url": "https://www.linkedin.com/in/patflynn/"},
    {"name": "Dama Jue",         "slug": "dama-jue",          "url": "https://www.linkedin.com/in/damajue/"},
    {"name": "Omar Zenhom",      "slug": "omar-zenhom",       "url": "https://www.linkedin.com/in/omarzenhom/"},
    {"name": "Alex Cattoni",     "slug": "alex-cattoni",      "url": "https://www.linkedin.com/in/alexcattoni/"},
    {"name": "Jon Penberthy",    "slug": "jon-penberthy",     "url": "https://www.linkedin.com/in/jonpenberthy/"},
]

PASS2_QUERIES = [
    {"query": '"Russell Brunson" webinar funnel',  "slug": "russell-brunson-webinar-funnel"},
    {"query": '"Jason Fladlien" webinar',           "slug": "jason-fladlien-webinar"},
    {"query": '"Alex Hormozi" webinar',             "slug": "alex-hormozi-webinar"},
    {"query": '"Mariah Coz" webinar',               "slug": "mariah-coz-webinar"},
    {"query": '"Melissa Kwan" webinar',             "slug": "melissa-kwan-webinar"},
    {"query": '"Pat Flynn" webinar',                "slug": "pat-flynn-webinar"},
    {"query": '"Dama Jue" webinar',                 "slug": "dama-jue-webinar"},
    {"query": '"Omar Zenhom" webinar',              "slug": "omar-zenhom-webinar"},
    {"query": '"Alex Cattoni" webinar',             "slug": "alex-cattoni-webinar"},
    {"query": '"Jon Penberthy" webinar',            "slug": "jon-penberthy-webinar"},
]

PASS3_QUERIES = [
    {"query": '"webinar funnel"',            "slug": "webinar-funnel"},
    {"query": '"webinar funnel from zero"',  "slug": "webinar-funnel-from-zero"},
    {"query": '"webinar registration page"', "slug": "webinar-registration-page"},
    {"query": '"webinar show up rate"',      "slug": "webinar-show-up-rate"},
    {"query": '"webinar email sequence"',    "slug": "webinar-email-sequence"},
    {"query": '"automated webinar funnel"',  "slug": "automated-webinar-funnel"},
    {"query": '"evergreen webinar"',         "slug": "evergreen-webinar"},
    {"query": '"webinar conversion rate"',   "slug": "webinar-conversion-rate"},
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

client = ApifyClient(APIFY_API_KEY)


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def make_frontmatter(title, author, author_slug, platform, source_url,
                     published_date, collection_method, query=None, tags=None):
    tags_str = json.dumps(tags or ["webinar-funnel", "linkedin"])
    q_line = f'search_query: "{query}"\n' if query else ""
    pub = published_date or "unknown"
    return (
        f"---\n"
        f'title: "{title}"\n'
        f'author: "{author}"\n'
        f'author_slug: "{author_slug}"\n'
        f'platform: "linkedin"\n'
        f'source_url: "{source_url}"\n'
        f'published_date: "{pub}"\n'
        f'collected_date: "{TODAY}"\n'
        f'{q_line}'
        f'collection_method: "{collection_method}"\n'
        f"tags: {tags_str}\n"
        f"---\n\n"
    )


def write_post_file(directory, filename, frontmatter, body):
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename
    if path.exists():
        print(f"  [skip] already exists: {path.relative_to(BASE)}")
        return
    path.write_text(frontmatter + body, encoding="utf-8")
    print(f"  [saved] {path.relative_to(BASE)}")


def run_actor(actor_id, run_input, label):
    print(f"\n  Running actor '{actor_id}' for: {label}")
    try:
        run = client.actor(actor_id).call(run_input=run_input, timeout_secs=300)
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        print(f"  Got {len(items)} items")
        return items
    except Exception as e:
        print(f"  ERROR running actor: {e}")
        return []


def extract_text(item):
    """Pull post body text from harvestapi result."""
    return (item.get("content") or "").strip()


def extract_author(item):
    """Pull author display name from harvestapi result."""
    author_obj = item.get("author") or {}
    if isinstance(author_obj, dict):
        name = author_obj.get("name", "").strip()
        if name:
            return name
    return "unknown"


def parse_post_date(item):
    """Extract date string from harvestapi postedAt field (which is a dict)."""
    val = item.get("postedAt") or item.get("createdAt") or {}
    if isinstance(val, dict):
        date_str = val.get("date", "")
        if date_str:
            return date_str[:10]
    elif isinstance(val, str) and val:
        return val[:10]
    return TODAY


# ---------------------------------------------------------------------------
# Pass 1 — Expert profiles
# ---------------------------------------------------------------------------

def run_pass1():
    print("\n=== PASS 1: Expert profiles ===")
    for expert in EXPERTS:
        items = run_actor(
            ACTOR_PROFILE,
            {"targetUrls": [expert["url"]], "maxPosts": 100},
            expert["name"],
        )
        out_dir = BASE / "resources" / "LinkedIn-posts" / expert["slug"]
        count = 0
        for item in items:
            text = extract_text(item)
            if not text:
                continue
            url   = item.get("linkedinUrl") or item.get("url") or expert["url"]
            pub   = parse_post_date(item)
            title_raw = text[:80].replace('"', "'")
            post_slug = slugify(text[:60])
            filename  = f"{pub}-{post_slug[:50]}.md"
            fm = make_frontmatter(
                title=title_raw,
                author=expert["name"],
                author_slug=expert["slug"],
                platform="linkedin",
                source_url=url,
                published_date=pub,
                collection_method="apify-linkedin-profile-scraper",
            )
            write_post_file(out_dir, filename, fm, text)
            count += 1
        print(f"  Saved {count} posts for {expert['name']}")


# ---------------------------------------------------------------------------
# Pass 2 — Topic + expert name
# ---------------------------------------------------------------------------

def run_pass2():
    print("\n=== PASS 2: Topic + expert name ===")
    out_dir = BASE / "resources" / "LinkedIn-posts" / "search-results"
    for q in PASS2_QUERIES:
        items = run_actor(
            ACTOR_SEARCH,
            {"searchQueries": [q["query"]], "maxPosts": 50},
            q["query"],
        )
        count = 0
        for item in items:
            text = extract_text(item)
            if not text:
                continue
            author_name = extract_author(item)
            author_slug = slugify(author_name) if author_name != "unknown" else "unknown"
            url  = item.get("linkedinUrl") or item.get("url") or ""
            pub  = parse_post_date(item)
            title_raw = text[:80].replace('"', "'")
            post_slug = slugify(text[:60])
            filename  = f"{pub}-{q['slug']}-{post_slug[:40]}.md"
            fm = make_frontmatter(
                title=title_raw,
                author=author_name,
                author_slug=author_slug,
                platform="linkedin",
                source_url=url,
                published_date=pub,
                collection_method="apify-linkedin-posts-search",
                query=q["query"],
                tags=["webinar-funnel", "linkedin", "expert-mention"],
            )
            write_post_file(out_dir, filename, fm, text)
            count += 1
        print(f"  Saved {count} posts for query: {q['query']}")


# ---------------------------------------------------------------------------
# Pass 3 — Topic keywords only
# ---------------------------------------------------------------------------

def run_pass3():
    print("\n=== PASS 3: Topic keywords only ===")
    out_dir = BASE / "resources" / "other" / "linkedin-topic-search"
    for q in PASS3_QUERIES:
        items = run_actor(
            ACTOR_SEARCH,
            {"searchQueries": [q["query"]], "maxPosts": 50},
            q["query"],
        )
        count = 0
        for item in items:
            text = extract_text(item)
            if not text:
                continue
            author_name = extract_author(item)
            author_slug = slugify(author_name) if author_name != "unknown" else "unknown"
            url  = item.get("linkedinUrl") or item.get("url") or ""
            pub  = parse_post_date(item)
            title_raw = text[:80].replace('"', "'")
            post_slug = slugify(text[:60])
            filename  = f"{pub}-{q['slug']}-{post_slug[:40]}.md"
            fm = make_frontmatter(
                title=title_raw,
                author=author_name,
                author_slug=author_slug,
                platform="linkedin",
                source_url=url,
                published_date=pub,
                collection_method="apify-linkedin-posts-search",
                query=q["query"],
                tags=["webinar-funnel", "linkedin", "keyword-search"],
            )
            write_post_file(out_dir, filename, fm, text)
            count += 1
        print(f"  Saved {count} posts for query: {q['query']}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pass", dest="run_pass", default="all",
                        choices=["1", "2", "3", "all"])
    args = parser.parse_args()

    if args.run_pass in ("1", "all"):
        run_pass1()
    if args.run_pass in ("2", "all"):
        run_pass2()
    if args.run_pass in ("3", "all"):
        run_pass3()

    print("\n=== All requested passes complete. Awaiting review. ===")
