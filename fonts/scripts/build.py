"""Build Twilight Text and Twilight Code from the pinned upstream sources.

Each upstream design source is copied, renamed and given the derivative's metadata (family
name, copyright line, manufacturer, description, version); the outlines, spacing, kerning and
features are untouched. The copies are compiled with gftools builder, with the upstream
build configuration, into fonts/build/<file>/fonts/: variable TTF, static TTF and WOFF2.

    python fonts/scripts/build.py              build both families
    python fonts/scripts/build.py --only TwilightCode
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

import glyphsLib
import yaml
from glyphsLib.classes import GSFontInfoValue

sys.path.insert(0, str(Path(__file__).resolve().parent))
import upstream  # noqa: E402

ROOT = upstream.ROOT
BUILD = ROOT / "fonts" / "build"
PROJECT = "https://github.com/iamdantz/twilight"
HOLDER = "José D. Gutiérrez"
YEAR = 2026


def metadata(family):
    up = family["upstream"]
    return {
        "copyright": f"{{original}} Copyright {YEAR} {HOLDER} ({PROJECT}).",
        "manufacturer": "Twilight",
        "manufacturerURL": PROJECT,
        # name ID 10, kept under the 200 characters applications expect
        "description": f"Derived from {up['family']} {up['version']}, designed by {{designers}}. "
                       f"Part of Twilight.",
    }


def prop(font, key, value=None):
    """Read or set a Glyphs 3 font-info property (name table source), adding it when absent."""
    entry = next((p for p in font.properties if p.key == key), None)
    localized = getattr(entry, "_localized_values", None)
    if value is None:
        return (localized.get("dflt", "") if localized else entry.value) if entry else ""
    if localized:
        entry._localized_values = {"dflt": value}
    elif entry:
        entry.value = value
    else:
        font.properties.append(GSFontInfoValue(key, value))


def rename(src, dst, family):
    font = glyphsLib.GSFont(str(src))
    meta = metadata(family)
    font.familyName = family["family"]
    prop(font, "copyrights", meta["copyright"].format(original=prop(font, "copyrights").rstrip(".") + "."))
    prop(font, "manufacturers", meta["manufacturer"])
    prop(font, "manufacturerURL", meta["manufacturerURL"])
    prop(font, "descriptions", meta["description"].format(designers=prop(font, "designers")))
    major, minor = family["version"].split(".")
    font.versionMajor, font.versionMinor = int(major), int(minor)
    font.save(str(dst))


def configure(family, sources_dir, names):
    config = yaml.safe_load((ROOT / family["directory"] / "sources" / "config.yaml").read_text(encoding="utf-8"))
    old, new = family["upstream"]["file"], family["file"]
    config["sources"] = names
    config["familyName"] = family["family"]
    config["stat"] = {key.replace(old, new): value for key, value in config.get("stat", {}).items()}
    config["buildOTF"] = False
    (sources_dir / "config.yaml").write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8")


def build(family):
    out = BUILD / family["file"]
    shutil.rmtree(out, ignore_errors=True)
    sources_dir = out / "sources"
    sources_dir.mkdir(parents=True)
    old, new = family["upstream"]["file"], family["file"]
    names = []
    for src in sorted((ROOT / family["directory"] / "sources").glob("*.glyphs")):
        name = src.name.replace(old, new)
        rename(src, sources_dir / name, family)
        names.append(name)
    configure(family, sources_dir, names)
    env = dict(os.environ, PATH=str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", ""))
    subprocess.run([str(Path(sys.executable).parent / "gftools"), "builder", "config.yaml"],
                   cwd=sources_dir, env=env, check=True)
    fonts = sorted((out / "fonts").rglob("*.*"))
    print(f"{family['family']}: {len(fonts)} files in {(out / 'fonts').relative_to(ROOT)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", help="build one family, by file name (TwilightText or TwilightCode)")
    args = parser.parse_args()
    if not upstream.verify():
        sys.exit("the upstream files changed; run upstream.py verify for details")
    for family in upstream.load()["families"]:
        if args.only in (None, family["file"]):
            build(family)
