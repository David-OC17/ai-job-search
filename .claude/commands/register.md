# /register - Register a job you applied to

Record a job you applied to (typically **outside** the `/apply` flow — e.g. you applied
directly on a company site). It sets the job's status in `job_scraper/seen_jobs.json` and,
because the status is an applied-stage one, **also upserts a row in `job_search_tracker.csv`**
(your permanent applied record). It then shows under the right status in `/roles`.

`$ARGUMENTS` is the job reference plus an optional status and reason. The reference may be a
**LinkedIn URL, a numeric job id, or free text** (company / title).

Default status is `applied`. Valid statuses (full vocabulary):
`new`, `seen`, `pending`, `ignore`, `applied`, `assessment`, `interview`, `offer`, `ghosted`, `rejected`.

## Steps

1. Parse `$ARGUMENTS` into `<ref>`, an optional `<status>` (default `applied`), and an
   optional reason. If the user just gives a URL/company, assume `applied`.
2. Run the tool:
   ```bash
   python3 tools/jobs.py register "<ref>" <status> --company "<Company>" --title "<Role>" --location "<Location>"
   ```
   - Pass `--company/--title/--location` when the ref is a URL not already in `seen_jobs.json`,
     so both the JSON entry and the tracker row are readable. Pull details from
     `job_scraper/matches-*.md` if present, or `WebFetch`/the LinkedIn CLI `detail` if needed.
   - If the tool reports the ref is **ambiguous**, show the candidates and ask which one.
   - If the status is invalid, the tool lists the valid ones — pick the closest and retry.
3. Refresh the human view:
   ```bash
   python3 tools/jobs.py render
   ```
4. Confirm to the user: the role, the status set, and that it's now in both the tracker and
   `/roles`. For applied-stage statuses the tracker row is created automatically — do not
   hand-edit the CSV.

Use `/update` to change the status later when a response arrives.
