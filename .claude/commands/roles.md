# /roles - Human-readable view of all tracked roles

Render every role Claude has tracked (applied, not-applying, rejected, planned, seen, and
freshly scraped) from `job_scraper/seen_jobs.json` into a readable Markdown file grouped by
status. The JSON stays as Claude's dedup memory; this gives David a browsable list.

`$ARGUMENTS` may optionally name a status to focus on: `applied`, `not-applying`, `pending`,
`rejected`, `interview`, `assessment`, `seen`, `new` (or empty for everything).

## Steps

1. Regenerate the view:
   ```bash
   python3 tools/jobs.py render
   ```
   This writes `job_scraper/roles.md` and prints a one-line summary of counts per status.
2. Tell David the file path (`job_scraper/roles.md`) so he can open it, and paste the
   **summary counts line** into the chat.
3. If `$ARGUMENTS` named a status, also show that section inline:
   - Applied → the "✅ Applied" section
   - not-applying → the "🚫 Not applying (skipped)" section
   - etc.
   Read the relevant section from `job_scraper/roles.md` (or grep the JSON) and present it
   as a compact table (Title · Company · Location · link · reason). Keep it short; if the
   section is long (>30 rows) summarize and point to the file.
4. If David asks to change a status, use the tool:
   - `python3 tools/jobs.py applied "<ref>"` — mark applied
   - `python3 tools/jobs.py not-apply "<ref>" --reason "..."` — mark not-applying (or use `/not-apply`)
   - `python3 tools/jobs.py set-status "<ref>" <status>` — any other status
   Then re-run `render`.

Status vocabulary: `applied`, `interview`, `assessment`, `pending`, `not_applying`,
`rejected`, `seen`, `new`.
