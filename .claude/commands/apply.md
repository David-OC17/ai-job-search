# /apply - Drafter-Reviewer Job Application Workflow

You are orchestrating a two-agent job application workflow. The job posting is provided below as `$ARGUMENTS` (either a URL or pasted text).

Follow these steps **exactly in order**. Do not skip steps.

**Token-efficiency rules for this workflow:**
- Never re-Read a file whose contents are already in your context from an earlier step. If you read it in Step 1, it is still available in Step 2.
- When dispatching the reviewer agent, pass draft content **inline in the agent prompt** rather than asking the agent to Read files you already have in memory.
- Run the full verification checklist exactly once, at the end (Step 6). The reviewer focuses on content critique, not verification.
- Step 5 (compile and inspect PDFs) is mandatory and non-skippable — LaTeX page-break decisions are unpredictable, and `.tex` files that look fine often produce broken PDFs (orphaned entry titles, cover letters spilling to page 2, bullet fonts mismatching).

---

## Step 0: Parse Input

- If `$ARGUMENTS` looks like a URL, use `WebFetch` to retrieve the job posting content.
- If it is pasted text, use it directly.
- Extract: **company name**, **role title**, **department** (if mentioned), and **location**.
- Applications are **always written in English** (CV and cover letter alike), regardless of the posting language.
- Check the location against `target-countries.md`. If it is Tier 4 or hits a hard requirement David can't meet (US-citizen/clearance/ITAR, on-site in a no-visa country), say so up front — the user may still choose to proceed, but flag it.
- Store these for use throughout the workflow.

---

## Step 1: DRAFTER - Evaluate Fit

Read the evaluation framework:
- `.claude/skills/job-application-assistant/04-job-evaluation.md`
- `.claude/skills/job-application-assistant/01-candidate-profile.md`

Using the framework from `04-job-evaluation.md`, evaluate the job posting against the candidate's profile. If the salary lookup tool is configured, run:

```bash
python salary_lookup.py "<Company Name>" --json
```

If the posting specifies a city, add `--city "<City>"` to narrow results. Parse the JSON output and include the salary benchmark in the evaluation. If the tool is not configured or returns an error, skip the salary benchmark.

Present the evaluation to the user with:

1. **Skills match** - which required/preferred skills match vs. gaps
2. **Experience match** - how work history maps to the role
3. **Behavioral/culture match** - how behavioral profile fits the role/company culture
4. **Salary benchmark** - salary index for the company (if available)
5. **Overall fit score** and recommendation (strong fit / moderate fit / weak fit)

After presenting the evaluation, ask the user:
> "Should I proceed with drafting the CV and cover letter for this role?"

**If the user says no, stop here.** If yes, continue to Step 2.

---

## Step 2: DRAFTER - Draft CV + Cover Letter

You already have `01-candidate-profile.md` and `04-job-evaluation.md` in context from Step 1. **Do not re-read them.**

Read only the reference files you do not yet have:
- `.claude/skills/job-application-assistant/03-writing-style.md`
- `.claude/skills/job-application-assistant/05-cv-templates.md`

Also read the master CV so you know the full inventory of experience/projects/bullets available to select from:
- `cv/resume.tex` (top-level layout) and every file in `cv/sections/` (`experience.tex`, `education.tex`, `projects.tex`, `skills.tex`, and the optional `awards.tex`, `research.tex`, `volunteer.tex`). The master keeps many **commented-out bullet and project variants** — tailoring means choosing which to enable, not inventing new content.

### CV — tailor a per-company copy of the resume.cls master (always English)

Create an isolated build directory so the master is never clobbered:

```
cv/applications/<Company>/
  ├── resume.cls        (copy of cv/resume.cls)
  ├── resume.tex        (copy of cv/resume.tex)
  └── sections/*.tex    (copies of cv/sections/*, then tailored)
```

