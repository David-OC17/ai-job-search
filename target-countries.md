# Target Countries & Location Policy

This file gates **which openings to pursue and which to skip** during `/scrape` and `/apply`.
David is a Mexican citizen finishing a B.S. (grad Jun 2026), **willing to relocate anywhere**
for the right role. He has held a **J-1 visa** before and is **TN-eligible** (fast route for
US engineering roles). The policy below is a **soft guide**: never auto-reject a strong-fit
role — instead apply the visa/tier note and surface the tradeoff to the user.

**Actively targeted markets (from user):** US (priority) and Mexico, plus **Canada, UK &
Ireland, Continental Europe (incl. Nordics), and Australia & New Zealand**. Asia and the
Middle East are opportunistic only (strong-fit roles).

## How to use this file

- **`/scrape`**: after fetching a posting, read its location. Assign it a tier below.
  Present Tier 1–2 first; include Tier 3 but flag the visa/logistics caveat; drop Tier 4.
- **`/apply`**: in the Location dimension of `04-job-evaluation.md`, use the tier +
  visa note instead of a plain PASS/FAIL. A Tier-3 country is still a PASS, annotated
  with "visa-dependent — confirm sponsorship."
- **Remote** always passes regardless of company HQ country, *unless* the posting
  restricts remote to a country/timezone David can't satisfy (see Remote rules).

## Tier 1 — Primary (apply aggressively)

| Country | Code | Notes |
|---------|------|-------|
| United States | US | **Top priority, all locations.** Needs work authorization — target employers that sponsor (H-1B/O-1) or roles open to STEM OPT / TN. **TN visa is available to Mexican citizens** for many engineering roles (fast, but employer must be willing); David has prior J-1 experience. |
| Mexico | MX | Home market, no visa needed. Prioritize **Guadalajara, CDMX, Monterrey, and remote-MX**. |

## Tier 2 — Strong secondary, actively targeted (apply; visa is routine for skilled tech)

All user-selected international markets. Apply as readily as Tier 1 when the role fits.

| Country | Code | Notes |
|---------|------|-------|
| Canada | CA | Global Talent Stream / Express Entry friendly to CS/robotics. |
| United Kingdom | UK/GB | Skilled Worker visa; many tech firms are licensed sponsors. London/Cambridge seen in past search. |
| Ireland | IE/IR | Critical Skills Employment Permit covers software roles. |
| Australia | AU | Skilled visas; robotics/mining-tech demand. |
| New Zealand | NZ | Skilled migrant / accredited-employer work visa. |
| Germany | DE | EU Blue Card; German language (David has some) is a plus. |
| Netherlands | NL | Highly Skilled Migrant scheme, English-friendly. |
| Switzerland | CH | David has ETH Zürich ties; strong robotics/embedded market. |
| Rest of Continental Europe / EEA | — | Spain, Italy, France, Portugal, Sweden, Denmark, Norway, Finland, Austria, Belgium, Poland, Czechia, etc. EU Blue Card or national skilled-worker permits. Treat as actively targeted; annotate "visa-dependent" only when a posting says no sponsorship. |

## Tier 3 — Opportunistic (apply only on strong fit; flag visa caveat)

Asia (Singapore, Japan, etc.) and the Middle East (UAE, etc.). Not a focus — apply when the
role is a strong technical match; annotate "visa-dependent — confirm sponsorship."

## Tier 4 — Skip by default

- Countries with no realistic work-authorization path for a Mexican new grad, or
  postings that explicitly require existing citizenship/clearance David lacks
  (e.g. US roles gated on "US citizen / green card required / active security clearance",
  ITAR-restricted defense roles).
- Any location the user later adds to the **Excluded** list below.

**Excluded (hard no — user-maintained):**
- _(none yet — add countries/cities you never want here)_

## Remote rules

- **Remote, worldwide / LATAM / Americas-timezone** → Tier 1 (apply).
- **Remote but country- or timezone-locked** to a place David can't legally work from
  or reach in-timezone → treat as that country's tier; if it hard-requires in-country
  presence/authorization, drop to Tier 4.
- Prefer roles that say "remote (Mexico OK)" or "remote (global)".

## Hard requirements to screen out (any tier)

Skip regardless of country when a posting requires something David cannot meet:
- "US citizenship required" / "must hold active security clearance" / "ITAR"
- Years-of-experience floors far above new-grad (e.g. "8+ years") — unless clearly mislabeled
- On-site in a Tier-4 location with no relocation/visa support
