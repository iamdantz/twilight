"""The upstream fonts Twilight Text and Twilight Code derive from.

fonts/upstream.json pins each upstream repository to one commit. The design sources and the
license files of that commit are copied into fonts/upstream/<repository>/ and recorded with
their SHA-256. The upstream's own compiled variable fonts are not stored: they are fetched at
the same commit when a build is compared against them, and verified by SHA-256.

The "ligatures" entry pins the Fira Code files Twilight Code's optional ligatures come from
(fonts/upstream/firacode/): the variable font of a release, its license, and the rules and glyph
class written from that release's design source by tools/ligaturizer (ligaturize.py extract).
verify checks them too; vendor leaves them alone.

    python fonts/scripts/upstream.py vendor            copy the pinned files and record hashes
    python fonts/scripts/upstream.py verify            check the copied files against their hashes
    python fonts/scripts/upstream.py reference DIR     fetch and verify the upstream binaries into DIR
"""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "fonts" / "upstream.json"
VENDORED = ["OFL.txt", "AUTHORS.txt", "CONTRIBUTORS.txt", "sources/config.yaml",
            "sources/{file}.glyphs", "sources/{file}-Italic.glyphs"]
REFERENCE = ["fonts/variable/{file}[wght].ttf", "fonts/variable/{file}-Italic[wght].ttf"]


def load():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def save(manifest):
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def fetch(repository, commit, paths):
    """The bytes of each path at one commit, fetched without cloning the history."""
    with tempfile.TemporaryDirectory() as tmp:
        git = ["git", "-C", tmp]
        subprocess.run(["git", "init", "-q", tmp], check=True)
        subprocess.run(git + ["fetch", "-q", "--depth", "1", repository, commit], check=True)
        return {p: subprocess.run(git + ["show", f"FETCH_HEAD:{p}"], check=True, capture_output=True).stdout
                for p in paths}


def paths(template, family):
    return [t.format(file=family["upstream"]["file"]) for t in template]


def vendor():
    manifest = load()
    for family in manifest["families"]:
        up = family["upstream"]
        files = fetch(up["repository"], up["commit"], paths(VENDORED, family))
        refs = fetch(up["repository"], up["commit"], paths(REFERENCE, family))
        target = ROOT / family["directory"]
        for rel, data in files.items():
            out = target / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
        family["vendored"] = {rel: sha256(data) for rel, data in sorted(files.items())}
        family["reference"] = {rel: sha256(data) for rel, data in sorted(refs.items())}
        print(f"{family['family']}: {len(files)} files from {up['repository']} at {up['commit'][:12]}")
    save(manifest)


def verify():
    bad = []
    manifest = load()
    for family in manifest["families"] + [manifest["ligatures"]]:
        for rel, digest in family["vendored"].items():
            path = ROOT / family["directory"] / rel
            if not path.exists():
                bad.append(f"missing {path.relative_to(ROOT)}")
            elif sha256(path.read_bytes()) != digest:
                bad.append(f"changed {path.relative_to(ROOT)}")
    for line in bad:
        print(line)
    print("upstream files: " + ("FAIL" if bad else "ok"))
    return not bad


def reference(out_dir):
    out_dir = Path(out_dir)
    for family in load()["families"]:
        up = family["upstream"]
        files = fetch(up["repository"], up["commit"], list(family["reference"]))
        for rel, data in files.items():
            if sha256(data) != family["reference"][rel]:
                sys.exit(f"reference {rel} of {up['family']} does not match its recorded SHA-256")
            out = out_dir / family["file"] / Path(rel).name
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
    print(f"reference fonts in {out_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("vendor")
    sub.add_parser("verify")
    sub.add_parser("reference").add_argument("dir")
    args = parser.parse_args()
    if args.command == "vendor":
        vendor()
    elif args.command == "verify":
        sys.exit(0 if verify() else 1)
    else:
        reference(args.dir)
