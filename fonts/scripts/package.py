"""Package the built fonts for a release.

For a version (the palette's, which must match the tag being released), writes into an output
directory:

- one archive per family, <File>-<version>.zip, holding <File>-<version>/ with the variable,
  static and web fonts as built (variable/, ttf/, webfonts/), OFL.txt and FONTLOG.txt: the
  SIL Open Font License requires the license and the copyright notices with every copy;
- SHA256SUMS.txt, the SHA-256 of each archive;
- notes.md, the version's section of CHANGELOG.md, as the release notes.

The Ligaturizer tool is not packaged: it is not needed to use the fonts.

    python fonts/scripts/package.py v1.20.0 dist/
"""
import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import upstream  # noqa: E402

ROOT = upstream.ROOT
BUILD = ROOT / "fonts" / "build"
FOLDERS = ("variable", "ttf", "webfonts")
NOTICES = (ROOT / "fonts" / "OFL.txt", ROOT / "fonts" / "FONTLOG.txt")
FIXED = (2026, 1, 1, 0, 0, 0)  # every entry gets one timestamp, so the same build zips the same bytes


def notes(version):
    """The CHANGELOG section of a version, without its heading."""
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(version)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        sys.exit(f"CHANGELOG.md has no section for {version}")
    return m.group(1).strip() + "\n"


def archive(family, version, out_dir):
    base = f"{family['file']}-{version}"
    fonts = BUILD / family["file"] / "fonts"
    files = [p for folder in FOLDERS for p in sorted((fonts / folder).glob("*")) if p.is_file()]
    if not files:
        sys.exit(f"{family['family']} is not built")
    path = out_dir / f"{base}.zip"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files + list(NOTICES):
            rel = p.relative_to(fonts) if p.is_relative_to(fonts) else Path(p.name)
            info = zipfile.ZipInfo(f"{base}/{rel.as_posix()}", FIXED)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, p.read_bytes())
    return path, len(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tag", help="the tag being released, v<version>")
    parser.add_argument("out", help="output directory")
    args = parser.parse_args()
    version = json.loads((ROOT / "palette" / "twilight.json").read_text(encoding="utf-8"))["version"]
    if args.tag != f"v{version}":
        sys.exit(f"tag {args.tag} does not match the palette's version {version}")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    sums = []
    for family in upstream.load()["families"]:
        path, count = archive(family, version, out_dir)
        sums.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
        print(f"{path.name}: {count} fonts, OFL.txt, FONTLOG.txt")
    (out_dir / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")
    (out_dir / "notes.md").write_text(notes(version), encoding="utf-8")
    print(f"release {args.tag} in {out_dir}")


if __name__ == "__main__":
    main()
