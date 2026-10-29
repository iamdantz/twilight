"""Twilight Theme's CSS reset, generated from the tokens.

    python css/build.py            write the three files below
    python css/build.py --check    exit 1 if any of them differs from what this script writes

Inputs: typography/twilight.json and css/upstream/tailwindcss/preflight.css (Tailwind CSS Preflight, pinned
with its SHA-256 in css/upstream.json). Outputs:

- css/twilight-tailwind.css   for Tailwind CSS 4: Twilight Theme's base in `@layer base`, after Preflight.
- css/twilight.css            for anything else: Preflight and Twilight Theme's base, in no layer.
- css/twilight.min.css        the same, minified.

The reset covers typography today. Only element selectors are styled globally; prose (spacing between
blocks, list markers, link underlines, quotes, table rules, line length, the opening paragraph) is styled
inside `.twl-prose` only. Every rule has at most the specificity of one element selector, so any class (a
component's, a utility's) overrides it. Nothing here sets a color.

Every name follows one scheme, the one of the tokens: the prefix `twl`, then a namespace (`font`, `text`,
`leading`, `spacing`, `container`), then a key from typography/twilight.json. `--twl-text-base` is a step of
the scale, `--twl-text-h1` a level, `--twl-leading-tight` a leading.

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
PREFIX = "twl"
PROSE = f".{PREFIX}-prose"
# Elements and the level they take
ELEMENTS = {"body": "body", **{f"h{i}": f"h{i}" for i in range(1, 7)}, "small, figcaption, caption": "body-sm"}


def n(v):
    """A number without trailing zeros, at most four decimals."""
    return f"{v:.4f}".rstrip("0").rstrip(".")


def var(namespace, key=None):
    return f"--{PREFIX}-{namespace}" + (f"-{key}" if key and key != "default" else "")


def use(namespace, key=None):
    return f"var({var(namespace, key)})"


# Pieces ----------------------------------------------------------------------------------------
def fallback_faces(T):
    out = []
    for font in T["fonts"].values():
        for name, F in font["fallbacks"].items():
            for key, names in F["faces"].items():
                weight, style = key.split()
                src = ", ".join(f'local("{x}")' for x in names)
                out.append(f'@font-face {{\n  font-family: "Twilight {name}";\n  src: {src};\n'
                           f"  font-weight: {weight};\n  font-style: {style};\n"
                           f"  size-adjust: {round(F['size-adjust'] * 100)}%;\n}}")
    return "\n\n".join(out)


def stack(T, key, generic):
    F = T["fonts"][key]
    names = [F["family"], F["original"]] + [f"Twilight {x}" for x in F["fallbacks"]]
    return ", ".join(f'"{x}"' for x in names) + f", {generic}"


def fit(T):
    F = T["fit"]
    return (F["narrowest"] - 2 * F["gutter"]) / F["em"], f"calc((100vw - {n(2 * F['gutter'] / 16)}rem) / {F['em']})"


def level_size(T, level):
    """A level's size: its step, bounded by the column where the step can be wider than the narrowest screen."""
    step = T["levels"][level]["size"]
    bound, _ = fit(T)
    widest = max(T["geometries"][g]["scale"][step] for g in ("desktop", "handheld"))
    return f"min({use('text', step)}, {use('text', 'fit')})" if widest > bound else use("text", step)


def scale(T, geometry, unit):
    S = T["geometries"][geometry]["scale"]
    value = (lambda v: f"{n(v / 16)}rem") if unit == "rem" else (lambda v: f"{n(v)}pt")
    return "\n".join(f"  {var('text', k)}: {value(v)};" for k, v in S.items())


def tokens_css(T):
    _, fit_expr = fit(T)
    lines = [
        f"  {var('font', 'sans')}: {stack(T, 'sans', 'sans-serif')};",
        f"  {var('font', 'mono')}: {stack(T, 'mono', 'monospace')};",
        scale(T, "desktop", "rem"),
        f"  {var('text', 'fit')}: {fit_expr};",
        *(f"  {var('text', level)}: {level_size(T, level)};" for level in T["levels"]),
        *(f"  {var('leading', k)}: {n(v)};" for k, v in T["leading"].items()),
        f"  {var('spacing')}: calc({use('text', 'base')} * {use('leading')});",
        f"  {var('container', 'prose')}: {n(T['container']['prose']['em'])}em;",
    ]
    media = lambda query, body: f"@media {query} {{\n  :root {{\n{textwrap.indent(body, '  ')}\n  }}\n}}"  # noqa: E731
    return (":root {\n" + "\n".join(lines) + "\n}\n\n"
            "/* Handheld screens: a coarse primary pointer. */\n" + media("(pointer: coarse)", scale(T, "handheld", "rem"))
            + "\n\n/* Pages: printed. */\n" + media("print", scale(T, "page", "pt")))


