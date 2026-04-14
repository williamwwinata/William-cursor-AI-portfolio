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

- **Status**: Pre-flight analysis complete — awaiting user command to begin
- **Collection log**:

| Expert | Platform | Items Planned | Items Collected | Status |
|--------|----------|--------------|----------------|--------|
| Russell Brunson | Blog (clickfunnels.com) | 8 | 0 | Pending |
| Jason Fladlien | YouTube | 9 | 0 | Pending |
| Alex Hormozi | YouTube | 1 | 0 | Pending |
| Mariah Coz | Blog (mariahcoz.com) | 7 | 0 | Pending |
| Melissa Kwan | Blog (ewebinar.com) | 17 | 0 | Pending |
| Pat Flynn | YouTube | 1 | 0 | Pending |
| Dama Jue | Podcast page (heartsoulhustle.com) | 1 | 0 | Flagged — see below |
| Omar Zenhom | Blog (webinarninja.com) | 18 | 0 | Pending |
| Alex Cattoni | YouTube + Blog (copyposse.com) | 3 | 0 | Pending |
| Jon Penberthy | YouTube | 4 | 0 | Pending |

**Totals**: 16 YouTube videos · 52 blog posts · 3 podcast-embed pages flagged

---

#### Scrapability Assessment (blogs)

| Domain | Scrapable? | Method | Notes |
|--------|-----------|--------|-------|
| clickfunnels.com/blog | Yes | requests + BS4 | Standard HTML blog. Two posts (`podcast-696`, `podcast-670`) are podcast episode pages — flagged for audio handling |
| mariahcoz.com/blog | Yes | requests + BS4 | Standard WordPress/personal blog |
| ewebinar.com/blog | Yes | requests + BS4 | Company blog, standard HTML |
| webinarninja.com/blog | Yes | requests + BS4 | Company blog, standard HTML |
| copyposse.com/blog | Yes | requests + BS4 | Brand blog, standard HTML |
| heartsoulhustle.com/blogs | TBD | requests + BS4 | Podcast episode page — check for written transcript first; may be audio-only embed |

---

#### Podcast Audio — Flagged Pages (3 total)

These links point to podcast episode pages that may contain embedded audio with no written transcript:

1. `clickfunnels.com/blog/podcast-696-peter-pru` (Russell Brunson)
2. `clickfunnels.com/blog/podcast-670-tim-shields` (Russell Brunson)
3. `heartsoulhustle.com/blogs/episode-077-...` (Dama Jue)

**Handling flow:**
1. Fetch page with requests + BS4 → check for written transcript or full show notes text
2. If text exists → scrape as normal blog post
3. If audio-only embed → use an audio transcription API (see options below) or prompt user

**Audio transcription API**: Deepgram (confirmed by user)
- REST API, ~$0.0043/min (~$0.26/hr), fastest turnaround
- Key stored in `.env` as `DEEPGRAM_API_KEY`, never committed

---

#### Phase 3 Sequence — Planned Order

1. **LinkedIn keyword search** (next up) — scrape public posts matching "webinar funnel from zero" and related queries across LinkedIn broadly, not limited to the 10 experts
2. **YouTube transcripts** — Supadata API for all 16 videos
3. **Blog scraping** — requests + BS4 for all 52 blog posts
4. **Podcast pages** — handle flagged pages after user decides on audio transcription API

---

#### LinkedIn Keyword Search — Plan

**Goal**: Find publicly available LinkedIn posts from practitioners discussing webinar funnels. Not profile-specific — this is a broad keyword sweep to surface posts that may not have been caught in the expert discovery phase.

**Search queries to run** (in priority order):
1. `"webinar funnel"`
2. `"webinar funnel from zero"`
3. `"webinar registration page"`
4. `"webinar show up rate"`
5. `"webinar email sequence"`
6. `"automated webinar funnel"`
7. `"evergreen webinar"`
8. `"webinar conversion rate"`

**Tool options:**

| Tool | Type | Cost | Notes |
|------|------|------|-------|
| **Apify — LinkedIn Posts Search Scraper** | Cloud actor (REST API) | Free tier ~$5 credits (~200-500 posts) | Already in plan; input: keyword query; output: post text, author, date, likes, URL. Most reliable option. |
| **Apify — LinkedIn Profile Scraper** | Cloud actor (REST API) | Same free tier | Scrapes posts from specific profiles — useful for the 10 experts' LinkedIn presence |
| **Proxycurl API** | REST API | $0.01-0.10/request | Clean API, higher cost, better for profile data than post search |
| **SerpApi (Google dorking)** | REST API | Free tier 100 searches/mo | Queries `site:linkedin.com/posts "webinar funnel"` via Google — gets indexed posts only, misses recent |
| **PhantomBuster** | Browser automation | Free trial | Requires LinkedIn login; ToS risk higher than Apify |

**Recommendation**: Use **Apify** for both passes:
- Pass 1: LinkedIn Posts Search Scraper → keyword queries above → broad post discovery
- Pass 2: LinkedIn Profile Scraper → the 10 experts' profiles → capture any expert LinkedIn posts missed in expert-specific collection

**Setup**: Apify API key confirmed by user → stored in `.env` as `APIFY_API_KEY`, never committed

**Output location**: `resources/LinkedIn-posts/search-results/[YYYY-MM-DD]-[query-slug].md`

**Awaiting user command to begin.**

---

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
| Supadata API (primary) | Fetch YouTube transcripts via REST API; key in `.env` |
| `youtube-transcript-api` (Python fallback) | Fallback if Supadata fails; no API key required |
| Apify LinkedIn Posts Search Scraper | Keyword search across LinkedIn posts; key in `.env` |
| Apify LinkedIn Profile Scraper | Scrape posts from each expert's LinkedIn profile; same key |
| Deepgram API | Transcribe podcast audio if episode pages are audio-only; key in `.env` |
| `requests` + `BeautifulSoup4` (Python) | Fetch and parse blog posts, podcast pages |
| Python `venv` | Isolated environment, excluded from git |


**YouTube transcript flow:**

1. Call Supadata API with video URL → success → write transcript file
2. If Supadata fails → prompt user for next step (manual copy-paste or fallback library)

**Setup:**

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install requests beautifulsoup4 python-dotenv
# Copy .env.example to .env and fill in SUPADATA_API_KEY
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


| Commit | Contents                                                                      |
| ------ | ----------------------------------------------------------------------------- |
| 1      | `plan.md` + `resources/sources.md` draft (15+ candidates)                     |
| 2      | Updated `sources.md` after user review (approved final list)                  |
| 3+     | Per-expert content batches (e.g., "Add YouTube transcripts: Amy Porterfield") |
| N-1    | README rewrite                                                                |
| N      | Final cleanup and plan.md status updates                                      |


---

## Decisions and Trade-offs

- **15 candidates in initial draft**: Gives enough breadth for user to cull down to a strong final 10 without the list feeling constrained
- **Scripts committed to repo**: Demonstrates technical execution to evaluators; makes data pipeline transparent and reproducible
- **Apify for LinkedIn**: Prioritizes data collection reliability over building a fragile custom scraper; cost is negligible on free tier; approach is documented transparently
- **Auto-generated YouTube transcripts**: Not corrected for errors; this is noted in frontmatter. The volume and speed trade-off is worth it for a research pass

---

## Known Limitations

- LinkedIn scraping operates in a ToS grey area; Apify is used as the least-risky approach
- Auto-generated YouTube transcripts may contain errors; no manual correction applied
- Content represents a point-in-time snapshot; all collected dates are recorded in frontmatter
- Podcast audio without posted transcripts requires either show notes (proxy) or manual transcription of key segments

