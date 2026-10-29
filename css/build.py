"""Twilight Theme's CSS reset, generated from the typography tokens.

    python css/build.py            write the three files below
    python css/build.py --check    exit 1 if any of them differs from what this script writes

Inputs: typography/twilight.json (the tokens) and css/upstream/tailwindcss/preflight.css (Tailwind CSS
Preflight, pinned with its SHA-256 in css/upstream.json). Outputs:

- css/twilight-tailwind.css   for Tailwind CSS 4: Twilight's typography in `@layer base`, after Preflight.
- css/twilight.css            for anything else: Preflight and Twilight's typography, in no layer.
- css/twilight.min.css        the same, minified.

Both carry the same typography; the vanilla files add Preflight, so a page without Tailwind starts from the
same base a Tailwind page does. Only element selectors are styled globally; document flow (spacing between
blocks, list markers, link underlines, quotes, table rules, line length, lead) applies inside `.document`
only. Every rule has at most the specificity of one element selector, so any class (a component's, a
utility's) overrides it. Nothing here sets a color.

Standard library only.
"""
import argparse
import hashlib
import json
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "typography" / "twilight.json"
UPSTREAM = ROOT / "css" / "upstream.json"
PREFLIGHT = ROOT / "css" / "upstream" / "tailwindcss" / "preflight.css"
OUT = {"tailwind": ROOT / "css" / "twilight-tailwind.css", "vanilla": ROOT / "css" / "twilight.css",
       "min": ROOT / "css" / "twilight.min.css"}
PROJECT = "https://github.com/iamdantz/twilight-theme"
HEADINGS = {f"h{i}": f"heading-{i}" for i in range(1, 7)}
STEP_VAR = {k: f"--twilight-step-{'n' + k[1:] if k.startswith('-') else k}" for k in map(str, range(-2, 8))}


def n(v):
    """A number without trailing zeros, at most four decimals."""
    return f"{v:.4f}".rstrip("0").rstrip(".")


def family(name):
    return f'"{name}"'


# Pieces ----------------------------------------------------------------------------------------
def fallback_faces(T):
    out = []
    for group in T["fallbacks"].values():
        for name, F in group.items():
            for key, names in F["faces"].items():
                weight, style = key.split()
                src = ", ".join(f'local("{x}")' for x in names)
                out.append(f'@font-face {{\n  font-family: "Twilight {name}";\n  src: {src};\n'
                           f"  font-weight: {weight};\n  font-style: {style};\n"
                           f"  size-adjust: {round(F['size adjust'] * 100)}%;\n}}")
    return "\n\n".join(out)


def stack(T, role, generic):
    names = [T["families"][role], T["originals"][role]] + [f"Twilight {x}" for x in T["fallbacks"][role]]
    return ", ".join(family(x) for x in names) + f", {generic}"


def fit(T):
    F = T["fit"]
    return (F["narrowest"] - 2 * F["gutter"]) / F["em"], f"calc((100vw - {n(2 * F['gutter'] / 16)}rem) / {F['em']})"


def level_value(T, level):
    """A level's size: its step, bounded by the column where the step can be wider than the narrowest screen."""
    step = str(T["levels"][level]["step"])
    bound, _ = fit(T)
    widest = max(T["geometries"][g]["steps"][step] for g in ("desktop", "handheld"))
    var = f"var({STEP_VAR[step]})"
    return f"min({var}, var(--twilight-fit))" if widest > bound else var


def steps(T, geometry, unit):
    S = T["geometries"][geometry]["steps"]
    if unit == "rem":
        return "\n".join(f"  {STEP_VAR[k]}: {n(S[k] / 16)}rem;" for k in STEP_VAR)
    return "\n".join(f"  {STEP_VAR[k]}: {n(S[k])}pt;" for k in STEP_VAR)


def tokens_css(T):
    L = T["levels"]
    _, fit_expr = fit(T)
    lines = [
        f"  --twilight-font-text: {stack(T, 'text', 'sans-serif')};",
        f"  --twilight-font-literal: {stack(T, 'literal', 'monospace')};",
        steps(T, "desktop", "rem"),
        f"  --twilight-fit: {fit_expr};",
    ]
    for level in L:
        if level == "code-block":
            continue
        lines.append(f"  --twilight-{level}: {level_value(T, level)};")
    C = T["code"]
    lines += [
        f"  --twilight-line: {n(T['line height']['running'])};",
        f"  --twilight-line-compact: {n(T['line height']['compact'])};",
        f"  --twilight-space: calc(var(--twilight-step-0) * var(--twilight-line));",
        f"  --twilight-measure: {n(T['measure']['em'])}em;",
        f"  --twilight-code: {n(C['minimum'] / 16)}rem;",
        f"  --twilight-code-optimal: {n(C['optimal'] / 16)}rem;",
    ]
    media = lambda query, body: f"@media {query} {{\n  :root {{\n{textwrap.indent(body, '  ')}\n  }}\n}}"  # noqa: E731
    return (":root {\n" + "\n".join(lines) + "\n}\n\n"
            "/* Handheld screens: a coarse primary pointer. */\n" + media("(pointer: coarse)", steps(T, "handheld", "rem"))
            + "\n\n/* Documents: printed pages. */\n" + media("print", steps(T, "documents", "pt")))


