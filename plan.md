# Research Plan: Webinar Funnel from Zero

**Project**: 100hires Evaluation Task  
**Researcher**: William Winata  
**Started**: 2026-04-14  
**Status**: Phase 3 — Content Collection (awaiting user content links)

---

## Objective

Map the best publicly available knowledge on building a webinar funnel from zero — covering registration pages, email sequences, show-up rate optimization, live delivery, and replay/follow-up sequences. The goal is to collect enough high-quality, practitioner-sourced material to support writing a real playbook later. Sources must be people who have actually run webinars and reported real results, not just theorists.

---

## Phases

### Phase 1: Expert Discovery
- **Status**: Complete
- **Completed**: 2026-04-14
- **Output**: `resources/sources.md` — 15+ candidate experts with quality gate scoring
- **Decision log**: See "Decisions and Trade-offs" section below

### Phase 2: User Review Checkpoint
- **Status**: Complete
- **Completed**: 2026-04-14
- **Feedback received**: User selected 10 of 17 candidates and added 2 new experts not in the original draft
- **Approved experts**: Russell Brunson, Jason Fladlien, Alex Hormozi, Mariah Coz, Melissa Kwan, Pat Flynn, Dama Jue, Omar Zenhom, Alex Cattoni, Jon Penberthy
- **Removed from draft**: Amy Porterfield, Todd Brown, Jon Schumacher, Sunny Lenarduzzi, Stu McLaren, Tarzan Kay, Navid Moazzez, Alyssa J. Dillon, Lewis Howes

### Phase 3: Content Collection
- **Status**: Not started
- **Collection log**:

| Expert | Platform | Items Planned | Items Collected | Status |
|--------|----------|--------------|----------------|--------|
| — | — | — | — | — |

### Phase 4: Repository Organization
- **Status**: Not started
- **Note**: Folder structure is created incrementally as content is added during Phase 3

### Phase 5: README Update
- **Status**: Not started

### Phase 6: Final Cleanup
- **Status**: Not started

---

## Repository Structure

```
William-cursor-AI-portfolio/
├── README.md                          (rewritten in Phase 5 to cover this project)
├── plan.md                            (this file)
├── .gitignore
├── scripts/
│   ├── README.md
│   ├── fetch_youtube_transcript.py
│   ├── batch_youtube.py
│   ├── fetch_webpage.py
│   └── config/
│       └── experts.json
└── resources/
    ├── sources.md
    ├── LinkedIn-posts/
    │   └── [author-slug]/
    │       └── [YYYY-MM-DD]-[post-slug].md
    ├── youtube-transcripts/
    │   └── [channel-slug]/
    │       └── [YYYY-MM-DD]-[video-slug].md
    └── other/
        └── [source-slug]/
            └── [YYYY-MM-DD]-[content-slug].md
```

**Naming conventions:**
- All slugs: lowercase, hyphen-separated, no spaces or special characters
- All content filenames prefixed with `YYYY-MM-DD`
- Example: `resources/youtube-transcripts/amy-porterfield/2024-03-15-webinar-funnel-from-scratch.md`

---

## Technical Stack

| Tool | Purpose |
|------|---------|
| `youtube-transcript-api` (Python) | Fetch YouTube auto-generated transcripts, no API key required |
| YouTube Data API v3 | Enrich transcript files with metadata (title, views, publish date) |
| Apify LinkedIn Posts Scraper | Collect LinkedIn posts within ToS constraints |
| `requests` + `BeautifulSoup4` (Python) | Fetch and parse podcast transcripts, blog posts, LinkedIn Articles |
| Python `venv` | Isolated environment, excluded from git |

**Setup:**
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install youtube-transcript-api requests beautifulsoup4 python-dotenv
```

---

## Content File Format

Every collected content file uses YAML frontmatter:

```markdown
---
title: "..."
author: "Amy Porterfield"
author_slug: "amy-porterfield"
platform: "youtube"
source_url: "https://..."
published_date: "2024-03-15"
collected_date: "2026-04-14"
transcript_type: "auto-generated"
collection_method: "youtube-transcript-api"
why_relevant: "Covers full funnel architecture with specific benchmarks at 24:30"
tags: ["webinar-funnel", "opt-in-page", "replay-sequence"]
---

[content here]
```

---

## LinkedIn Collection Approach

LinkedIn does not allow scraping under its ToS. Decision tree (in priority order):

1. **LinkedIn Articles/Newsletters** (public pages) → direct fetch with `requests`, no auth required
2. **Regular posts** → Apify LinkedIn Posts Scraper (free tier ~$5 credits/month)
3. **Fallback** → manual copy-paste, noted with `collection_method: manual`

Custom LinkedIn scrapers are out of scope — too brittle and ToS risk.

---

## Commit Strategy

One expert or one platform per commit. No giant dumps.

| Commit | Contents |
|--------|---------|
| 1 | `plan.md` + `resources/sources.md` draft (15+ candidates) |
| 2 | Updated `sources.md` after user review (approved final list) |
| 3+ | Per-expert content batches (e.g., "Add YouTube transcripts: Amy Porterfield") |
| N-1 | README rewrite |
| N | Final cleanup and plan.md status updates |

---

## Decisions and Trade-offs

- **15 candidates in initial draft**: Gives enough breadth for user to cull down to a strong final 6-10 without the list feeling constrained
- **Scripts committed to repo**: Demonstrates technical execution to evaluators; makes data pipeline transparent and reproducible
- **Apify for LinkedIn**: Prioritizes data collection reliability over building a fragile custom scraper; cost is negligible on free tier; approach is documented transparently
- **Auto-generated YouTube transcripts**: Not corrected for errors; this is noted in frontmatter. The volume and speed trade-off is worth it for a research pass

---

## Known Limitations

- LinkedIn scraping operates in a ToS grey area; Apify is used as the least-risky approach
- Auto-generated YouTube transcripts may contain errors; no manual correction applied
- Content represents a point-in-time snapshot; all collected dates are recorded in frontmatter
- Podcast audio without posted transcripts requires either show notes (proxy) or manual transcription of key segments