Tailoring rules (single page, pdflatex):
- **Select, don't fabricate.** Turn commented bullet/project variants on or off to match the posting's keywords and stack. Reorder projects so the most relevant appear first. Never add a skill, project, or metric David doesn't already have somewhere in the master.
- Adjust `sections/skills.tex` ordering to lead with the stack the posting names.
- Keep the header (name/contact) identical to the master.
- Target **exactly one page** — this is a resume, not a 2-page CV.
- Any mention of agentic coding or AI tooling must reference **Claude Code** by name.

### Cover Letter — only when the posting asks for one (default: skip)

David sends resumes only. Generate a cover letter **only if** the posting requires or explicitly invites one, or the user asks. When you do:
- Write it in **English**, use the `cover.cls` template (read `06-cover-letter-templates.md` for structure), output to `cover_letters/cover_<company>_<role>.tex`.
- Tailor the opening to the role/company; address a named person if the posting has one, else "Dear Hiring Manager."
- Keep to ~one page; reference **Claude Code** by name for any AI-tooling mention.

If you skip the cover letter, note that in the final summary and ignore all cover-letter substeps below.

Write the file(s) to disk. Keep the exact text of the drafts in working memory — you will pass them inline to the reviewer in Step 3 and revise them in Step 4 without re-reading.

---

## Step 3: REVIEWER - Research & Critique

Use the **Agent tool** to spawn a `general-purpose` reviewer agent. The reviewer gets a fresh context, so pass the drafts **inline in the prompt** below (do not make the reviewer Read them). Scope the reviewer's file reads to content-critique essentials only — the reviewer does not need the LaTeX template files (`05`, `06`) to critique content, since those govern structural/LaTeX concerns the drafter already applied.

Replace `<COMPANY>`, `<ROLE>`, `<INSERT_JOB_POSTING_TEXT_HERE>`, `<INSERT_CV_DRAFT_HERE>`, and `<INSERT_COVER_LETTER_DRAFT_HERE>` with actual values before dispatching.

```
You are a hiring manager proxy reviewing a job application. Your job is to make the application as targeted and compelling as possible.

## Your Tasks

### 1. Research the Company
Use WebSearch and WebFetch to research:
- The company's website, mission, and recent news
- The specific department or team (if mentioned in the posting)
- Any recent projects, press releases, or strategic initiatives relevant to the role
- Company culture and values

### 2. Read Reference Materials (content-critique only)
Read these four files — and only these — to ground your critique:
- `.claude/skills/job-application-assistant/01-candidate-profile.md`
- `.claude/skills/job-application-assistant/02-behavioral-profile.md` — use this specifically to check whether the cover letter's voice matches the candidate's natural register. A "Collaborator" PI profile, for example, should not be given a combative, solo-hero tone; a "Persuader" profile should not be given over-hedged, apologetic phrasing.
- `.claude/skills/job-application-assistant/03-writing-style.md`
- `.claude/skills/job-application-assistant/04-job-evaluation.md`

Do NOT read `05-cv-templates.md` or `06-cover-letter-templates.md` — those govern LaTeX structure the drafter already applied and are not needed for content critique.

### 3. Drafts to Review
Both drafts are provided inline below. Do NOT use the Read tool on the draft files — use these exact texts.

<CV_DRAFT file="cv/applications/<COMPANY>/sections/*.tex (tailored resume.cls sections)">
<INSERT_CV_DRAFT_HERE>
</CV_DRAFT>

<!-- Include this block ONLY if a cover letter was generated; otherwise omit it and tell the reviewer to critique the CV only. -->
<COVER_LETTER_DRAFT file="cover_letters/cover_<COMPANY>_<ROLE>.tex">
<INSERT_COVER_LETTER_DRAFT_HERE>
</COVER_LETTER_DRAFT>

### 4. Job Posting
<JOB_POSTING>
<INSERT_JOB_POSTING_TEXT_HERE>
</JOB_POSTING>

### 5. Produce Feedback

Return your feedback in **two parts**:

**Part A — Structured edits (preferred format whenever possible):**
A JSON array of concrete edits the drafter can apply directly without re-reading the files. Each edit is an object:
```json
{
  "file": "cv/applications/<COMPANY>/sections/<section>.tex" | "cover_letters/cover_<COMPANY>_<ROLE>.tex",
  "old_string": "<exact text currently in the draft>",
  "new_string": "<replacement text>",
  "reason": "<one-line rationale: keyword match / company angle / reframing / style>"
}
```
Only use this format when you can quote the exact `old_string` from the drafts above. Make `old_string` unique — include enough surrounding context so it matches exactly once per file.

**Part B — Narrative suggestions (for judgment calls that are not mechanical edits):**
Prose suggestions grouped by category. Produce each category even if your finding is "no issues" — silence on a category can be mistaken for skipping it.
- **Missed keywords/requirements** — what to add and roughly where, if it cannot be expressed as a clean string replacement
- **Company/department-specific angles** — connections between experience and the company's strategic priorities, based on your research
- **Action-oriented reframing** — identify passive, generic, or low-energy statements and suggest action-oriented rewrites. Use this category especially for structural weakness that doesn't fit a single-sentence swap (e.g., "the whole opening paragraph reads as passive — restructure around your single strongest match to the posting").
- **Tone and style issues** — check against `03-writing-style.md` AND `02-behavioral-profile.md`. Flag any issues with tone, formality, or voice (cliches, hedging, over-humility, inconsistent register), and specifically flag any mismatch between the letter's voice and the candidate's natural register as described in the behavioral profile.

**CRITICAL RULE:** All suggestions must be grounded in actual profile data. Do NOT suggest fabricating skills, experience, or achievements. If a requirement is a gap, say so honestly and suggest how to frame adjacent experience instead.

Do **not** run a verification checklist — the drafter will do that in the final step. Focus on content critique.

Return Part A and Part B together as a single structured message.
```