def global_css(T):
    L = T["levels"]
    head = "\n".join(f"{el} {{\n  font-size: var(--twilight-{lv});\n}}" for el, lv in HEADINGS.items())
    weight = L["heading-1"]["weight"]
    return f"""html {{
  font-family: var(--twilight-font-text);
  line-height: var(--twilight-line);
  letter-spacing: 0;
}}

body {{
  font-size: var(--twilight-running-text);
}}

{head}

h1,
h2,
h3,
h4,
h5,
h6 {{
  font-weight: {weight};
  line-height: var(--twilight-line-compact);
  text-wrap: balance;
}}

b,
strong {{
  font-weight: {weight};
}}

small,
figcaption,
caption {{
  font-size: var(--twilight-small);
}}

code,
kbd,
samp,
pre {{
  font-family: var(--twilight-font-literal);
  font-size: 1em;
  font-variant-ligatures: none;
}}

pre {{
  line-height: var(--twilight-line-compact);
}}

table,
time,
output {{
  font-variant-numeric: tabular-nums;
}}"""


def document_css(T):
    S = T["spacing"]
    space = lambda k: "var(--twilight-space)" if k == 1 else f"calc(var(--twilight-space) * {n(k)})"  # noqa: E731
    half, before, after = space(0.5), space(S["before-heading"]), space(S["after-heading"])
    hs = "h1, h2, h3, h4, h5, h6"
    return f""":where(.document) {{
  max-inline-size: var(--twilight-measure);
}}

:where(.document) > :where(* + *) {{
  margin-block-start: {space(S['paragraph'])};
}}

:where(.document) > :where({hs}):where(:not(:first-child)) {{
  margin-block-start: {before};
}}

:where(.document) > :where({hs}) + :where(*) {{
  margin-block-start: {after};
}}

:where(.document) > :where(p:first-of-type) {{
  font-size: var(--twilight-lead);
}}

:where(.document) :is(ul, ol) {{
  padding-inline-start: 1.5em;
}}

:where(.document) ul {{
  list-style: disc;
}}

:where(.document) ol {{
  list-style: decimal;
}}

:where(.document) li > * + *,
:where(.document) :is(ul, ol):has(> li > p + p) > li + li {{
  margin-block-start: {half};
}}

:where(.document) a {{
  text-decoration-line: underline;
}}

:where(.document) blockquote {{
  padding-inline-start: 1.5em;
  border-inline-start-width: 3px;
}}

:where(.document) :is(th, td) {{
  padding-inline-end: 1em;
  border-block-end-width: 1px;
  text-align: start;
  vertical-align: top;
}}

:where(.document) figcaption {{
  margin-block-start: {half};
}}

:where(.document) pre {{
  overflow-x: auto;
}}"""


def twilight(T):
    return "\n\n".join([
        "/* Fallback faces: the system fonts closest to Twilight Crystal, sized to its x-height. */",
        fallback_faces(T),
        "/* Tokens: the scale of the geometry, levels, line heights, spacing and line length. */",
        tokens_css(T),
        "/* Every text: families, levels, literal text and figures. */",
        global_css(T),
        "/* Document text: flow inside .document only, never above the specificity of one element. */",
        document_css(T),
    ])


def preflight():
    pin = json.loads(UPSTREAM.read_text())["tailwindcss"]
    data = PREFLIGHT.read_bytes()
    if hashlib.sha256(data).hexdigest() != pin["files"]["preflight.css"]:
        sys.exit("css/upstream/tailwindcss/preflight.css does not match its SHA-256 in css/upstream.json")
    text = data.decode()
    # --theme(--name, fallback) is Tailwind's; without Tailwind, the fallback is the value.
    text = re.sub(r"--theme\(\s*--[\w-]+,\s*(.*?)\s*\)(?=;)", lambda m: re.sub(r"\s*\n\s*", " ", m.group(1)), text, flags=re.S)
    return pin["version"], text.strip()


def header(T, extra=""):
    return (f"/*! Twilight Theme typography reset {T['version']} | MIT License | {PROJECT}\n"
            f"    Generated from typography/twilight.json by css/build.py; do not edit.{extra} */")


def minify(css):
    keep = re.match(r"/\*!.*?\*/", css, re.S).group(0)
    body = re.sub(r"/\*.*?\*/", "", css[len(keep):], flags=re.S)
    body = re.sub(r"\s+", " ", body)
    body = re.sub(r"\s*([{};,])\s*", r"\1", body)
    body = re.sub(r":\s+", ":", body)
    body = body.replace(";}", "}")
    return keep + "\n" + body.strip() + "\n"


def build():
    T = json.loads(TOKENS.read_text())
    version, pre = preflight()
    tw = twilight(T)
    tailwind = (header(T, "\n    For Tailwind CSS 4: import it after tailwindcss.") + "\n\n@layer base {\n"
                + "\n".join(("  " + line) if line else "" for line in tw.split("\n")) + "\n}\n")
    vanilla = (header(T, f"\n    Includes Tailwind CSS Preflight {version}, MIT License, Copyright (c) Tailwind Labs, Inc.")
               + "\n\n/* Tailwind CSS Preflight */\n\n" + pre + "\n\n/* Twilight Theme */\n\n" + tw + "\n")
    return {"tailwind": tailwind, "vanilla": vanilla, "min": minify(vanilla)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    files = build()
    if a.check:
        bad = [str(OUT[k].relative_to(ROOT)) for k, v in files.items() if not OUT[k].exists() or OUT[k].read_text() != v]
        print("\n".join(f"{b} differs from css/build.py" for b in bad) or "CSS matches the typography tokens")
        sys.exit(1 if bad else 0)
    for k, v in files.items():
        OUT[k].write_text(v)
    print("wrote", ", ".join(str(OUT[k].relative_to(ROOT)) for k in files))


if __name__ == "__main__":
    main()
