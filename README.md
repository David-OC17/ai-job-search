<p align="center">
  <img src="claude_animation.gif" alt="Claude Job Search Assistant" width="200">
</p>

# AI Job Search

An AI-powered job application framework built on [Claude Code](https://claude.com/claude-code). Fork it, fill in your profile, and let Claude evaluate job postings, tailor your CV, write cover letters, and prepare you for interviews.

## What this is

A structured workflow that turns Claude Code into a full-stack job application assistant. The core workflow (self-profiling, fit evaluation, and the drafter-reviewer application pipeline) is **language- and country-agnostic**. This fork is adapted for the **US, Mexico, and international** job markets: it searches via the country-agnostic LinkedIn CLI plus WebSearch across Indeed, OCC, Computrabajo, Glassdoor, and company ATS boards, and gates results with a country/visa policy (`target-countries.md`).

```
/setup          /scrape              /apply <url>          /roles · /not-apply
  |                |                     |                        |
  v                v                     v                        v
Fill in        Search job           Evaluate fit             Track your
your profile   portals              Score & recommend        pipeline
  |                |                     |                    (applied /
  v                v                     v                     not-applying /
Profile        Present matches      Tailor 1-page resume      seen ...)
files ready    + shortlist file    (comment-toggle; cover
                   |                 letter on demand)
                   v                     |
               Pick a match             v
               -> /apply            Reviewer agent -> Revise -> Compile -> Final
```

The framework encodes career guidance best practices, including structured evaluation criteria, forward-looking cover letter framing, and optional salary benchmarking.

## Prerequisites

- [Claude Code](https://claude.com/claude-code) (CLI)
- Python 3.11 (only for the optional salary tool) — a `mamba`/`conda` env is recommended
- [Bun](https://bun.sh) (for the LinkedIn job-search CLI)
- LaTeX distribution with `pdflatex` and `xelatex`: [TeX Live](https://tug.org/texlive/) or [MiKTeX](https://miktex.org/). The resume (`cv/resume.cls`) compiles with `pdflatex`; the optional cover letter compiles with `xelatex` because `cover.cls` requires `fontspec`.

## Quick start

### 1. Fork and clone

```bash
gh repo fork MadsLorentzen/ai-job-search --clone
cd ai-job-search
```

### 2. Install the job search tool

```bash
cd .agents/skills/linkedin-search/cli && bun install && cd ../../../..
```

The install is optional: `linkedin-search` has zero runtime dependencies and runs with plain `bun`; `bun install` only pulls TypeScript dev types.

### 3. Set up your profile

```bash
claude
# Then inside Claude Code:
/setup
```

`/setup` offers three paths: read your `documents/` folder if you have one populated (CV PDF, LinkedIn export, diplomas, reference letters, past applications), import a single CV pasted in chat, or walk through an interview. It auto-detects what you have and asks. Documents-folder mode is idempotent and safe to re-run as you add more material; see `documents/README.md` for the layout.

### 4. Search for jobs

```bash
/scrape
```

This searches multiple job portals for positions matching your profile, deduplicates results, and presents them sorted by fit. Pick a match to run `/apply` on it directly.

### 5. Apply to a job

```bash
/apply https://job-boards.greenhouse.io/company/jobs/1234567
```

If the URL can't be fetched (some job portals block automated access), you can paste the job description directly instead:

```bash
/apply <paste the full job description here>
```

This runs the full workflow: evaluate fit, draft CV + cover letter, review with a second agent, revise, and present the final output.

## Other commands

`/setup`, `/scrape`, and `/apply` form the core workflow. Additional commands extend it once your profile is in place.

**Tracking your pipeline:**

- **`/roles [status]`** renders every tracked role (applied, not-applying, rejected, planned, seen, freshly scraped) from `job_scraper/seen_jobs.json` into a human-readable `job_scraper/roles.md`, grouped by status. Optional filter, e.g. `/roles applied` or `/roles not-applying`. The JSON stays as the deduplication memory; `roles.md` is the browsable view.
- **`/not-apply <url | id | text> [reason]`** registers a job you're *deliberately skipping* — a neutral "read it, passing" marker, not a fit-rejection. It's recorded so `/scrape` never resurfaces it and it shows under "Not applying" in `/roles`.

Both are backed by `tools/jobs.py`, a small CLI that mutates `seen_jobs.json` and renders the Markdown views (also usable directly: `python3 tools/jobs.py render`, `... applied <ref>`, `... set-status <ref> <status>`).

**Profile & analysis:**

- **`/expand`** enriches your profile by scanning public sources you've already linked in it (GitHub repos, portfolio site, Kaggle, Google Scholar) and looking up syllabi for named courses and certifications. Discovered competencies are added to your profile with a source tag. Useful right after `/setup` to surface skills that documents alone don't make explicit.
- **`/upskill`** analyzes the gap between your profile and your tracked job postings (or a single posting via `/upskill <URL>`). Produces a prioritized heatmap of skill gaps and a learning plan with web-searched study resources and time estimates. Useful for career planning between applications.

`/reset` is also available, see [Starting over](#starting-over) below.

## File structure

```
ai-job-search/
├── CLAUDE.md                          # Main candidate profile + workflow rules
├── .claude/
│   ├── commands/
│   │   ├── apply.md                   # /apply workflow (drafter-reviewer)
│   │   ├── setup.md                   # /setup onboarding (documents folder, CV import, or interview)
│   │   ├── expand.md                  # /expand competency enrichment from documents and online presence
│   │   ├── roles.md                   # /roles human-readable view of all tracked roles by status
│   │   ├── not-apply.md               # /not-apply register a job you're deliberately skipping
│   │   └── reset.md                   # /reset wipe profile data or documents folder
│   ├── skills/
│   │   ├── job-application-assistant/  # Core application skill
│   │   │   ├── SKILL.md               # Skill definition
│   │   │   ├── 01-candidate-profile.md # Your education, experience, skills
│   │   │   ├── 02-behavioral-profile.md# PI/DISC/personality assessment
│   │   │   ├── 03-writing-style.md    # Tone, structure, do's and don'ts
│   │   │   ├── 04-job-evaluation.md   # Scoring framework for job fit
│   │   │   ├── 05-cv-templates.md     # resume.cls structure + tailoring rules
│   │   │   ├── 06-cover-letter-templates.md # LaTeX cover letter templates (on demand)
│   │   │   └── 07-interview-prep.md   # STAR examples + interview framework
│   │   ├── job-scraper/               # Job search orchestration
│   │   └── upskill/                   # /upskill skill gap analysis and learning plan
│   └── settings.json                  # Claude Code permissions (shared, scoped)
├── target-countries.md                # Country/visa tier policy gating which openings to pursue
├── .agents/skills/                    # Job portal CLI tools
│   └── linkedin-search/               # LinkedIn public job listings (country-agnostic)
├── cv/
│   ├── resume.cls                     # Custom single-page resume LaTeX class
│   ├── resume.tex                     # Resume master (header + \input sections)
│   └── sections/                      # Resume content (bullet/project variants to select)
├── cover_letters/
│   ├── cover.cls                      # Custom cover letter LaTeX class (used on demand)
│   └── OpenFonts/                     # Lato + Raleway fonts
├── documents/                         # Career source materials for /setup Path A and /expand
│   ├── README.md                      # Folder layout instructions
│   ├── cv/                            # Master CV (PDF or .tex)
│   ├── linkedin/                      # LinkedIn profile export (PDF)
│   ├── diplomas/                      # Degree certificates and transcripts
│   ├── references/                    # Reference letters
│   └── applications/                  # Past application records (<company>_<role>/)
├── salary_lookup.py                   # Salary benchmarking tool (BYO data)
├── tools/
│   ├── jobs.py                        # Job status manager + renderer (/roles, /not-apply)
│   ├── convert_salary_excel.py        # Convert salary Excel to JSON
│   └── README_SALARY_TOOL.md          # Salary tool setup instructions
├── job_scraper/                       # Scraper state (all git-ignored, personal)
│   ├── seen_jobs.json                 # Canonical dedup memory + per-role status
│   ├── roles.md                       # Human-readable roles view (generated by /roles)
│   └── matches-YYYY-MM-DD.md          # Per-run shortlist checklists (generated by /scrape)
├── upskill/                           # /upskill report output (markdown reports per run)
├── job_search_tracker.csv             # Application tracking spreadsheet (permanent applied record)
└── SETUP.md                           # Detailed setup guide
```

## How `/apply` works

The `/apply` command runs a **drafter-reviewer workflow** with mandatory PDF compilation:

1. **Parse** the job posting (URL or text) and screen the location against `target-countries.md`
2. **Evaluate fit** against your profile (skills, experience, culture, location/visa, career alignment)
3. **Draft** a tailored single-page resume (and a cover letter only if the posting requires one) in LaTeX, in English
4. **Spawn a reviewer agent** that researches the company and critiques the drafts
5. **Revise** based on the reviewer's feedback
6. **Compile and inspect** the PDF(s): pdflatex for the resume, xelatex for a cover letter. Claude reads the rendered pages and iterates on the LaTeX until the resume is exactly 1 page with no orphaned entry titles (and any cover letter is exactly 1 page with the signature visible and fonts consistent).
7. **Present** the final output with a verification checklist

All claims in the resume and cover letter are verified against your actual profile. **Tailoring is limited to commenting existing content variants in or out** — the master resume ships alternate and shorter bullet/project variants for this purpose. The system never fabricates skills or experience, and any actual wording change to the resume `.tex` files is proposed to you for approval before it is written.

### What makes this workflow different

- **PDF verification loop.** LaTeX resumes produce "looks fine in the .tex" output that breaks in the PDF: a role title orphans to the next page, a resume spills onto page 2, a cover letter's bullet font silently falls back to the body font. The `/apply` command compiles (`pdflatex` for the resume, `xelatex` for a cover letter) and visually inspects every PDF, iterating until the layout is clean. This runs automatically on every application.
- **Relevance-weighted fitting.** The resume must land on exactly one page. Rather than cutting from the "oldest" section, the workflow scores each candidate line by (a) relevance to the target posting, (b) uniqueness, and (c) whether a cover letter depends on it, then comments out the lowest-total-score variants first. An older-role bullet that hits posting keywords survives ahead of a recent one that does not.
- **Drafter-reviewer separation.** The drafter writes; a second Claude agent, spawned with a fresh context, researches the company and critiques the drafts. The drafter then revises. This catches missed keywords, weak framing, and generic language that a single pass often leaves in.
- **Token-efficient reviewer dispatch.** The reviewer agent receives drafts inline rather than re-reading them, and the verification checklist runs once at the end of the workflow rather than being duplicated by both agents. Note: the new compile-and-inspect step in Step 5 spends some of those savings on PDF rendering and layout iteration — the workflow trades some end-to-end token cost for a real reduction in broken PDFs reaching the user.

## Customization

### Which files to edit manually

If you prefer editing files directly instead of using `/setup`:

| File | What to change |
|------|---------------|
| `CLAUDE.md` | Your full profile (name, education, experience, skills, goals) |
| `01-candidate-profile.md` | Structured version of your CV data |
| `02-behavioral-profile.md` | Your behavioral assessment or self-assessment |
| `04-job-evaluation.md` | Skill match areas, career goals, motivation filters |
| `05-cv-templates.md` | Resume tailoring rules (which section variants to enable per role type) |
| `07-interview-prep.md` | Your STAR examples from actual experience |
| `search-queries.md` | Job search queries for your skills and location |
| `target-countries.md` | Country/visa tiers deciding which openings to pursue or skip |
| `cv/sections/*.tex` | Your actual resume content (add/adjust the commented bullet & project variants) |

### Updating your search queries

As your priorities evolve, you can reconfigure just the job search without re-running the full profile setup:

```
/setup --section search
```

This re-runs the search configuration interview: which roles to target, which skills to search for, which locations, and which portals. It also suggests role types you may not have considered based on your profile.

### LaTeX templates

The resume uses a custom single-page `resume.cls` (article-based, compiled with `pdflatex`). The cover letter uses a custom `cover.cls` with Lato/Raleway fonts (compiled with `xelatex`, generated only when a posting requires one). You can replace these with your own templates; just update the guidance in `05-cv-templates.md` and `06-cover-letter-templates.md`.

### Job search tools

The `linkedin-search` CLI in `.agents/skills/` is a country-agnostic worked example of the job-portal integration pattern. If you want deeper coverage of a specific board (Indeed, OCC, Computrabajo, a company ATS), you can build an equivalent tool for it using the same structure.

For a **country-agnostic** starting point, the repo also includes **`linkedin-search`** — a job-search skill built on LinkedIn's public, unauthenticated `jobs-guest` endpoints. It is field-agnostic, has **zero runtime dependencies** (runs with just `bun`), and takes the search location as an explicit flag, so it works for any market out of the box (`-l "Berlin, Germany"`, `-l "Mumbai, Maharashtra, India"`, `-l "Remote"`, …). It is intended for **personal use only** — automated access is against LinkedIn's Terms of Service, so keep volume low. See `.agents/skills/linkedin-search/SKILL.md`.

### Salary benchmarking

The salary tool works with any salary data you provide (union statistics, Glassdoor exports, personal research, etc.). See `tools/README_SALARY_TOOL.md` for the expected format and setup. If you don't have salary data, the salary step is simply skipped.

### Starting over

To wipe your profile data and start fresh:

```
/reset profile    # clears skill files, preserves framework rules
/reset documents  # deletes files from documents/ folder
/reset all        # both
```

`/reset` shows exactly what will be deleted and requires you to type `RESET` to confirm. Nothing is deleted until you do.

## Tips for better results

### Profile depth matters

The single biggest factor in output quality is how much detail you put into your profile. A thin profile produces generic applications; a detailed one enables genuinely tailored results.

- **Role descriptions:** Don't just list job titles. Describe what you actually did in each position: specific projects, tools used, responsibilities, and measurable achievements. The more material you provide, the more precisely the system can reframe your experience for different roles.
- **Skills in context:** Instead of listing "Python" or "project management," describe how and where you applied them. "Built ML pipelines for customer churn prediction in Python using scikit-learn" gives the system far more to work with than "Python, machine learning."
- **All onboarding paths work:** Whether you point `/setup` at your `documents/` folder, paste a single CV, or walk through the interview, the principle is the same: richer input produces sharper output.

### Career path discovery

The framework supports two distinct modes of job searching:

- **Explicit targeting:** You know which roles or sectors you want. The system helps refine and prioritize based on fit.
- **Latent opportunity discovery:** By analyzing your full history (not just job titles, but the actual work you did), the system can surface career paths you haven't considered. Transferable skills that map to unexpected industries, patterns in what you enjoyed or excelled at, or emerging roles that combine your domain expertise with new technology.

To get the most from this, invest time during `/setup` in describing not just your experience, but what energized you, what drained you, and what you'd want more of. This context directly shapes how the system evaluates fit and which roles it surfaces during `/scrape`.

## Acknowledgements

- [Mikkel Krogholm](https://github.com/mikkelkrogsholm) ([skills repo](https://github.com/mikkelkrogsholm/skills)) for the job search CLI skills
- Built with [Claude Code](https://claude.com/claude-code) by [Anthropic](https://anthropic.com)

## License

MIT
