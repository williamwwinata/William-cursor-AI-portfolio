"""
YouTube transcript scraper — fetches transcripts for all 16 planned videos.

Uses Supadata API (primary). If Supadata fails for a video, logs it and continues.

Usage:
    python scripts/youtube_transcripts.py

Output: resources/youtube-transcripts/[expert-slug]/[video-id]-[slug].md
"""

import os
import re
import json
import requests
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

SUPADATA_KEY = os.getenv("SUPADATA_API_KEY")
if not SUPADATA_KEY:
    raise SystemExit("ERROR: SUPADATA_API_KEY not found in .env")

TODAY = date.today().isoformat()
BASE  = Path(__file__).parent.parent

VIDEOS = [
    # --- Jason Fladlien (9) ---
    {"expert": "Jason Fladlien", "slug": "jason-fladlien", "url": "https://www.youtube.com/watch?v=AwZbMUoRKcg"},
    {"expert": "Jason Fladlien", "slug": "jason-fladlien", "url": "https://www.youtube.com/watch?v=mWdIrgCCWYw"},
    {"expert": "Jason Fladlien", "slug": "jason-fladlien", "url": "https://www.youtube.com/watch?v=YFssGxdN5-c"},
    {"expert": "Jason Fladlien", "slug": "jason-fladlien", "url": "https://www.youtube.com/watch?v=JbKDmeFibZ4"},
    {"expert": "Jason Fladlien", "slug": "jason-fladlien", "url": "https://www.youtube.com/watch?v=H_TvNSNbRiU"},
    {"expert": "Jason Fladlien", "slug": "jason-fladlien", "url": "https://www.youtube.com/watch?v=oCMGvn1evl4"},
    {"expert": "Jason Fladlien", "slug": "jason-fladlien", "url": "https://www.youtube.com/watch?v=imAIf-q9uN8"},
    {"expert": "Jason Fladlien", "slug": "jason-fladlien", "url": "https://www.youtube.com/watch?v=VEqCCgbvdek"},
    {"expert": "Jason Fladlien", "slug": "jason-fladlien", "url": "https://www.youtube.com/watch?v=g1qYfu42VRQ"},
    # --- Alex Hormozi (1) ---
    {"expert": "Alex Hormozi", "slug": "alex-hormozi", "url": "https://www.youtube.com/watch?v=k4HdBsf6woY"},
    # --- Pat Flynn (1) ---
    {"expert": "Pat Flynn", "slug": "pat-flynn", "url": "https://www.youtube.com/watch?v=gXixgxLSuTU"},
    # --- Alex Cattoni (1) ---
    {"expert": "Alex Cattoni", "slug": "alex-cattoni", "url": "https://www.youtube.com/watch?v=4yERUa0Aktc"},
    # --- Jon Penberthy (4) ---
    {"expert": "Jon Penberthy", "slug": "jon-penberthy", "url": "https://www.youtube.com/watch?v=uTIoiNtIJVY"},
    {"expert": "Jon Penberthy", "slug": "jon-penberthy", "url": "https://www.youtube.com/watch?v=HcM8hqzXCKM"},
    {"expert": "Jon Penberthy", "slug": "jon-penberthy", "url": "https://www.youtube.com/watch?v=zbVybf_0ecM"},
    {"expert": "Jon Penberthy", "slug": "jon-penberthy", "url": "https://www.youtube.com/watch?v=of4VhEHP2bs"},
]


def video_id(url):
    m = re.search(r"v=([A-Za-z0-9_-]{11})", url)
    return m.group(1) if m else url.split("/")[-1]


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def fetch_transcript(url):
    """Call Supadata API. Returns (content, lang) or raises on failure."""
    resp = requests.get(
        "https://api.supadata.ai/v1/youtube/transcript",
        headers={"x-api-key": SUPADATA_KEY},
        params={"url": url, "text": "true"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("content", ""), data.get("lang", "unknown")


def fetch_video_title(url):
    """Get video title via Supadata /metadata endpoint."""
    try:
        resp = requests.get(
            "https://api.supadata.ai/v1/metadata",
            headers={"x-api-key": SUPADATA_KEY},
            params={"url": url},
            timeout=15,
        )
        if resp.status_code == 200:
            return resp.json().get("title", "")
    except Exception:
        pass
    return ""


def make_frontmatter(title, expert, expert_slug, url, vid_id, lang):
    safe_title = title.replace('"', "'") if title else f"YouTube — {vid_id}"
    return (
        f"---\n"
        f'title: "{safe_title}"\n'
        f'author: "{expert}"\n'
        f'author_slug: "{expert_slug}"\n'
        f'platform: "youtube"\n'
        f'source_url: "{url}"\n'
        f'video_id: "{vid_id}"\n'
        f'published_date: "unknown"\n'
        f'collected_date: "{TODAY}"\n'
        f'transcript_lang: "{lang}"\n'
        f'transcript_type: "auto-generated"\n'
        f'collection_method: "supadata-api"\n'
        f'tags: ["webinar-funnel", "youtube"]\n'
        f"---\n\n"
    )


def run():
    failed = []
    saved  = 0

    for video in VIDEOS:
        url      = video["url"]
        expert   = video["expert"]
        slug     = video["slug"]
        vid      = video_id(url)
        out_dir  = BASE / "resources" / "youtube-transcripts" / slug
        out_dir.mkdir(parents=True, exist_ok=True)

        # Check if already collected
        existing = list(out_dir.glob(f"{vid}-*.md"))
        if existing:
            print(f"  [skip] {expert} — {vid} (already exists)")
            saved += 1
            continue

        print(f"  Fetching: {expert} — {vid} ...", end=" ", flush=True)
        try:
            content, lang = fetch_transcript(url)
            if not content:
                raise ValueError("Empty transcript returned")

            title = fetch_video_title(url)
            title_slug = slugify(title[:60]) if title else vid
            filename = f"{vid}-{title_slug}.md"
            fm = make_frontmatter(title, expert, slug, url, vid, lang)
            path = out_dir / filename
            path.write_text(fm + content, encoding="utf-8")
            print(f"OK ({len(content):,} chars) -> {path.relative_to(BASE)}")
            saved += 1

        except Exception as e:
            print(f"FAILED — {e}")
            failed.append({"expert": expert, "url": url, "error": str(e)})

    print(f"\n=== Done: {saved} saved, {len(failed)} failed ===")
    if failed:
        print("\nFailed videos:")
        for f in failed:
            print(f"  {f['expert']} — {f['url']}")
            print(f"    Error: {f['error']}")
    print("\nAwaiting review.")


if __name__ == "__main__":
    run()
