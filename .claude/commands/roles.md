# /roles - Human-readable view of all tracked roles

Render every role Claude has tracked (applied, not-applying, rejected, planned, seen, and
freshly scraped) from `job_scraper/seen_jobs.json` into a readable Markdown file grouped by
status. The JSON stays as Claude's dedup memory; this gives David a browsable list.

`$ARGUMENTS` may optionally name a status to focus on: `applied`, `ignore`, `pending`,
`rejected`, `interview`, `assessment`, `offer`, `ghosted`, `seen`, `new` (or empty for everything).

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
   - ignore → the "🚫 Ignored (skipped)" section
   - etc.
   Read the relevant section from `job_scraper/roles.md` (or grep the JSON) and present it
   as a compact table (Title · Company · Location · link · reason). Keep it short; if the
   section is long (>30 rows) summarize and point to the file.
4. If David asks to change a status, use the tool (or the dedicated commands):
   - `/register <ref> [status]` — record a job applied to (or `python3 tools/jobs.py register "<ref>" <status>`)
   - `/update <ref> <status>` — change status on a response (or `python3 tools/jobs.py update "<ref>" <status>`)
   - `/not-apply <ref> [reason]` — mark `ignore` (or `python3 tools/jobs.py not-apply "<ref>" --reason "..."`)
   Then re-run `render`.

Status vocabulary: `new`, `seen`, `pending`, `ignore`, `applied`, `assessment`,
`interview`, `offer`, `ghosted`, `rejected`. Applied-stage statuses are auto-synced to
`job_search_tracker.csv`.
