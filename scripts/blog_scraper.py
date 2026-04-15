"""
Blog scraper — fetches 52 blog posts + 3 flagged podcast pages.

Uses requests + BeautifulSoup4. Domain-specific content selectors tuned per site.

Usage:
    python scripts/blog_scraper.py

Output: resources/other/blog-posts/[expert-slug]/[slug].md
"""

import os
import re
import time
import requests
from datetime import date
from pathlib import Path
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

TODAY   = date.today().isoformat()
BASE    = Path(__file__).parent.parent
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"}

# ---------------------------------------------------------------------------
# Domain → content selector (tuned from pre-flight inspection)
# ---------------------------------------------------------------------------
SELECTORS = {
    "clickfunnels.com": ".entry-content",
    "mariahcoz.com":    "div.route",
    "ewebinar.com":     ".blog_post_body",
    "webinarninja.com": "article",
    "copyposse.com":    ".single-post",
    "heartsoulhustle.com": "article",
}

# ---------------------------------------------------------------------------
# Blog post list
# ---------------------------------------------------------------------------
POSTS = [
    # --- Russell Brunson / ClickFunnels (8) ---
    {"expert": "Russell Brunson", "slug": "russell-brunson", "url": "https://www.clickfunnels.com/blog/webinar-marketing-funnel/"},
    {"expert": "Russell Brunson", "slug": "russell-brunson", "url": "https://www.clickfunnels.com/blog/how-to-pre-sell-your-course-idea-with-a-webinar-funnel/"},
    {"expert": "Russell Brunson", "slug": "russell-brunson", "url": "https://www.clickfunnels.com/blog/podcast-696-peter-pru/", "flagged": "podcast"},
    {"expert": "Russell Brunson", "slug": "russell-brunson", "url": "https://www.clickfunnels.com/blog/podcast-670-tim-shields/", "flagged": "podcast"},
    {"expert": "Russell Brunson", "slug": "russell-brunson", "url": "https://www.clickfunnels.com/blog/how-to-create-webinar-that-converts-viewers-into-buyers/"},
    {"expert": "Russell Brunson", "slug": "russell-brunson", "url": "https://www.clickfunnels.com/blog/one-guide-successful-webinar-funnel-part-1/"},
    {"expert": "Russell Brunson", "slug": "russell-brunson", "url": "https://www.clickfunnels.com/blog/one-guide-successful-webinar-funnel-part-2/"},
    {"expert": "Russell Brunson", "slug": "russell-brunson", "url": "https://www.clickfunnels.com/blog/one-guide-successful-webinar-funnel-part-3/"},
    # --- Mariah Coz (7) ---
    {"expert": "Mariah Coz", "slug": "mariah-coz", "url": "https://mariahcoz.com/blog/make-money-with-webinars"},
    {"expert": "Mariah Coz", "slug": "mariah-coz", "url": "https://mariahcoz.com/blog/how-to-create-a-webinar-free"},
    {"expert": "Mariah Coz", "slug": "mariah-coz", "url": "https://mariahcoz.com/blog/increase-webinar-registrations"},
    {"expert": "Mariah Coz", "slug": "mariah-coz", "url": "https://mariahcoz.com/blog/how-to-host-a-webinar"},
    {"expert": "Mariah Coz", "slug": "mariah-coz", "url": "https://mariahcoz.com/blog/pick-a-webinar-topic"},
    {"expert": "Mariah Coz", "slug": "mariah-coz", "url": "https://mariahcoz.com/blog/evergreen-webinar-mindset-blocks"},
    {"expert": "Mariah Coz", "slug": "mariah-coz", "url": "https://mariahcoz.com/blog/how-to-validate-your-online-course-idea-with-a-webinar"},
    # --- Melissa Kwan / eWebinar (17) ---
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/webinar-checklist"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/webinar-outline"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/webinar-agenda"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/how-to-moderate-a-webinar"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/live-vs-pre-recorded-webinar"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/webinar-engagement-strategies"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/webinar-lead-generation"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/what-is-an-automated-webinar"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/webinars-on-autopilot"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/webinar-registration-form"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/high-converting-webinar-landing-page"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/best-webinar-platforms-for-small-business"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/types-of-webinar-software"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/webinar-series-platform"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/just-in-time-webinar"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/webinar-replay"},
    {"expert": "Melissa Kwan", "slug": "melissa-kwan", "url": "https://ewebinar.com/blog/asynchronous-webinar"},
    # --- Omar Zenhom / WebinarNinja (18) ---
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/webinar-funnel/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/interactive-webinar-platforms/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/how-to-moderate-a-webinar/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/event-marketing-webinar/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/webinar-statistics/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/webinar-invitation/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/webinar-content-syndication/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/simulive-webinars/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/webinar-etiquette/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/white-label-webinars/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/webinar-branding/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/automated-webinar-funnel/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/webinar-costs/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/webinar-target-audience/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/webinar-titles/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/webinar-challenges/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/repurpose-webinar-content/"},
    {"expert": "Omar Zenhom", "slug": "omar-zenhom", "url": "https://webinarninja.com/blog/webinar-mistakes/"},
    # --- Alex Cattoni / CopyPosse (2 blog posts; YouTube already done) ---
    {"expert": "Alex Cattoni", "slug": "alex-cattoni", "url": "https://copyposse.com/blog/the-ultimate-webinar-funnel-everything-you-need-to-do-from-start-to-finish/"},
    {"expert": "Alex Cattoni", "slug": "alex-cattoni", "url": "https://copyposse.com/blog/proven-copywriting-formula-that-works-for-webinars/"},
    # --- Dama Jue / Heart Soul Hustle (1 flagged podcast page) ---
    {"expert": "Dama Jue", "slug": "dama-jue", "url": "https://www.heartsoulhustle.com/blogs/episode-077-unconventional-marketing-that-works-with-dama-jue", "flagged": "podcast"},
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def url_slug(url):
    path = url.rstrip("/").split("/")[-1]
    return slugify(path)[:70]


