# Resume Templates and Tailoring Guide

David uses a **custom single-page LaTeX resume**, not moderncv. Tailoring means
**selecting from existing content variants**, never inventing new claims.

> **Hard rule — comment in/out only.** Per-role tailoring is limited to **commenting
> existing bullet/project/section variants in or out** (LaTeX `%`). Do **not** edit the
> wording of any bullet, add new bullets/metrics/skills, reorder entries, or change the
> header on your own. If any of that seems warranted, **propose it to David as a concrete
> before/after diff and wait for his approval** before writing it. He owns the resume's
> content; you only choose which existing pieces are visible.

## Template: custom `resume.cls`

**Class:** `cv/resume.cls` - an `article`-based class (a4paper, 11pt) using
`sourcesanspro`, `marvosym`, `ulem`, `hyperref`, `enumitem`, `fullpage`. No fontspec,
no fontawesome.
**Master file:** `cv/resume.tex` - the header (name/contact) plus `\input{sections/...}`.
**Content:** `cv/sections/*.tex` - `experience.tex`, `education.tex`, `projects.tex`,
`skills.tex`, and optional `awards.tex`, `research.tex`, `volunteer.tex`.
**Compile with:** **pdflatex** (fast, correct for this class).
**Output:** exactly **1 page**.

### The master ships alternate variants

Each section keeps **commented-out bullet and project variants** (shorter phrasings,
alternate projects, older roles). Tailoring is done by **commenting/uncommenting** these
variants and reordering entries - not by writing new bullets. Example from
`projects.tex`: several `\resumeItem{...}` lines are commented so the base set fits one
page; enable the ones whose keywords match the target posting and disable the rest.

### Custom commands (from `resume.cls`)

- `\resumeQuadHeading{Title}{Date}{Subtitle}{Location}` - experience/research entries
- `\resumeTrioHeading{Title}{Tech/Org}{Year}` - projects/awards
- `\resumeItem{...}` - a bullet
- `\resumeItemListStart` / `\resumeItemListEnd` - bullet list wrappers
- `\resumeSectionType{Label}{:}{Content}` - skills-style rows
- `\resumeHeadingListStart` / `\resumeHeadingListEnd` - section wrappers
- Negative `\vspace{-Nmm}` values are used deliberately to keep everything on one page - keep them balanced when editing.

## Per-company build directory (how `/apply` produces a tailored resume)

Never edit the master in place for a single application. Instead:

```
cv/applications/<Company>/
  ├── resume.cls        (copy of cv/resume.cls)
  ├── resume.tex        (copy of cv/resume.tex)
  └── sections/*.tex    (copies, then tailored by toggling variants)
```

Compile inside that directory (`pdflatex -interaction=nonstopmode resume.tex`) and copy
the result to `David_Ortiz-Resume-<Company>.pdf`. `cv/applications/` is git-ignored.

## Section-by-section tailoring

### Skills (`skills.tex`)
Lead with the stack the posting names. If the role is embedded, order firmware/C/RTOS
first; if robotics, ROS2/C++/perception first; if systems/compilers, C++/systems first.

### Experience (`experience.tex`)
All four internships (Microsoft x2, Connectia, Meta) are strong. Choose the bullet
**variant** that best matches the posting (each role ships a short and a detailed variant).
Keep the most role-relevant metrics.

### Projects (`projects.tex`)
This is the main tailoring lever. ~10 projects exist (most commented). Enable 3-4 whose
tech stack and domain match the posting; disable the rest. Robotics roles -> AMR-UAV,
drone SLAM; systems/HFT -> C++23 matching engine; embedded -> FPGA soft processor, PCB
inspection, 2-DOF control; ML -> PCB inspection, Hyper-Kamiokande.

### Research / Education / Awards / Volunteer
Toggle `research.tex` on for research-heavy roles (ETH Zürich, DroneOps). Keep education
always. Awards/volunteer are optional space fillers - enable only if the page is thin.

## Compile-and-inspect loop (MANDATORY)

1. `pdflatex -interaction=nonstopmode resume.tex` inside the build dir
2. Confirm the page count is **exactly 1** (`pdfinfo resume.pdf | grep Pages`)
3. Read the PDF via the Read tool and inspect layout
4. Check for orphaned headings (a title alone at the page bottom)

### Fixing page problems

- **Spills to page 2:** disable the lowest-relevance bullet/project variant (see
  relevance-weighted cutting below), or swap a detailed bullet for its shorter variant.
- **Ends thin (well short of a full page):** enable one more relevant project, the longer
  bullet variant, or an optional section (research/awards/volunteer).
- **Orphaned heading:** reorder entries or shorten the entry above it.
- **Never** compress geometry or delete the negative `\vspace` tuning to force a fit.

## Relevance-weighted cutting (the right way to shrink a resume)

**Cut by signal, not by section.** For every candidate line, score three things:

1. **Relevance to THIS posting** - does it hit a named tool, keyword, or responsibility?
2. **Uniqueness** - is it the only place this claim appears?
3. **Narrative load** - does a cover letter (if any) depend on it?

Disable the lowest-total-score line first, regardless of section. An older-role or
"lower-priority" project that speaks directly to the posting beats a recent one that does not.

### Practical order of cuts (easiest -> last resort)
1. **Redundancy** - a claim duplicated across projects and experience.
2. **Low-relevance projects** - disable projects whose stack the posting never mentions.
3. **Detailed -> short bullet variant** - swap to the shorter phrasing the master ships.
4. **Optional sections** - drop awards/volunteer before touching core experience.
5. **Last resort** - trim an older role to fewer bullets.

### Pitfalls
- Do not cut the one concrete example a cover letter leans on.
- Do not invent content to fill space - only enable variants that already exist.
- Do not reduce geometry/line spacing to force-fit.