def rule(selector, decls):
    return f"{selector} {{\n" + "".join(f"  {k}: {v};\n" for k, v in decls) + "}"


def global_css(T):
    L = T["levels"]
    out = [rule("html", [("font-family", use("font", "sans")), ("line-height", use("leading")),
                         ("letter-spacing", T["tracking"])])]
    out += [rule(selector.replace(", ", ",\n"), [("font-size", use("text", level))]) for selector, level in ELEMENTS.items()]
    headings = [f"h{i}" for i in range(1, 7)]
    assert len({(L[h]["weight"], L[h]["leading"]) for h in headings}) == 1, "headings share weight and leading"
    out.append(rule(",\n".join(headings), [("font-weight", L["h1"]["weight"]), ("line-height", use("leading", L["h1"]["leading"])),
                                           ("text-wrap", "balance")]))
    out += [
        rule("b,\nstrong", [("font-weight", L["h1"]["weight"])]),
        rule("code,\nkbd,\nsamp,\npre", [("font-family", use("font", L["code"]["font"])), ("font-size", "1em"),
                                          ("font-variant-ligatures", "none")]),
        rule("pre", [("line-height", use("leading", L["code"]["leading"]))]),
        rule("table,\ntime,\noutput", [("font-variant-numeric", "tabular-nums")]),
    ]
    return "\n\n".join(out)


def prose_css(T):
    S = T["spacing"]
    space = lambda k: use("spacing") if k == 1 else f"calc({use('spacing')} * {n(k)})"  # noqa: E731
    w = f":where({PROSE})"
    hs = "h1, h2, h3, h4, h5, h6"
    return "\n\n".join([
        rule(w, [("max-inline-size", use("container", "prose"))]),
        rule(f"{w} > :where(* + *)", [("margin-block-start", space(S["block"]))]),
        rule(f"{w} > :where({hs}):where(:not(:first-child))", [("margin-block-start", space(S["before-heading"]))]),
        rule(f"{w} > :where({hs}) + :where(*)", [("margin-block-start", space(S["after-heading"]))]),
        rule(f"{w} > :where(p:first-of-type)", [("font-size", use("text", "body-lg"))]),
        rule(f"{w} :is(ul, ol)", [("padding-inline-start", "1.5em")]),
        rule(f"{w} ul", [("list-style", "disc")]),
        rule(f"{w} ol", [("list-style", "decimal")]),
        rule(f"{w} li > * + *,\n{w} :is(ul, ol):has(> li > p + p) > li + li",
             [("margin-block-start", space(S["list-item-with-paragraphs"]))]),
        rule(f"{w} a", [("text-decoration-line", "underline")]),
        rule(f"{w} blockquote", [("padding-inline-start", "1.5em"), ("border-inline-start-width", "3px")]),
        rule(f"{w} :is(th, td)", [("padding-inline-end", "1em"), ("border-block-end-width", "1px"),
                                  ("text-align", "start"), ("vertical-align", "top")]),
        rule(f"{w} figcaption", [("margin-block-start", space(S["after-heading"]))]),
        rule(f"{w} pre", [("overflow-x", "auto")]),
    ])


def twilight(T):
    return "\n\n".join([
        "/* Fallback faces: the system fonts closest to Twilight Crystal, sized to its x-height. */",
        fallback_faces(T),
        "/* Tokens: fonts, the scale of the geometry, levels, leading, spacing and the prose container. */",
        tokens_css(T),
        "/* Elements: fonts, levels, code and figures. */",
        global_css(T),
        f"/* Prose: flow inside {PROSE} only, never above the specificity of one element. */",
        prose_css(T),
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
    return (f"/*! Twilight Theme reset {T['version']} | MIT License | {PROJECT}\n"
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
