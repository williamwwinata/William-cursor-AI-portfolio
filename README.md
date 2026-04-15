# William's Cursor AI Portfolio

A portfolio project built as part of the 100hires AI-Native application process. This repository documents my setup, tools, and process of configuring an AI-assisted development environment using Cursor IDE.

---

## Tools Installed

- **[Cursor IDE](https://cursor.com):** AI-native code editor built on VS Code
- **Claude Code** (Cursor Extension): Anthropic's AI coding assistant, which I run via the integrated terminal
- **Codex** (Cursor Extension): OpenAI-powered coding extension with a sidebar interface

---

## Languages and Technologies Used

- **Markdown:** for documentation and README authoring
- **Git / GitHub:** for version control and remote repository management
- **Bash / Terminal:** for running CLI tools within Cursor's integrated terminal

---

## Setup Process

### 1. Installing Cursor IDE

- I visited [cursor.com](https://cursor.com), created an account, and downloaded the desktop application
- I logged in to the Cursor app using my newly created account
- I restarted my PC after installation to ensure a clean environment before proceeding

### 2. Installing Extensions

- I located the Extensions panel via **View > Extensions** in the Cursor menu bar
- I searched for and installed both the **Claude Code** and **Codex** extensions

### 3. Setting Up Claude Code

- I already had Claude Code installed on my machine as a CLI tool via my personal Anthropic subscription
- Claude Code authentication is **local**, meaning credentials are stored on-device in `~/.claude/` after the initial OAuth login
- Because my authentication was already stored locally, I did not need to log in again inside Cursor; I simply opened Cursor's integrated terminal and ran `claude` to start a session immediately

### 4. Setting Up Codex

- The Codex extension did not have an immediately obvious entry point in the UI
- I watched a YouTube tutorial to understand how to launch it
- I used **Ctrl + Shift + P** to open the Command Palette and ran the **Open Codex Sidebar** command
- The extension prompted me to log in, which I completed successfully

### 5. Creating the GitHub Repository and Cloning Locally

- I created a new public repository on GitHub using my existing GitHub account
- I cloned the repository to my local machine to start working with it inside Cursor
- I set up the Cursor and GitHub connection so that all Git operations such as commits and pushes could be run directly from within the editor

### 6. Writing the README and Pushing to GitHub

- With Claude Code running in my Cursor terminal, I used it to write this README documenting my full setup process. I specifically told Claude to write it in first person so it accurately reflects my own experience
- I had Claude Code handle the `git commit` and `git push` to upload the changes to my GitHub repository

---

## Issues Encountered and How They Were Resolved

- **Did not know where to find the Extensions panel in Cursor:** I explored the menu bar and found it under **View > Extensions**
- **Unsure how to launch the Codex extension after installing it:** I searched YouTube for a tutorial and learned to use **Ctrl + Shift + P** then **Open Codex Sidebar**
- **Needed to verify whether Claude Code required re-authentication inside Cursor:** I confirmed that Claude Code stores auth locally on the device, so no additional login was needed

---

## Key Takeaways

- Cursor's interface felt familiar since I have used VS Code before, which made the learning curve much easier
- Claude Code's local authentication model means it works seamlessly across any terminal on the same machine without repeated logins
- When documentation or UI discoverability is lacking, a targeted YouTube search is a fast and effective way to get unblocked
- Restarting my PC after installations was a simple but effective step to avoid potential environment issues
- AI tools like Claude Code can handle not just coding tasks but also documentation and Git operations, which streamlines the entire development workflow

---

## Personal Note

This entire project was built using Claude Code inside Cursor. To me, this task is ultimately about demonstrating problem-solving ability and clarity of thinking. My view is that as long as a person has a clear understanding of the problem and the steps needed to address it, AI becomes a powerful multiplier that accelerates the workflow without replacing the judgment behind it. That is exactly why I chose to leverage Claude Code here: so I could stay focused on the what and the why, while letting AI handle the execution. This approach is also backed by a level of technical literacy that I believe is one of the most essential skills an individual can have in this era.

---

## Research: Webinar Funnel from Zero

This section documents the ongoing research phase of the project, a structured content collection effort exploring how top practitioners think about, teach, and execute webinar funnels. The goal is to gather primary-source material from recognized experts across LinkedIn, YouTube, and their own blog platforms, so that patterns, frameworks, and actionable strategies can be synthesized from real practitioner knowledge rather than generic advice.

---

## What Was Collected


| Platform                       | Method                         | Volume          |
| ------------------------------ | ------------------------------ | --------------- |
| LinkedIn (profile posts)       | Apify LinkedIn Profile Scraper | 483 posts       |
| LinkedIn (topic + name search) | Apify LinkedIn Posts Search    | 265 posts       |
| LinkedIn (broad keyword sweep) | Apify LinkedIn Posts Search    | 334 posts       |
| YouTube transcripts            | Supadata API                   | 16 transcripts  |
| Blog articles                  | requests + BeautifulSoup4      | 53 articles     |
| **Total**                      |                                | **1,151 items** |


All files follow a consistent YAML frontmatter format (author, platform, source URL, collection method, tags) to make filtering and synthesis straightforward in the next phase.

---

## Research Process

### Expert Selection

Claude generated an initial candidate list of 17 practitioners, each scored against a set of quality gates: documented track record with actual webinar results, consistency of public output, and coverage of a distinct angle (funnel structure, copywriting, automation, paid traffic, evergreen systems, etc.).

I reviewed the list myself, removed 7 candidates, and independently added 2 that were not in the original draft. The final 10 were approved by me before any collection began.

### Collection Phases

Collection ran in three sequential phases: LinkedIn, YouTube, then blog scraping. After each phase completed, I reviewed the output before giving the go-ahead for the next. Nothing proceeded without that checkpoint.

### My Role Throughout

Every meaningful decision in this project was mine:

- I defined the research objective and what sufficient coverage meant
- I curated the expert list, not just approving suggestions but independently adding names
- I wrote every "Why this expert was chosen" field from scratch, without being prompted
- I cross-checked my own written rationale against the actual collected resources and identified where my reasoning didn't hold up
- I directed all corrections when the collected content and the stated rationale were misaligned

AI handled the execution: building the scripts, running the scrapers, fetching transcripts, and formatting files. I handled the judgment: who to include, what to collect, and the overall research direction.

---

## Repository Structure

```
William-cursor-AI-portfolio/
├── README.md
├── plan.md                              (full research log with phase decisions and trade-offs)
├── .gitignore
├── scripts/
│   ├── linkedin_scrape.py               (LinkedIn 3-pass scraper via Apify)
│   ├── youtube_transcripts.py           (YouTube transcript fetcher via Supadata API)
│   └── blog_scraper.py                  (Blog scraper via requests + BeautifulSoup4)
└── resources/
    ├── sources.md                       (expert registry with quality gate scores)
    ├── LinkedIn-posts/
    │   ├── [expert-slug]/               (Pass 1: posts directly from expert profiles)
    │   └── search-results/              (Pass 2: topic + expert name search results)
    ├── youtube-transcripts/
    │   └── [expert-slug]/
    └── other/
        ├── blog-posts/
        │   └── [expert-slug]/
        └── linkedin-topic-search/       (Pass 3: broad keyword sweep, no expert name constraint)
```

---

## How to Reproduce

```bash
git clone <repo-url>
cd William-cursor-AI-portfolio
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install requests beautifulsoup4 python-dotenv apify-client
```

Copy `.env.example` to `.env` and fill in your API keys:

```
SUPADATA_API_KEY=your_key_here
APIFY_API_KEY=your_key_here
```

Then run each script in order:


| Script                   | Purpose                                        | Command                                        |
| ------------------------ | ---------------------------------------------- | ---------------------------------------------- |
| `linkedin_scrape.py`     | LinkedIn 3-pass scraper (Apify)                | `python scripts/linkedin_scrape.py --pass all` |
| `youtube_transcripts.py` | YouTube transcript fetcher (Supadata)          | `python scripts/youtube_transcripts.py`        |
| `blog_scraper.py`        | Blog and podcast page scraper (requests + BS4) | `python scripts/blog_scraper.py`               |


Full technical notes, known limitations, and cost breakdowns are documented in `plan.md`.

---

## Experts Covered

The following 10 experts were selected as the primary sources for this research. Each has demonstrated consistent, high-quality output on webinar strategy, funnel design, or online course sales, either through their own products, platforms, or published content. Content was collected across LinkedIn posts, YouTube transcripts, and blog articles where available.

---

1. **Russell Brunson**
  - **Expert bio/description:** Russell Brunson is the co-founder of ClickFunnels and one of the most recognized figures in the online sales funnel space. He popularized the concept of the "perfect webinar" script, a structured presentation framework designed to sell high-ticket offers. His books (*DotCom Secrets*, *Expert Secrets*, and *Traffic Secrets*) have sold millions of copies and are widely cited as foundational resources in digital marketing. Brunson built ClickFunnels into a $1B+ software company largely through webinar-based marketing.
  - **What was collected:** LinkedIn (profile posts): 100 posts | LinkedIn (topic + name search): 44 posts | Blog (clickfunnels.com): 8 articles
  - **Why this expert was chosen:** His "Perfect Webinar" script is one of the most widely used webinar framework out there (as expected from the co-founder of ClickFunnels). It made sense to include him in this list since it gave me a proven structural baseline to build the playbook around, rather than starting from scratch. His platform also provides lots of materials, both basics and advanced, to be included in the playbook later.

---

1. **Jason Fladlien**
  - **Expert bio/description:** Jason Fladlien is widely regarded as one of the highest-converting webinar presenters in the world, credited with generating over $250 million in webinar sales. He is the co-founder of Rapid Crush and the author of *One to Many*, a book dedicated entirely to webinar selling strategy. Fladlien's methods focus heavily on objection handling, offer structuring, and psychological sequencing within a live presentation. His work is frequently cited by other experts on this list as a primary influence.
  - **What was collected:** LinkedIn (topic + name search): 50 posts | YouTube transcripts: 9 videos
  - **Why this expert was chosen:** His track record of $250M+ in webinar sales made him impossible to ignore. I included him specifically because some of his content goes deep on objection handling and closing.

---

1. **Alex Hormozi**
  - **Expert bio/description:** Alex Hormozi is the founder of Acquisition.com and the author of *$100M Offers* and *$100M Leads*, two of the most widely read books in modern business growth. He built and sold multiple companies across gym, software, and education verticals before transitioning to investing and content creation. Hormozi's approach to offers, pricing psychology, and value stacking has directly influenced how practitioners frame webinar pitches and closing sequences. His content is known for its density and directness.
  - **What was collected:** LinkedIn (profile posts): 82 posts | LinkedIn (topic + name search): 50 posts | YouTube transcripts: 1 video
  - **Why this expert was chosen:** Because it's Alex Hormozi. All jokes aside, the resource we collected from him is a live session, advising on webinar and event conversion, breaking down the difference between declarative and procedural content, why you should sell at the point of greatest deprivation and not greatest value, and why speed of commitment will always outsell a big outcome that's far away. These mind frameworks might help on building a reliable webinar funnel.

---

1. **Mariah Coz**
  - **Expert bio/description:** Mariah Coz is an online course strategist who specializes in live and evergreen webinar funnels for course creators. She founded Femtrepreneur and later Mariah Coz LLC, where she teaches creators how to build scalable, automated sales systems around digital products. Her content is particularly focused on the mindset and mechanics of converting a live webinar into a repeatable evergreen funnel. She has run and documented numerous high-revenue course launches built around the webinar model.
  - **What was collected:** LinkedIn (topic + name search): 3 posts | Blog (mariahcoz.com): 7 articles
  - **Why this expert was chosen:** She's one of the few experts who documents the full journey from a one-time live webinar to a repeatable system. That scalability angle was important to include with hopes that it can create a funnel that can run consistently.

---

1. **Melissa Kwan**
  - **Expert bio/description:** Melissa Kwan is the co-founder and CEO of eWebinar, an automated webinar platform built specifically for repeatable, scalable webinar delivery. She brings a product and operations perspective to webinar strategy; her content covers registration flow, attendee experience, engagement mechanics, and platform selection at a granular level. Having built a SaaS company around the problem of webinar automation, her insights are grounded in real product data and customer behavior. She is a recognized voice in the automated and asynchronous webinar space.
  - **What was collected:** LinkedIn (profile posts): 97 posts | LinkedIn (topic + name search): 15 posts | Blog (ewebinar.com): 17 articles
  - **Why this expert was chosen:** I chose her because she covers the operational and technical side of webinar delivery that most content creators skip, which is exactly what an internal team needs to set things up properly.

---

1. **Pat Flynn**
  - **Expert bio/description:** Pat Flynn is the founder of Smart Passive Income and one of the earliest and most trusted voices in the online business and passive income space. He has built multiple businesses, courses, and communities through transparent, audience-first content, and has documented the role of webinars extensively in his own launches. Flynn is known for combining practical execution with honest performance reporting, making his content useful for both strategy and benchmarking. His audience spans both beginners and experienced online entrepreneurs.
  - **What was collected:** LinkedIn (profile posts): 6 posts | LinkedIn (topic + name search): 43 posts | YouTube transcripts: 1 video
  - **Why this expert was chosen:** He's one of the experts who openly walks through the behind the scenes of his own most profitable webinar, including real engagement and list-growth data from his own runs. I included him for that data and for his "trust-first" take on live webinars.

---

1. **Dama Jue**
  - **Expert bio/description:** Dama Jue is a launch strategist and copywriter who focuses on helping online course creators and coaches design high-converting launch sequences, with webinars as a central component. She is the founder of Heart Soul Hustle and has coached hundreds of creators through live and automated webinar launches. Her perspective integrates copywriting, emotional storytelling, and audience psychology into webinar strategy. She is known for an unconventional, values-driven approach to marketing that prioritizes alignment over volume.
  - **What was collected:** Blog/podcast page (heartsoulhustle.com): 1 article
  - **Why this expert was chosen:** She takes a deliberately unconventional approach to webinar-based selling: short formats (13–20 minutes), low-ticket multi-offer model, no big production launch required. I included her because her model proves that a webinar doesn't have to be a two-hour event to move product, which felt like an important perspective to have alongside the heavier, launch-focused frameworks from the other experts in this list.

---

1. **Omar Zenhom**
  - **Expert bio/description:** Omar Zenhom is the co-founder of WebinarNinja, a webinar hosting platform, and the host of *The $100 MBA Show*, one of the top-ranked business podcasts on iTunes. He brings both a practitioner and platform-builder perspective to webinar strategy; his content covers the full funnel from audience targeting to post-webinar follow-up sequences. Zenhom's blog is one of the most comprehensive freely available resources on webinar mechanics, covering topics from branding and etiquette to automated funnels and content repurposing. His work is data-informed and operationally detailed.
  - **What was collected:** LinkedIn (profile posts): 98 posts | LinkedIn (topic + name search): 7 posts | Blog (webinarninja.com): 18 articles
  - **Why this expert was chosen:** As a webinar platform founder, he's seen what works and what doesn't across a large volume of webinars. His blog was one of the most detailed free resources I found, covering everything from registration flow to post-webinar follow-up.

---

1. **Alex Cattoni**
  - **Expert bio/description:** Alex Cattoni is a copywriter, brand strategist, and founder of the Copy Posse, a global community for ethical copywriters. She is known for her frameworks around conversion copy, particularly for webinar landing pages, email sequences, and sales presentations. Cattoni's background in agency copywriting gives her a technical precision that complements the more funnel-strategy-oriented experts in this list. Her YouTube channel and blog regularly cover how copywriting directly impacts webinar registration rates and close rates.
  - **What was collected:** LinkedIn (profile posts): 100 posts | LinkedIn (topic + name search): 39 posts | YouTube transcripts: 1 video | Blog (copyposse.com): 2 articles
  - **Why this expert was chosen:** Somewhat similar with Dama Jue. She's heavily focused on the copy component of the webinar funnel. She's one of the strongest copywriting-focused voice in this selection, and I felt the playbook might need that.

---

1. **Jon Penberthy**
  - **Expert bio/description:** Jon Penberthy is a digital marketer and webinar strategist who has built multiple seven-figure businesses using webinar funnels as the primary sales mechanism. He is the creator of AdClients and is recognized for his systematic approach to webinar traffic, conversion, and scaling, particularly through paid advertising. Penberthy's content focuses on the intersection of ad strategy and webinar funnel design, a perspective not covered by most other experts in this list. He has trained thousands of agency owners and consultants on building client-acquisition systems anchored around webinars.
    - **What was collected:** LinkedIn (topic + name search): 14 posts | YouTube transcripts: 4 videos
    - **Why this expert was chosen:** I chose Jon Penberthy because his content covers the full webinar funnel, from traffic acquisition to conversion: the presentation, the confirmation page, "indoctrination" sequence, and how to move registrants into attendees into buyers. His business is built almost entirely on driving traffic into a webinar funnel, and the mechanics he breaks down are some of the most detailed in what we collected.

---

