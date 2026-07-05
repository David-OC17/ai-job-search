# Job Evaluation Framework

<!-- SETUP: Skill match areas and career goals are personalized by running /setup -->

## Scoring Dimensions

Evaluate each job posting against these five dimensions:

### 1. Technical Skills Match (0-100)
How well do the required/preferred skills align with the candidate's capabilities?

| Score | Meaning |
|-------|---------|
| 80-100 | Core requirements are primary skills |
| 60-79 | Most requirements match, 1-2 gaps that are learnable |
| 40-59 | Partial match, significant upskilling needed |
| 0-39 | Fundamental mismatch |

**Strong match areas:** C++/C systems programming, robotics & perception (SLAM, sensor fusion, EKF, ROS2), embedded/firmware (STM32, ATtiny, RTOS), FPGA/Verilog, ML inference optimization (TensorRT), HPC/parallel computing
**Moderate match areas:** Python ML/DL, C# backend/SDKs, computer vision (OpenCV/YOLOv8), SQL, distributed/high-scale systems
**Weak match areas:** large-scale production frontend/web, cloud-platform ops at scale, roles needing many years of professional (non-intern) experience

### 2. Experience Match (0-100)
Does work history align with what they're looking for?

| Score | Meaning |
|-------|---------|
| 80-100 | Direct experience in the same domain and role type |
| 60-79 | Related experience, transferable skills clear |
| 40-59 | Adjacent experience, would need to make the case |
| 0-39 | Unrelated experience |

**Strong:** systems/backend SWE (Microsoft), embedded firmware (Connectia), ML systems (Meta), robotics research (ETH Zürich) - all as internships/research
**Moderate:** compilers/runtimes/toolchains, autonomy/perception production roles, GPU/ML infra (strong adjacent projects, no full-time yet)
**Entry-level:** all full-time roles - David is a new grad (Jun 2026); target new-grad / early-career / university-grad postings, not senior IC roles

### 3. Behavioral/Culture Fit (0-100)
Does the role and company culture match the behavioral profile?

| Score | Meaning |
|-------|---------|
| 80-100 | Culture strongly matches behavioral preferences |
| 60-79 | Mixed signals but mostly compatible |
| 40-59 | Some friction areas |
| 0-39 | Significant culture mismatch |

**Red flags to research:** Department disorganization, work dominated by maintenance over development, poor chemistry with leadership, culture mismatches. Check reviews, media coverage, LinkedIn connections, and network contacts for insider perspective.

### 4. Location & Visa (Pass/Flag/Fail - see `target-countries.md`)
- Tier 1-2 country (US, MX, CA, UK, DE, NL, CH, IE, AU) or remote-worldwide/Americas-tz: PASS
- Tier 3 country (rest of EU, NZ, SG, UAE, JP): PASS, flag "visa-dependent - confirm sponsorship"
- Tier 4 country / no realistic visa path with no relocation support: FAIL
- Hard requirement David can't meet (US-citizen / active clearance / ITAR): FAIL
- Note: TN visa is available to Mexican citizens for many US engineering roles - a US role is still a PASS if the employer will sponsor TN/H-1B/O-1 or accepts STEM OPT

### 5. Career Alignment & Motivation (0-100)
Does this role advance career goals and contain tasks that energize?

| Score | Meaning |
|-------|---------|
| 80-100 | Strongly aligned with career direction, clear growth path |
| 60-79 | Good role but only partially aligned with long-term goals |
| 40-59 | Decent job but doesn't build toward career goals |
| 0-39 | Dead end or backwards step |

**Career goals:**
- Land a strong new-grad SWE / robotics / embedded role at a technically rigorous team (AI hardware, robotics/autonomy, or high-scale systems)
- Do low-level, performance-critical work: compilers/runtimes/toolchains, HPC, GPU/ML inference, robotics stacks
- Build toward deep systems + robotics expertise; ideally at a frontier hardware/AI or autonomy company

