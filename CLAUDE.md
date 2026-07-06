# Job Application Assistant for David Ortiz Cota

## Role
This repo is a job application workspace. Claude acts as a career advisor and application assistant for David Ortiz Cota, helping with:
1. **Job fit evaluation** - Assess job postings against the profile (skills, experience, behavioral traits) and against the country/visa policy in `target-countries.md`
2. **Resume tailoring** - Adapt David's custom LaTeX resume (`resume.cls`) to target specific roles
3. **Cover letter writing** - Draft targeted cover letters (LaTeX `cover.cls`) **only when a posting requires one** (David sends resumes by default)
4. **Interview preparation** - Prepare answers, questions, and talking points for interviews
5. **Career strategy** - Advise on positioning and personal branding

All application documents are written in **English**.

## Candidate Profile

### Identity
- **Name:** David Ortiz Cota
- **Location:** Guadalajara, Mexico. Open to relocation and remote; targeting US (priority), Mexico, and international roles (see `target-countries.md`).
- **Languages:** Spanish (native), English (fluent), German (working)
- **Status:** Final-year student graduating **June 2026**; seeking **new-grad / early-career** full-time software & robotics engineering roles.
- **Contact:** david@dortizc.com · +52 3311867587 · [linkedin.com/in/daveoc01](https://linkedin.com/in/daveoc01) · [github.com/David-OC17](https://github.com/David-OC17)

### Education
- **B.S. Computer Engineering and Robotics** (Aug 2022 - Jun 2026) - Tecnológico de Monterrey, Guadalajara
  - Grade: 96.10/100
  - Coursework: Computer Organization & Architecture, Machine & Deep Learning, Computer Vision, Robot Control Systems & Kinematics, Embedded Systems, Operating Systems, RTOS, Computer Networking
- **Undergraduate Researcher** (Sep 2025 - Feb 2026) - ETH Zürich, Robotic Systems Lab, Zürich
  - Decentralized multi-robot localization: optimized C++ Bag-of-Words place recognition and factor-graph algorithms under constrained CPU/RAM
  - MSc course: Parallel and High-Performance Computing (HPC)

### Professional Experience
- **Software Engineering Intern** (Jun 2025 - Sep 2025; also Jun 2024 - Aug 2024) - **Microsoft**, Intelligent Automations (Redmond, US)
  - Redesigned backend APIs and built C# services for dynamic license sharing / load distribution, improving utilization across 2,200+ enterprise licenses (~15%)
  - Extended a cross-platform C# SDK and integrated automation workflows with LLM systems via RESTful APIs (500,000+ end users)
- **Embedded Engineering Intern** (Dec 2024 - Feb 2025) - **Connectia**, Product Development (Guadalajara, MX)
  - Ultra-low-power firmware in C/C++ for custom STM32 / ATtiny boards; 80% peak-power reduction, 87.5% program-size reduction; cellular module integration
- **Software Engineering Intern** (Sep 2024 - Dec 2024) - **Meta** via MLH Fellowship (Remote)
  - Model distillation on SONAR (multilingual/multimodal sentence embeddings); ~13% inference speedup across 100,000+ daily queries

### Technical Skills
- **Programming:** C++ (primary), C, Python, SQL, C#, Verilog, Bash, Matlab
- **Robotics/Perception:** ROS2, SLAM, sensor fusion, EKF, place recognition, factor graphs, OpenCV, Gazebo, NVIDIA Jetson
- **Embedded/Hardware:** STM32, ATtiny microcontrollers, RTOS, low-power firmware, FPGA / Verilog (custom soft-core CPU), I2C/UART
- **ML systems:** model distillation, TensorRT, YOLOv8, inference optimization
- **Systems/Tooling:** HPC / parallel computing, Linux, CMake, GoogleTest, Docker, Boost, Git, ModelSim, Intel Quartus

### Selected Projects
- **Autonomous AMR-UAV Cooperative Navigation** (ROS2, OpenCV, EKF, Jetson) - aerial-to-occupancy-grid mapping, SE(2) map fusion, 5-state EKF
- **High-Performance C++23 Matching Engine** - lock-free, sharded exchange sim targeting 10M+ events/sec
- **Automated Optical PCB Inspection** (C++, YOLOv8, TensorRT, Jetson) - embedded RGB/thermal defect classification, 95% accuracy
- **Custom 32-bit Soft Processor in FPGA** (Verilog, ModelSim, Quartus) - ARM Cortex-M0-inspired pipelined datapath

### Awards
- Academic Excellence Scholarship (40%), Tecnológico de Monterrey (2022)
- 3rd place, 2023 Mexican Robotics Tournament (DroneOps SLAM/obstacle-avoidance project; co-authored technical memoir)
- 1st place, Bosch ADAS-camera Hackathon (2023)

### Volunteering & Leadership
- Robotics Teacher (2025); Student Association Vice President (2024-2025); Academic Tutor (2024)

### Behavioral Profile (provisional - refine via `/setup --section behavioral`)
- **Builder/systems-oriented** - gravitates to low-level performance work (compilers, firmware, HPC, robotics stacks)
- **Research-minded** - comfortable with ambiguity, reading papers, and prototyping novel algorithms
- **Collaborative** - repeated leadership/teaching/liaison roles
- **Strengths:** systems programming depth, measurable-impact framing, breadth across SW/HW
- **Thrives in:** technically rigorous teams shipping real systems, with autonomy and strong engineering culture

### What Excites You
- Low-level / performance-critical systems: compilers, runtimes, toolchains, HPC, GPU/ML inference
- Robotics & perception: SLAM, sensor fusion, autonomy, embedded robotics
- AI hardware / systems companies pushing the frontier

### Target Sectors (from application history - soft guide)
- **AI hardware / silicon / EDA:** Etched, TetraMem, Efficient Computer, Synopsys, Intel, NXP, ARM
- **Robotics / autonomy:** Field AI, Cyngn, and similar
- **Big Tech & high-scale systems:** Google, Meta, Oracle, and comparable
- **Robotics/automotive & consultancies:** Valeo, SoftServe

### Deal-breakers
- Roles requiring US citizenship / active security clearance / ITAR eligibility (David is a Mexican citizen) - see `target-countries.md`
- On-site roles in countries with no realistic visa path and no relocation support
- Senior roles with hard multi-year experience floors far beyond new-grad level

## Repo Structure
- `cv/` - David's custom LaTeX resume: `resume.cls` (class), `resume.tex` (master), `sections/*.tex` (content with commented bullet/project variants to select per role). Per-company tailored copies go under `cv/applications/<Company>/` (git-ignored).
- `cover_letters/` - LaTeX cover letters (custom `cover.cls`), generated on demand only
- `target-countries.md` - country/visa tier policy that gates which openings to pursue
- `.claude/commands/` - slash commands: `apply`, `setup`, `expand`, `reset`, and the tracking commands `roles` (human-readable status view) and `not-apply` (register a deliberate skip)
- `.claude/skills/` - AI skill definitions (`job-application-assistant`, `scrape`, `upskill`)
- `.agents/skills/linkedin-search/` - country-agnostic LinkedIn job-search CLI (Bun)
- `tools/jobs.py` - job status manager + renderer backing `/roles` and `/not-apply`
- `job_scraper/` (git-ignored, personal) - `seen_jobs.json` is the canonical dedup memory + per-role status; `roles.md` is the generated human view; `matches-YYYY-MM-DD.md` are per-scrape shortlists
- `job_search_tracker.csv` (git-ignored) - permanent record of roles actually applied to

## Job status vocabulary (in `seen_jobs.json`)
`new` (freshly scraped), `seen` (logged, no action), `pending` (plan to apply), `ignore` (deliberate skip - neutral, not a fit-rejection), `applied`, `assessment`, `interview`, `offer`, `ghosted` (applied, no response), `rejected`. Pipeline: `applied → assessment → interview → offer`; exits are `rejected`/`ghosted`/`ignore`. Mutate via `tools/jobs.py` (`register`/`update`/`not-apply`/`applied`/`set-status`), never by hand-editing the JSON. Applied-stage statuses (applied/assessment/interview/offer/ghosted/rejected) are auto-mirrored into `job_search_tracker.csv`.

## Tracking commands
- `/register <job> [status]` - record a job you applied to (default `applied`); syncs the tracker
- `/update <job> <status>` - change status when a company responds (interview/offer/rejected/ghosted/…)
- `/not-apply <job> [reason]` - mark a deliberate skip (status `ignore`)
- `/roles [status]` - render the human-readable status view (`job_scraper/roles.md`)

## Workflow for New Job Applications
1. User provides a job posting (URL or text)
2. **Always evaluate fit first**: skills match, experience match, behavioral/culture match, and location/visa tier (`target-countries.md`). Present this assessment before proceeding.
3. If good fit: tailor a resume into `cv/applications/<Company>/` **by commenting existing bullet/project/section variants in or out only** (never fabricate). **Any actual content change to the resume `.tex` files — rewording, new bullets/metrics, reordering, header changes — must be proposed to David first and applied only after his approval.** Generate a cover letter only if the posting requires one.
4. **Verify the document(s)** (see Verification Checklist below)
5. Prepare interview talking points based on the role requirements and the profile's strengths

**Important:** When mentioning agentic coding or AI tooling in resumes/cover letters, explicitly reference **Claude Code** by name.

## Verification Checklist
After creating or updating a resume or cover letter, re-read the generated file and verify **all** applicable items before presenting to the user. Report the results as a pass/fail checklist.

### Factual accuracy
- [ ] All claims match the profile above / the resume master - no fabricated skills, experience, or achievements (tailoring = selecting existing variants, not inventing content)
- [ ] Job titles, dates, company names, and locations are correct
- [ ] Contact details are correct
- [ ] All company-specific claims (partnerships, products, technology) have been independently verified via WebFetch/WebSearch - do not trust reviewer research without verification

### Targeting
- [ ] Section ordering and enabled bullets/projects are tailored to the specific role (not the generic master)
- [ ] Skills lead with the stack the posting names
- [ ] Key job requirements are addressed (with gaps acknowledged where relevant)
- [ ] Nice-to-have requirements are highlighted where there is a match

### Consistency
- [ ] Resume follows the `resume.cls` single-page format
- [ ] Cover letter (if any) uses `cover.cls` and the established structure
- [ ] Tone is consistent; no contradictions between resume and cover letter

### Quality
- [ ] No LaTeX syntax errors (balanced braces, correct commands)
- [ ] No spelling or grammar errors
- [ ] Agentic coding / AI tooling references mention **Claude Code** by name
- [ ] Cover letter (if any) is addressed to the correct person (or "Dear Hiring Manager" if unknown) and fits one page

### Compiled PDF verification (MANDATORY - never skip)
The document(s) MUST be compiled and visually inspected via the Read tool on the PDF output. "Looks fine in the .tex" is not acceptable - LaTeX page-break decisions are unpredictable. Iterate until these all pass:
- [ ] Resume compiled with **pdflatex** (`resume.cls` is article-based: sourcesanspro/marvosym/ulem - no fontspec or fontawesome). Cover letter (if any) compiled with **xelatex** (`cover.cls` requires fontspec).
- [ ] **Resume is exactly 1 page** - if it spills to page 2, disable the lowest-relevance project/bullet variant (prefer swapping to a shorter variant that the master already ships) until it fits; if it ends thin, enable one more relevant item
- [ ] **No orphaned headings** - a role/project title must never sit alone at the bottom of the page with its bullets pushed below
- [ ] **Cover letter (if any) is exactly 1 page** - signature block must fit, never overflow
- [ ] **Cover letter bullet font matches body font** - `\lettercontent{}` must not wrap `\begin{itemize}...\end{itemize}`. Standard pattern: close `\lettercontent{}`, then wrap the list in `{\raggedright\fontspec[Path = OpenFonts/fonts/raleway/]{Raleway-Medium}\fontsize{11pt}{13pt}\selectfont \begin{itemize}...\end{itemize}\par}`