---

## Step 4: DRAFTER - Revise Based on Feedback

Once the reviewer agent returns its feedback:

1. **Apply Part A (structured edits) directly with the Edit tool.** Do NOT re-read the draft files — you already have them in context from Step 2, and the reviewer's `old_string` values were quoted from that same text. For each edit in the JSON array, call `Edit` with the given `file`, `old_string`, and `new_string`. Skip any whose rationale would require fabricating content.
2. **Apply Part B (narrative suggestions)** using judgment. These need interpretation, not mechanical replacement. Walk through every Part B category the reviewer returned and address it:
   - **Missed keywords/requirements:** add the keyword or capability where it fits naturally in the CV or cover letter. Prefer the experience bullets (concrete evidence) over the profile statement (abstract claim).
   - **Company/department-specific angles:** weave the reviewer's research into the cover letter opening or motivation paragraph. Verify every company claim via WebFetch/WebSearch before including it — do not trust reviewer research at face value.
   - **Action-oriented reframing:** rewrite passive or generic phrasing (CV profile statement, cover letter opening, bullet leads). Structural weakness that the reviewer flagged without a clean JSON edit lives here.
   - **Tone and style issues:** apply the writing-style-guide fixes (no em-dashes, no cliches, no apologetic hedging, consistent first-person active voice).
   Use Edit for targeted changes; only re-read a file if an edit fails because the surrounding text has shifted.
3. Do NOT incorporate any suggestion that would fabricate skills or experience. If a posting requirement is a genuine gap, acknowledge it honestly and frame adjacent experience instead.

After all edits are applied, the two files on disk are the final drafts.

---

## Step 5: DRAFTER - Compile & Inspect PDFs (MANDATORY)

**Never skip this step.** The `.tex` files looking fine is not sufficient — LaTeX page-break decisions are unpredictable and commonly produce broken layouts (orphaned job titles separated from their bullets, cover letters spilling to 2 pages, bullet fonts not matching body text). Compile both documents and visually verify the PDFs before presenting.

### 5a. Compile

