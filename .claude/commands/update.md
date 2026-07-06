# /update - Change a job's status when you hear back

Update the status of a job already tracked in `job_scraper/seen_jobs.json` — use it when a
company responds (moves you to `assessment`, `interview`, `offer`, or `rejected`), when you
stop hearing back (`ghosted`), or to correct any status. If the new status is an applied-stage
one, the change is mirrored into `job_search_tracker.csv` automatically.

`$ARGUMENTS` is the job reference followed by the new status. The reference may be a
**LinkedIn URL, a numeric job id, or free text** (company / title).

Valid statuses: `new`, `seen`, `pending`, `ignore`, `applied`, `assessment`, `interview`,
`offer`, `ghosted`, `rejected`.

Pipeline for reference: `applied → assessment → interview → offer`, with `rejected`,
`ghosted` (silent / no response), or `ignore` as exits.

## Steps

1. Parse `$ARGUMENTS` into `<ref>` and the new `<status>`. If the status is missing or
   invalid, ask the user which of the valid statuses they mean.
2. Run the tool:
   ```bash
   python3 tools/jobs.py update "<ref>" <status> [--reason "<why, optional>"]
   ```
   - If the tool reports the ref is **ambiguous** (matched several roles), show the
     candidates and ask which one (or have the user give the URL / id).
   - If the ref matches nothing, tell the user — they may mean `/register` (for a brand-new
     job) instead.
3. Refresh the human view:
   ```bash
   python3 tools/jobs.py render
   ```
4. Confirm to the user: the role and its old → new status, and whether the tracker was
   updated (applied-stage statuses only).