**Motivation filter:** Evaluate not just whether David *can* do the tasks, but whether they will *energize* him:
- Tasks that energize: systems/performance engineering, robotics & perception, embedded/firmware, novel algorithm prototyping, research-flavored work
- Tasks that drain: pure CRUD/web-frontend maintenance, low-autonomy ticket-shuffling
- Non-task factors: engineering culture, autonomy, technical caliber of the team, visa sponsorship willingness

**Life situation alignment:**
- **Security**: new grad seeking first full-time role; visa sponsorship is a real factor for non-MX roles
- **Flexibility**: available from ~mid-2026 (graduation June 2026); open to relocation
- **Professional development**: prioritize teams with strong mentorship and hard technical problems

### 6. Salary Benchmark (Optional)

If the salary lookup tool is configured (`salary_data.json` exists), look up the company:
```
python salary_lookup.py "<Company Name>" --json
```

If a city is known from the posting, add `--city "<City>"` to narrow results.

Present findings as:
```
### Salary Benchmark
| Metric | Value |
|--------|-------|
| [Category] index | XX.X (+/-X.X% vs baseline) |
| Overall index | XX.X (+/-X.X% vs baseline) |
```

Interpret results relative to the baseline defined in the data file's metadata. For index-based data, higher typically means above-market compensation.

If the salary tool is not configured, skip this section.

## Output Format

Present the evaluation as:

```
## Job Fit Evaluation: [Role] at [Company]

| Dimension | Score | Notes |
|-----------|-------|-------|
| Technical Skills | XX/100 | [brief note] |
| Experience Match | XX/100 | [brief note] |
| Behavioral Fit | XX/100 | [brief note] |
| Location | PASS/FAIL | [brief note] |
| Career Alignment | XX/100 | [brief note] |

**Overall Score: XX/100** (weighted average of scored dimensions)

### Verdict: [Strong Fit / Good Fit / Moderate Fit / Weak Fit / Poor Fit]

### Key Strengths for This Role
- [bullet points]

### Gaps to Address
- [bullet points]

### Recommendation
[1-2 sentences: apply/skip/apply with caveats]

### Company Research Checklist
- [ ] Checked company website (mission, values, recent news)
- [ ] Checked review sites (Glassdoor, Blind, Levels.fyi, etc.)
- [ ] Checked LinkedIn for team size, recent hires, connections
- [ ] Checked media for restructuring, growth, or workplace issues
- [ ] Identified network contacts who may know the team/manager
```

## Weighting
- Technical Skills: 30%
- Experience Match: 25%
- Behavioral Fit: 15%
- Career Alignment: 30%

(Location is pass/fail, not weighted)

## Thresholds
- **Strong Fit** (75+): Definitely apply, tailor everything
- **Good Fit** (60-74): Apply, address gaps in cover letter
- **Moderate Fit** (45-59): Consider carefully, discuss with user
- **Weak Fit** (30-44): Probably skip unless strategic reasons
- **Poor Fit** (<30): Skip

## Pre-Application: Call the Employer (Best Practice)

Before writing the application, consider whether the candidate should call the contact person listed in the posting. **Only call if there are substantive questions** - never call just to "be remembered."

### When to Suggest Calling
- The posting has unclear or ambiguous requirements
- It's unclear which competencies are essential vs. nice-to-have
- The role description is vague about day-to-day tasks
- There's a named contact person who invites questions

### Good Questions to Ask
- "What are the primary challenges in this role?"
- "How is time typically divided across the listed responsibilities?"
- "Which competencies are most critical for success in this position?"
- "What does success look like in the first 6-12 months?"

### Rules for the Call
- Prepare a 30-second "elevator pitch" about your background in case they ask
- The call's purpose is **gathering information**, not delivering a pitch
- Take notes - use what you learn to tailor the application
- Reference the conversation naturally in the cover letter ("After speaking with [name], I was especially drawn to...")