```bash
cd cv/applications/<Company> && pdflatex -interaction=nonstopmode resume.tex
# Only if a cover letter was generated:
cd ../../../cover_letters && xelatex -interaction=nonstopmode cover_<company>_<role>.tex
```

- Resume uses **pdflatex** — `resume.cls` is an `article`-based class (sourcesanspro/marvosym/ulem), no fontspec or fontawesome, so pdflatex is correct and fast.
- Cover letter (only if generated) uses **xelatex** — `cover.cls` requires fontspec.

When the resume compiles clean, copy the PDF to David's naming convention: `David_Ortiz-Resume-<Company>.pdf`.

If a compile fails, fix the error and re-compile until clean.

### 5b. Inspect layout

Read the PDF(s) via the Read tool and verify:

**Resume (`cv/applications/<Company>/resume.pdf`):**
- [ ] **Exactly 1 page** — if it spills to page 2, trim by disabling lower-relevance project/bullet variants until it fits.
- [ ] No orphaned headings — a role/project title must not sit alone at the bottom with its bullets pushed below.
- [ ] No awkward whitespace gaps; the negative `\vspace` values still look balanced.

**Cover letter (`cover_letters/cover_<company>_<role>.pdf`) — only if generated:**
- [ ] Exactly 1 page
- [ ] Signature block visible, not cut off or pushed to a second page
- [ ] Bullet list font matches surrounding body text (both should be Raleway-Medium)

### 5c. Iterate until clean

If the layout has problems, edit the section `.tex` files and recompile. Common fixes (see `05-cv-templates.md` for full details):

- **Resume spills to page 2:** disable (comment out) the lowest-relevance project or bullet variant using **relevance-weighted cutting** (see `05-cv-templates.md`). Score each candidate line by (a) relevance to THIS posting's keywords and responsibilities, (b) uniqueness, (c) narrative load. Comment out the lowest-total-score line first, regardless of section. The master already ships alternate/shorter bullet variants — prefer swapping to a shorter variant over deleting a whole entry.
- **Resume ends thin (well short of a full page):** enable one more relevant project or the longer bullet variant so the page looks complete.
- **Orphaned title at page bottom:** reorder entries or trim the entry above so the title and its bullets stay together.
- **Cover letter itemize breaks compile or uses wrong font:** close `\lettercontent{}` before the list, wrap the list in `{\raggedright\fontspec[Path = OpenFonts/fonts/raleway/]{Raleway-Medium}\fontsize{11pt}{13pt}\selectfont \begin{itemize}...\end{itemize}\par}`
- **Cover letter spills to 2 pages:** trim using the same relevance-weighted logic. First cut: sentences that restate what a bullet already said. Second cut: a bullet that does not hit posting keywords. Last resort: a bullet that does hit posting keywords. Never reduce geometry or line spacing.

Do not proceed to Step 6 until both PDFs pass inspection.

### 5d. Clean up build artifacts

After the final clean compile, delete the `.aux`, `.log`, `.out` files (keep the `.tex` and `.pdf`).

---

## Step 6: Present Final Output

Run the full verification checklist from `CLAUDE.md` now — this is the **only** verification pass in the workflow. Re-read both files once here to verify final state on disk matches your mental model after the Step 4 and Step 5 edits.

### Verification Checklist
Report pass/fail for each item in the CLAUDE.md verification checklist (factual accuracy, targeting, consistency, quality).

### Key Tailoring Decisions
Summarize 3-5 key decisions made to tailor the application:
- What was emphasized and why
- What company-specific angles were incorporated
- What the reviewer suggested that was most impactful
- Any gaps that were acknowledged or reframed

### Files Created
List the files written:
- `cv/applications/<Company>/` (tailored resume + `David_Ortiz-Resume-<Company>.pdf`)
- `cover_letters/cover_<company>_<role>.tex` — **only if** a cover letter was generated

Tell the user which files are ready for review, and note explicitly whether a cover letter was produced or skipped. Ask them to open the PDF(s) before sending.
