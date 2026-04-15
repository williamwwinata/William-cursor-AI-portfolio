"""
One-time fix: rename LinkedIn post files that have {'timestam prefix in filename
and fix published_date in frontmatter.

These were saved before parse_post_date was fixed. We use the collected_date
(2026-04-15) as the published_date fallback since the actual post date is unavailable
without re-fetching from Apify.

Usage: python scripts/fix_linkedin_dates.py
"""

import re
from pathlib import Path

BASE = Path(__file__).parent.parent
DIRS = [
    BASE / "resources" / "LinkedIn-posts",
    BASE / "resources" / "other" / "linkedin-topic-search",
]

BAD_PREFIX = "{'timestam"
FALLBACK_DATE = "unknown"

renamed = 0
fixed = 0

for search_dir in DIRS:
    for md_file in search_dir.rglob("*.md"):
        name = md_file.name

        # Fix frontmatter published_date
        content = md_file.read_text(encoding="utf-8")
        new_content = re.sub(
            r"published_date: \"[^\"]*\{[^\"]*\"",
            f'published_date: "{FALLBACK_DATE}"',
            content,
        )
        if new_content != content:
            md_file.write_text(new_content, encoding="utf-8")
            fixed += 1

        # Rename file if it has the bad prefix
        if name.startswith(BAD_PREFIX):
            new_name = name[len(BAD_PREFIX):].lstrip("-")
            new_name = f"{FALLBACK_DATE}-{new_name}"
            new_path = md_file.parent / new_name
            if new_path.exists():
                # avoid collision: add suffix
                new_path = md_file.parent / f"{FALLBACK_DATE}-dup-{new_name}"
            md_file.rename(new_path)
            renamed += 1

print(f"Renamed {renamed} files, fixed frontmatter in {fixed} files.")
