#!/usr/bin/env python3
"""Job status manager + human-readable renderer.

Single source of truth: job_scraper/seen_jobs.json (Claude's dedup memory).
This tool mutates status there and renders readable Markdown for humans.

Usage:
  python tools/jobs.py not-apply <ref> [--reason R] [--title T] [--company C] [--location L] [--url U]
  python tools/jobs.py applied   <ref> [--reason R] ... (same optional fields)
  python tools/jobs.py set-status <ref> <status> [--reason R] ...
  python tools/jobs.py render [--out job_scraper/roles.md]
  python tools/jobs.py find <query>

<ref> may be a LinkedIn URL, a numeric job id, or free text matched against
company/title. If it matches nothing, a new entry is created from the flags.

Statuses: applied, interview, assessment, pending, not_applying, rejected, seen, new
"""
import argparse, json, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEN = os.path.join(ROOT, "job_scraper", "seen_jobs.json")
TODAY = datetime.date.today().isoformat()

STATUS_ORDER = ["applied", "interview", "assessment", "pending",
                "not_applying", "rejected", "seen", "new"]
STATUS_LABEL = {
    "applied": "✅ Applied",
    "interview": "🎤 Interview",
    "assessment": "📝 Assessment",
    "pending": "🕒 Plan to apply",
    "not_applying": "🚫 Not applying (skipped)",
    "rejected": "❌ Rejected",
    "seen": "👁 Seen (no action)",
    "new": "🆕 New (from scrape)",
}


def load():
    if not os.path.exists(SEEN):
        return {"seen": {}}
    with open(SEEN) as f:
        return json.load(f)


