"""Font Bakery on the built Twilight fonts, against the upstream fonts they derive from.

Each built variable font and its upstream counterpart are checked with the Google Fonts
profile, each alone in a scratch directory, so checks that read catalog files fail the same
way on both. A check that fails on the built font and not on the upstream one is a new
failure, and fails this script. Errors (checks that could not run, usually for lack of network)
are reported and not counted.

    python fonts/scripts/upstream.py reference /tmp/reference
    python fonts/scripts/bakery.py /tmp/reference
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "fonts" / "build"
MANIFEST = ROOT / "fonts" / "upstream.json"


def run(font):
    """Check id -> result for one font checked alone."""
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / font.name
        shutil.copy(font, copy)
        report = Path(tmp) / "report.json"
        bakery = Path(sys.executable).parent / "fontbakery"
        subprocess.run([str(bakery), "check-googlefonts", "--json", str(report), str(copy)],
                       capture_output=True, text=True)
        data = json.loads(report.read_text(encoding="utf-8"))
    results = {}
    for section in data["sections"]:
        for check in section["checks"]:
            key = re.search(r"Check:([^>]+)", str(check.get("key", check))).group(1)
            worst = results.get(key)
            order = ["PASS", "SKIP", "INFO", "WARN", "ERROR", "FAIL", "FATAL"]
            if worst is None or order.index(check["result"]) > order.index(worst):
                results[key] = check["result"]
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("reference", help="directory written by upstream.py reference")
    args = parser.parse_args()
    failed = False
    for family in json.loads(MANIFEST.read_text(encoding="utf-8"))["families"]:
        old, new = family["upstream"]["file"], family["file"]
        refs = sorted((Path(args.reference) / new).glob("*.ttf"))
        if not refs:
            print(f"FAIL {family['family']}: no reference fonts in {Path(args.reference) / new}")
            failed = True
        for ref in refs:
            ours = BUILD / new / "fonts" / "variable" / ref.name.replace(old, new)
            a, b = run(ours), run(ref)
            new_fails = sorted(k for k, v in a.items() if v in ("FAIL", "FATAL") and b.get(k) not in ("FAIL", "FATAL"))
            fixed = sorted(k for k, v in b.items() if v in ("FAIL", "FATAL") and a.get(k) not in ("FAIL", "FATAL"))
            count = lambda r: Counter(v for v in r.values())
            ca, cb = count(a), count(b)
            status = "FAIL" if new_fails else "ok"
            print(f"{status:4} {ours.name}: {ca['FAIL']} fail, {ca['WARN']} warn, {ca['ERROR']} error "
                  f"(upstream {cb['FAIL']} fail, {cb['WARN']} warn, {cb['ERROR']} error)")
            for key in new_fails:
                print(f"     new failure: {key}")
            for key in fixed:
                print(f"     no longer failing: {key}")
            for key in sorted(k for k, v in a.items() if v == "WARN" and b.get(k) != "WARN"):
                print(f"     new warning (not blocking): {key}")
            failed |= bool(new_fails)
    print("Font Bakery against upstream: " + ("FAIL" if failed else "ok"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
