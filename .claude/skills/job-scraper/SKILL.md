---
name: job-scraper
description: >
  Scrapes job sites (Mexico, US, and international) for new positions matching your profile. Deduplicates across runs.
  Triggers on: job scrape, find jobs, search jobs, new jobs, job search, scrape jobs, /scrape
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(bun run:*), WebFetch, WebSearch, Agent, AskUserQuestion
---

# Job Scraper

---

## How It Works

This skill searches multiple job boards (Mexican, US, and international) using targeted queries based on your profile, deduplicates against previously seen jobs and the application tracker, and presents new matches with a quick fit assessment. It uses two paths: the country-agnostic **LinkedIn CLI** (`bun run .agents/skills/linkedin-search/cli/src/cli.ts ...`) for structured results, and **WebSearch/WebFetch** for board-agnostic coverage (Indeed, OCC, Computrabajo, Glassdoor, and company ATS pages on Greenhouse/Lever/Ashby).

## Invocation

The user triggers this skill by saying things like:
- "Find new jobs"
- "Scrape for jobs"
- "Any new positions?"
- "/scrape"

Optional arguments:
- A focus area, e.g. "/scrape data science" or "/scrape geophysics"
- "broad" to run all search categories, e.g. "/scrape broad"

---

## Execution Steps

### Step 0: Load State

1. Read `job_scraper/seen_jobs.json` (create if missing - start with `{"seen": {}}`)
2. Read `job_search_tracker.csv` to extract already-applied companies+roles
3. Read `search-queries.md` (this directory) for the search strategy
4. Read `target-countries.md` (repo root) for the location/visa tier policy

### Step 1: Search

Run the queries from `search-queries.md`. By default, run the top 3 priority categories. If the user said "broad", run all categories.

If the user specified a focus area (e.g. "robotics", "compilers", "mexico"), prioritize queries from that category.

For each search, use both paths from `search-queries.md`:
- **LinkedIn CLI** for structured, deduplicable results:
  `bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "<query>" -l "<location>" --jobage 14 --format json`
- **WebSearch** with site-specific queries (linkedin.com/jobs, mx.indeed.com, occ.com.mx, mx.computrabajo.com, glassdoor.com, boards.greenhouse.io, jobs.lever.co, jobs.ashbyhq.com)
- Sweep the configured markets (US, Mexico — Guadalajara/CDMX/Monterrey/remote — and international per `target-countries.md`)
- Look for postings from the last 14 days

### Step 2: Fetch & Parse

For each promising result from Step 1:
- Use `WebFetch` to retrieve the job posting page
- Extract: **job title**, **company**, **location**, **posting date** (or "recent"), **URL**, **key requirements** (brief), **application deadline** (if listed)
- Skip if the URL or company+title combo already exists in `seen_jobs.json`
- Skip if the company+role already appears in `job_search_tracker.csv`

### Step 3: Quick Fit Assessment

For each new job, do a rapid fit check (NOT the full evaluation from `04-job-evaluation.md` - just a quick signal):

- **High match**: Role directly involves your core skills
- **Medium match**: Role is adjacent to your experience
- **Low match**: Role requires significant skills you lack

### Step 4: Deduplicate & Store

1. Add ALL fetched jobs (new and skipped) to `seen_jobs.json` with structure:
```json
{
  "seen": {
    "<url_or_company_title_key>": {
      "title": "...",
      "company": "...",
      "url": "...",
      "first_seen": "YYYY-MM-DD",
      "fit": "high/medium/low",
      "status": "new/skipped/evaluated"
    }
  }
}
```
2. Only present jobs NOT already in the seen list or tracker.

### Step 5: Present Results

**Always write a persistent, human-readable shortlist file** so David can browse and action matches after the run, not just in chat. Write `job_scraper/matches-YYYY-MM-DD.md` (git-ignored) as a checklist:
- One `- [ ] <emoji> **Title** — Company · Location · Date · [link](url) · \`/apply <url>\`` line per new high/medium match (and a separate section for any visa/ITAR-flagged ones)
- Grouped by fit (🟢 high, 🟡 medium, ⚠️ flagged); low-fit roles stay only in `seen_jobs.json`
- If a file for today already exists, append/merge rather than clobbering earlier ticks

Tell David the file path so he can open it. Then also present new jobs in chat as a table sorted by fit (high first):

```
## New Job Matches - YYYY-MM-DD

Found X new positions (Y high, Z medium, W low match).

| # | Fit | Title | Company | Location | Deadline | URL |
|---|-----|-------|---------|----------|----------|-----|
| 1 | High | ... | ... | ... | ... | [Link](...) |

### High-Match Highlights
For each high-match job, add 2-3 bullet points:
- Why it matches your profile
- Key requirements to check
- Any red flags
```

After presenting, ask:
> "Want me to evaluate any of these in detail? Just give me the number(s)."

If the user picks a number, invoke the **job-application-assistant** skill workflow (fit evaluation first, then CV + cover letter if approved).

### Step 6: Update Tracker (Optional)

If the user decides to apply to any job, add a row to `job_search_tracker.csv`.

---

## Important Rules

1. **Never fabricate job postings.** Only present jobs found via actual WebSearch/WebFetch results.
2. **Respect deduplication.** Always check seen_jobs.json AND job_search_tracker.csv before presenting.
3. **Apply the country/visa policy.** Use `target-countries.md`: present Tier 1–2 first, include Tier 3 with a "visa-dependent" flag, and drop Tier 4 (and hard requirements like US-citizen/clearance/ITAR). Remote-worldwide/Americas-timezone always passes.
4. **Only open positions.** Skip postings with expired deadlines or those marked as closed.
5. **Be efficient with WebFetch.** Don't fetch every search result - use titles and snippets to pre-filter before fetching.
6. **Parallel searches.** Use the Agent tool or parallel WebSearch calls to speed up the search phase.