def get_selector(url):
    for domain, sel in SELECTORS.items():
        if domain in url:
            return sel
    return "article"


def extract_content(soup, selector):
    """Extract text using selector, fall back to <main>, then <body>."""
    el = soup.select_one(selector)
    if not el:
        el = soup.find("main") or soup.find("body")
    if not el:
        return "", 0
    # Remove nav, header, footer, script, style noise
    for tag in el.find_all(["nav", "header", "footer", "script", "style", "aside"]):
        tag.decompose()
    text = el.get_text("\n", strip=True)
    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip(), len(text.split())


def extract_title(soup):
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].strip()
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    title = soup.find("title")
    return title.get_text(strip=True) if title else ""


def make_frontmatter(title, expert, slug, url, method, flagged=False):
    safe_title = title.replace('"', "'")
    flag_line  = f'flagged: "podcast-page"\n' if flagged else ""
    return (
        f"---\n"
        f'title: "{safe_title}"\n'
        f'author: "{expert}"\n'
        f'author_slug: "{slug}"\n'
        f'platform: "blog"\n'
        f'source_url: "{url}"\n'
        f'published_date: "unknown"\n'
        f'collected_date: "{TODAY}"\n'
        f'collection_method: "{method}"\n'
        f'{flag_line}'
        f'tags: ["webinar-funnel", "blog"]\n'
        f"---\n\n"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run():
    saved   = 0
    skipped = 0
    failed  = []

    for post in POSTS:
        url     = post["url"]
        expert  = post["expert"]
        slug    = post["slug"]
        flagged = post.get("flagged") == "podcast"
        uslug   = url_slug(url)
        out_dir = BASE / "resources" / "other" / "blog-posts" / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{uslug}.md"

        if out_path.exists():
            print(f"  [skip] {expert} -- {uslug}")
            skipped += 1
            continue

        print(f"  Fetching: {expert} -- {uslug} ...", end=" ", flush=True)
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            r.raise_for_status()
            soup     = BeautifulSoup(r.text, "html.parser")
            selector = get_selector(url)
            text, wc = extract_content(soup, selector)

            if wc < 50:
                raise ValueError(f"Too little text extracted ({wc} words) with selector '{selector}'")

            title  = extract_title(soup)
            method = "requests-bs4-podcast-page" if flagged else "requests-bs4"
            fm     = make_frontmatter(title, expert, slug, url, method, flagged)
            out_path.write_text(fm + text, encoding="utf-8")
            flag_note = " [podcast page]" if flagged else ""
            print(f"OK ({wc:,} words){flag_note}")
            saved += 1

        except Exception as e:
            print(f"FAILED -- {e}")
            failed.append({"expert": expert, "url": url, "error": str(e)})

        time.sleep(0.5)  # polite crawl delay

    print(f"\n=== Done: {saved} saved, {skipped} skipped, {len(failed)} failed ===")
    if failed:
        print("\nFailed:")
        for f in failed:
            print(f"  {f['expert']} -- {f['url']}")
            print(f"    {f['error']}")
    print("\nAwaiting review.")


if __name__ == "__main__":
    run()
