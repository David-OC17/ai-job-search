# Search Queries for Job Scraper

Tailored to David Ortiz Cota: **new-grad / early-career** software & robotics engineer
(grad Jun 2026). Core directions: systems/compilers SWE, robotics & perception, embedded/
firmware, ML systems. Markets: **US (priority, all locations), Mexico (Guadalajara / CDMX /
Monterrey / remote), and international** — see `target-countries.md` for the tier policy that
decides which results to keep.

## Two search paths

1. **LinkedIn CLI (structured, preferred for volume)** — the country-agnostic Bun tool.
   Runs directly, returns clean JSON with job IDs you can pass to `detail`:
   ```bash
   bun run .agents/skills/linkedin-search/cli/src/cli.ts search -q "<query>" -l "<location>" --jobage 14 --format json
   ```
   Locations to sweep: `"Guadalajara, Jalisco, Mexico"`, `"Mexico City, Mexico"`,
   `"United States"`, `"San Francisco Bay Area"`, `"London, United Kingdom"`, `"Remote"`.

2. **WebSearch + WebFetch (broad, board-agnostic)** — use `site:` filters against the
   boards below for postings the LinkedIn endpoint misses (esp. company ATS pages).

## Search boards (WebSearch `site:` targets)

Mexico:
- **mx.indeed.com** — largest general board in MX
- **occ.com.mx** — OCC Mundial, major MX board
- **mx.computrabajo.com** — Computrabajo MX
- **linkedin.com/jobs** — filter to Mexico / Guadalajara / CDMX

US & international:
- **indeed.com** (and country Indeed domains: uk.indeed.com, ca.indeed.com, de.indeed.com)
- **linkedin.com/jobs**
- **glassdoor.com**
- **wellfound.com** (startups) and **levels.fyi/jobs**
- **Company ATS via Google:** `site:boards.greenhouse.io`, `site:jobs.lever.co`,
  `site:jobs.ashbyhq.com`, `site:*.myworkdayjobs.com`, `site:job-boards.greenhouse.io`
  (many roles David tracked came from Ashby/Lever/Greenhouse)
- **New-grad aggregators:** GitHub new-grad lists, e.g.
  `site:github.com "New Grad" software engineer 2026 jobs`

## Query Categories

Combine each query with a location term where the board supports it. Default window: last 14 days.

### Priority 1: Systems / Software Engineer (new grad)

```
site:linkedin.com/jobs "software engineer" ("new grad" OR "early career" OR "university grad") 2026
site:boards.greenhouse.io software engineer new grad compilers OR runtime OR toolchain
site:jobs.ashbyhq.com software engineer "new grad" OR "early career"
"software engineer" (compilers OR runtimes OR toolchains OR "systems") new grad site:linkedin.com/jobs
```

### Priority 2: Robotics / Perception / SLAM

```
site:linkedin.com/jobs "robotics software engineer" OR "perception engineer" new grad
robotics engineer (SLAM OR perception OR "sensor fusion" OR localization) site:jobs.lever.co
"robotics software engineer" (C++ OR ROS2) site:linkedin.com/jobs
perception OR autonomy engineer new grad site:boards.greenhouse.io
```

### Priority 3: Embedded / Firmware

```
site:linkedin.com/jobs "embedded" OR "firmware" engineer new grad C OR C++
firmware engineer (STM32 OR RTOS OR "low power" OR microcontroller) site:jobs.lever.co
embedded software engineer new grad site:boards.greenhouse.io
```

### Priority 4: ML systems / GPU / AI infra

```
site:linkedin.com/jobs "machine learning" OR "ML systems" engineer new grad (CUDA OR inference OR TensorRT)
"ML infrastructure" OR "inference" OR "model optimization" engineer new grad site:jobs.ashbyhq.com
```

### Mexico-specific sweep

```
site:mx.indeed.com software engineer Guadalajara OR CDMX
site:occ.com.mx "software engineer" OR "ingeniero de software" Guadalajara
site:mx.computrabajo.com software engineer OR robotics Guadalajara OR "ciudad de mexico"
site:linkedin.com/jobs software engineer (Guadalajara OR "Mexico City" OR remote) Mexico
```

## Location & country filter

Apply `target-countries.md`:
- **Tier 1–2** (US, MX, CA, UK, DE, NL, CH, IE, AU): keep, present first.
- **Tier 3** (rest of EU, NZ, SG, UAE, JP): keep but flag "visa-dependent."
- **Tier 4** / hard requirements (US-citizen/clearance/ITAR, on-site in a no-visa country):
  drop, note why in the run summary.
- **Remote worldwide / Americas-timezone**: always keep.

## Date filter

Only include jobs posted within the last 14 days, or with an application deadline not yet
passed. If the posting date can't be determined, include it but flag "date unknown."

## Adapting queries

If the user runs `/scrape <focus>` (e.g. `/scrape robotics`, `/scrape compilers`,
`/scrape mexico`), prioritize the matching category and generate 2–3 custom queries for it.
`/scrape broad` runs every category above.