def save(data):
    os.makedirs(os.path.dirname(SEEN), exist_ok=True)
    with open(SEEN, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def id_of(url):
    m = re.search(r"(\d{6,})", url or "")
    return m.group(1) if m else ""


def find_key(seen, ref):
    """Return matching key(s) for a ref (url / id / text)."""
    ref = ref.strip()
    if not ref:
        return []
    # direct key hit
    if ref in seen:
        return [ref]
    base = ref.split("?")[0]
    if base in seen:
        return [base]
    # numeric id
    if ref.isdigit():
        return [k for k, v in seen.items()
                if id_of(v.get("url", "")) == ref or id_of(k) == ref]
    # url
    if ref.startswith("http"):
        rid = id_of(ref)
        if rid:
            hit = [k for k, v in seen.items()
                   if id_of(v.get("url", "")) == rid or id_of(k) == rid]
            if hit:
                return hit
        return [k for k, v in seen.items() if v.get("url", "").split("?")[0] == base]
    # free text against company/title/key
    n = norm(ref)
    return [k for k, v in seen.items()
            if n in norm(v.get("company", "")) or n in norm(v.get("title", "")) or n in norm(k)]


def set_status(args):
    data = load(); seen = data["seen"]
    status = args.status
    keys = find_key(seen, args.ref)
    if len(keys) > 1:
        print(f"Ambiguous ref '{args.ref}' matched {len(keys)} entries:", file=sys.stderr)
        for k in keys[:10]:
            v = seen[k]
            print(f"  - {v.get('company')} — {v.get('title')} [{v.get('status')}]", file=sys.stderr)
        print("Refine the ref (use the URL or job id).", file=sys.stderr)
        sys.exit(2)
    if keys:
        key = keys[0]; entry = seen[key]
        entry["status"] = status
        if args.reason: entry["reason"] = args.reason
        for fld in ("title", "company", "location", "url"):
            val = getattr(args, fld, None)
            if val: entry[fld] = val
        entry.setdefault("first_seen", TODAY)
        entry["status_date"] = TODAY
        action = "updated"
    else:
        url = args.url or (args.ref if args.ref.startswith("http") else "")
        key = (url.split("?")[0]) or (norm(args.company) + "|" + norm(args.title)) or args.ref
        seen[key] = {
            "title": args.title or (args.ref if not url else ""),
            "company": args.company or "",
            "location": args.location or "",
            "url": url,
            "first_seen": TODAY,
            "status_date": TODAY,
            "fit": "",
            "status": status,
            "source": "manual",
        }
        if args.reason: seen[key]["reason"] = args.reason
        action = "created"
    save(data)
    e = seen[key]
    r = f" (reason: {e['reason']})" if e.get("reason") else ""
    print(f"{action}: [{status}] {e.get('company') or '?'} — {e.get('title') or key}{r}")


def render(args):
    data = load(); seen = data["seen"]
    buckets = {s: [] for s in STATUS_ORDER}
    unknown = {}  # surface unrecognized statuses instead of hiding them in "seen"
    for k, v in seen.items():
        s = v.get("status", "seen")
        if s in buckets:
            buckets[s].append(v)
        else:
            unknown.setdefault(s, []).append(v)
    lines = [f"# Job Roles — status overview ({TODAY})", ""]
    total = len(seen)
    counts = " · ".join(f"{STATUS_LABEL[s].split(' ',1)[1] if ' ' in STATUS_LABEL[s] else s}: {len(buckets[s])}"
                        for s in STATUS_ORDER if buckets[s])
    lines += [f"**{total} roles tracked.** {counts}", "",
              "_Canonical data lives in `job_scraper/seen_jobs.json` (Claude's dedup memory); this file is a generated human view._", ""]
    def emit(header, rows):
        lines.append(f"## {header} ({len(rows)})"); lines.append("")
        for v in sorted(rows, key=lambda x: (norm(x.get("company")), norm(x.get("title")))):
            comp = v.get("company") or "?"
            title = v.get("title") or "?"
            loc = v.get("location") or ""
            url = (v.get("url") or "").split("?")[0]
            reason = f" — _{v['reason']}_" if v.get("reason") else ""
            link = f" · [link]({url})" if url else ""
            locpart = f" · {loc}" if loc else ""
            lines.append(f"- **{title}** — {comp}{locpart}{link}{reason}")
        lines.append("")

    for s in STATUS_ORDER:
        if buckets[s]:
            emit(STATUS_LABEL[s], buckets[s])
    for s, rows in sorted(unknown.items()):
        emit(f"⚠️ Unknown status '{s}'", rows)
        print(f"WARNING: {len(rows)} role(s) have unrecognized status '{s}'", file=sys.stderr)
    out = args.out or os.path.join(ROOT, "job_scraper", "roles.md")
    with open(out, "w") as f:
        f.write("\n".join(lines))
    print(f"wrote {os.path.relpath(out, ROOT)} — {total} roles ({counts})")


def find(args):
    data = load(); seen = data["seen"]
    for k in find_key(seen, args.ref):
        v = seen[k]
        print(f"[{v.get('status')}] {v.get('company')} — {v.get('title')} · {v.get('url')}")


def main():
    p = argparse.ArgumentParser(description="Job status manager + renderer")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_common(sp):
        sp.add_argument("ref")
        sp.add_argument("--reason"); sp.add_argument("--title")
        sp.add_argument("--company"); sp.add_argument("--location"); sp.add_argument("--url")

    sp = sub.add_parser("not-apply"); add_common(sp); sp.set_defaults(status="not_applying", func=set_status)
    sp = sub.add_parser("applied"); add_common(sp); sp.set_defaults(status="applied", func=set_status)
    sp = sub.add_parser("set-status")
    sp.add_argument("ref"); sp.add_argument("status")
    sp.add_argument("--reason"); sp.add_argument("--title")
    sp.add_argument("--company"); sp.add_argument("--location"); sp.add_argument("--url")
    sp.set_defaults(func=set_status)
    sp = sub.add_parser("render"); sp.add_argument("--out"); sp.set_defaults(func=render)
    sp = sub.add_parser("find"); sp.add_argument("ref"); sp.set_defaults(func=find)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
