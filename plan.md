# Research Plan: Webinar Funnel from Zero

**Project**: 100hires Evaluation Task  
**Researcher**: William Winata  
**Started**: 2026-04-14  
**Status**: Phase 3 — Content Collection complete (LinkedIn + YouTube + Blog all done)

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

- **Status**: Complete — all platforms collected
- **Completed**: LinkedIn scraping (all 3 passes) — 2026-04-15
- **Completed**: YouTube transcripts (all 16 videos) — 2026-04-15
- **Completed**: Blog scraping (all 53 posts) — 2026-04-15
- **Collection log**:

| Expert | Platform | Items Planned | Items Collected | Status |
|--------|----------|--------------|----------------|--------|
| Russell Brunson | Blog (clickfunnels.com) | 8 | 8 | Complete |
| Jason Fladlien | YouTube | 9 | 9 | Complete |
| Alex Hormozi | YouTube | 1 | 1 | Complete |
| Mariah Coz | Blog (mariahcoz.com) | 7 | 7 | Complete |
| Melissa Kwan | Blog (ewebinar.com) | 17 | 17 | Complete |
| Pat Flynn | YouTube | 1 | 1 | Complete |
| Dama Jue | Podcast page (heartsoulhustle.com) | 1 | 1 | Complete — written content found, no audio transcription needed |
| Omar Zenhom | Blog (webinarninja.com) | 18 | 18 | Complete |
| Alex Cattoni | YouTube + Blog (copyposse.com) | 3 | 3 | Complete |
| Jon Penberthy | YouTube | 4 | 4 | Complete |

**Totals**: 16 YouTube · 53 blog/podcast posts
**YouTube**: 16/16 complete · **Blog + podcast pages**: 53/53 complete

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

1. **LinkedIn scraping** (complete — 2026-04-15) — 3 passes via Apify; 1,082 posts collected. See "LinkedIn Scraping" section below for full results.
2. **YouTube transcripts** (complete — 2026-04-15) — 16 videos via Supadata API. See "YouTube Transcripts" section below.
3. **Blog scraping** (complete — 2026-04-15) — 53 posts via requests + BS4. See "Blog Scraping" section below.
4. **Podcast pages** — resolved during blog scraping; all 3 flagged pages had sufficient written content. Deepgram not needed.

---

#### LinkedIn Scraping — Complete (2026-04-15)

**Status**: All 3 passes ran and committed. 1,082 posts saved. Awaiting user review.

**Goal**: Collect publicly available LinkedIn posts relevant to webinar funnels. Ran in three passes in strict priority order.

**Results summary:**

| LinkedIn Scraping Pass | Description | Posts Collected | Output Location |
|------------------------|-------------|----------------|-----------------|
| Pass 1 — Expert profiles | Posts directly from each approved expert's LinkedIn profile | 483 | `resources/LinkedIn-posts/[expert-slug]/` |
| Pass 2 — Topic + expert name | Posts mentioning a webinar topic AND an expert's name | 265 | `resources/LinkedIn-posts/search-results/` |
| Pass 3 — Topic keywords only | Broad keyword sweep, no expert name constraint | 334 | `resources/other/linkedin-topic-search/` |
| **Total** | | **1,082** | |

**Pass 1 expert breakdown:**

| Expert | Posts collected | Notes |
|--------|----------------|-------|
| Russell Brunson | 100 | Many posts via ClickFunnels company page |
| Alex Cattoni | 100 | |
| Melissa Kwan | 97 | |
| Omar Zenhom | 98 | |
| Alex Hormozi | 82 | |
| Pat Flynn | 6 | Low activity on LinkedIn |
| Jason Fladlien | 0 | Profile not found / private |
| Mariah Coz | 0 | Profile not found / private |
| Dama Jue | 0 | Profile not found / private |
| Jon Penberthy | 0 | Profile not found / private |

**Known issue**: `published_date` is set to `"unknown"` on all LinkedIn files. The Apify actor returns `postedAt` as a nested dict — the parser was fixed after the run; a re-run would recover real dates but would cost ~$2 of the remaining ~$2.70 free tier credit. Decision: leave as `"unknown"` for this research pass.

