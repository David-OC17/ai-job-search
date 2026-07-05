# /not-apply - Register a job you're deliberately skipping

Mark a job as **not applying** — a deliberate skip, **not** a fit-rejection. David has
read (or seen) the role and is choosing to pass (e.g. can't get authorization, timing,
duplicate, or simply not pursuing it). This records it in `job_scraper/seen_jobs.json` so
it stays deduped and never resurfaces in `/scrape`, and it appears under "Not applying"
in the human-readable roles view.

`$ARGUMENTS` is the job reference plus an optional reason. The reference may be a **LinkedIn
URL, a numeric job id, or free text** (company / title).

## Steps

1. Parse `$ARGUMENTS` into a `<ref>` and an optional reason (anything after the ref, or a
   phrase like `reason: ...`). If no reason is given, that's fine — it's optional.
2. Run the tool (single source of truth):
   ```bash
   python3 tools/jobs.py not-apply "<ref>" --reason "<reason if any>"
   ```
   - If `<ref>` is a URL that isn't in `seen_jobs.json` yet, also pass what you know so the
     entry is readable: `--title "..." --company "..." --location "..."`. Pull these from the
     current `job_scraper/matches-*.md` if the row is there; only `WebFetch` the URL if the
     details aren't already available to you.
   - If the tool reports the ref is **ambiguous** (matched several roles), show David the
     candidates and ask which one (or have him give the URL / id).
3. Refresh the human-readable view:
   ```bash
   python3 tools/jobs.py render
   ```
4. Confirm to David: which role was marked not-applying, the reason (if any), and that it
   won't reappear in future scrapes. Do **not** modify `job_search_tracker.csv` — that file
   is for roles actually applied to.

**Never** treat `/not-apply` as negative feedback about the role's quality or David's fit —
it is a neutral "skipping this one" marker.