**Apify credit usage** (FREE plan, $5/month):
- Spent: ~$2.30 (all of today's LinkedIn runs)
- Remaining: ~$2.70
- Cycle ends: 2026-05-13

---

**Pass 1 — Expert profiles (highest priority)**

Scrape posts directly from each approved expert's LinkedIn profile.

Tool: **Apify — LinkedIn Profile Scraper**

| Expert | LinkedIn URL |
|--------|-------------|
| Russell Brunson | `https://www.linkedin.com/in/russellbrunson/` |
| Jason Fladlien | `https://www.linkedin.com/in/jasonfladlien/` |
| Alex Hormozi | `https://www.linkedin.com/in/alexhormozi/` |
| Mariah Coz | `https://www.linkedin.com/in/mariahcoz/` |
| Melissa Kwan | `https://www.linkedin.com/in/melissakwan/` |
| Pat Flynn | `https://www.linkedin.com/in/patflynn/` |
| Dama Jue | `https://www.linkedin.com/in/damajue/` |
| Omar Zenhom | `https://www.linkedin.com/in/omarzenhom/` |
| Alex Cattoni | `https://www.linkedin.com/in/alexcattoni/` |
| Jon Penberthy | `https://www.linkedin.com/in/jonpenberthy/` |

Output location: `resources/LinkedIn-posts/[expert-slug]/[YYYY-MM-DD]-[post-slug].md`

---

**Pass 2 — Topic + expert name (second priority)**

Search LinkedIn posts that mention a webinar topic AND at least one approved expert's name. This catches expert mentions, reposts, and commentary from others.

Tool: **Apify — LinkedIn Posts Search Scraper**

Queries (each expert name paired with core topics):
1. `"Russell Brunson" webinar funnel`
2. `"Jason Fladlien" webinar`
3. `"Alex Hormozi" webinar`
4. `"Mariah Coz" webinar`
5. `"Melissa Kwan" webinar`
6. `"Pat Flynn" webinar`
7. `"Dama Jue" webinar`
8. `"Omar Zenhom" webinar`
9. `"Alex Cattoni" webinar`
10. `"Jon Penberthy" webinar`

Output location: `resources/LinkedIn-posts/search-results/[YYYY-MM-DD]-[query-slug].md`

---

**Pass 3 — Webinar topic keywords only (third priority)**

Broad keyword sweep with no expert name constraint. Surfaces practitioners outside the approved list.

Tool: **Apify — LinkedIn Posts Search Scraper**

Queries (in priority order):
1. `"webinar funnel"`
2. `"webinar funnel from zero"`
3. `"webinar registration page"`
4. `"webinar show up rate"`
5. `"webinar email sequence"`
6. `"automated webinar funnel"`
7. `"evergreen webinar"`
8. `"webinar conversion rate"`

Output location: `resources/other/linkedin-topic-search/[YYYY-MM-DD]-[query-slug].md`

---

**Actors used:**

| Actor | Apify ID | Used for | Notes |
|-------|----------|----------|-------|
| LinkedIn Profile Posts Scraper | `harvestapi/linkedin-profile-posts` | Pass 1 | No cookies required |
| LinkedIn Post Search Scraper | `harvestapi/linkedin-post-search` | Pass 2 & 3 | No cookies required |

**Script**: `scripts/linkedin_scrape.py` — run with `--pass 1`, `--pass 2`, `--pass 3`, or `--pass all`

---

#### Blog Scraping — Complete (2026-04-15)

**Status**: All 53 posts scraped and saved. No Deepgram transcription needed — all flagged podcast pages had written content.

**Tool**: `requests` + `BeautifulSoup4` — domain-specific CSS selectors tuned per site.

**Script**: `scripts/blog_scraper.py`

| Expert | Posts | Domain | Content selector used |
|--------|-------|--------|----------------------|
| Russell Brunson | 8 | clickfunnels.com | `.entry-content` |
| Mariah Coz | 7 | mariahcoz.com | `div.route` |
| Melissa Kwan | 17 | ewebinar.com | `.blog_post_body` |
| Omar Zenhom | 18 | webinarninja.com | `article` |
| Alex Cattoni | 2 | copyposse.com | `.single-post` |
| Dama Jue | 1 | heartsoulhustle.com | `article` |
| **Total** | **53** | | |

**Output**: `resources/other/blog-posts/[expert-slug]/[url-slug].md`

**Flagged podcast pages — resolved**:
- `clickfunnels.com/blog/podcast-696-peter-pru` → 1,010 words of show notes — scraped as blog post
- `clickfunnels.com/blog/podcast-670-tim-shields` → 918 words of show notes — scraped as blog post
- `heartsoulhustle.com/blogs/episode-077` → 10,655 words (full written transcript) — scraped as blog post
- **Deepgram not used** — all three pages had adequate written content

---

#### YouTube Transcripts — Complete (2026-04-15)

**Status**: All 16 videos fetched and committed. Awaiting user review (confirmed OK).

**Tool**: Supadata API (`https://api.supadata.ai/v1/youtube/transcript`) — `text: true` returns plain text transcript. Video titles fetched separately via `/metadata` endpoint.

**Script**: `scripts/youtube_transcripts.py`

| Expert | Videos | Output location |
|--------|--------|-----------------|
| Jason Fladlien | 9 | `resources/youtube-transcripts/jason-fladlien/` |
| Jon Penberthy | 4 | `resources/youtube-transcripts/jon-penberthy/` |
| Alex Hormozi | 1 | `resources/youtube-transcripts/alex-hormozi/` |
| Pat Flynn | 1 | `resources/youtube-transcripts/pat-flynn/` |
| Alex Cattoni | 1 | `resources/youtube-transcripts/alex-cattoni/` |
| **Total** | **16** | |

**Note**: `published_date: "unknown"` on all files — Supadata transcript endpoint does not return publish date. Not re-fetched to avoid extra API cost.

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
| Apify `harvestapi/linkedin-profile-posts` | Scrape posts from expert LinkedIn profiles (LinkedIn Pass 1); key in `.env` |
| Apify `harvestapi/linkedin-post-search` | Keyword + name search across LinkedIn posts (LinkedIn Pass 2 & 3); same key |
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
pip install requests beautifulsoup4 python-dotenv apify-client
# Copy .env.example to .env and fill in SUPADATA_API_KEY, APIFY_API_KEY, DEEPGRAM_API_KEY
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

