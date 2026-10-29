"""Remix, Twilight Theme's CSS reset, written from the tokens.

    python remix/build.py            write the three files below
    python remix/build.py --check    exit 1 if any of them differs from what this script writes

Remix does what a CSS reset does and nothing more (docs/construction/remix.md): it makes browsers
agree, removes the defaults that vary between them, and sets the base every element starts from. That
base follows the design system, so far its typography. It styles elements and attributes only: no
classes, no components, no layout, no spacing between elements, no colors.

- remix/remix.css            the whole reset, in no layer, readable.
- remix/remix.min.css        the same, minified, for use.
- remix/remix-tailwind.css   for Tailwind CSS 4: in `@layer base` after Preflight, only the rules whose
                             result differs from Preflight's, so a page looks the same with either file.

Each block below is marked `tailwind=True` when Preflight does not already produce its result; those
blocks form the Tailwind file. tests/remix checks in Chromium that the two files give every element the
same computed style.

Names follow docs/design-system/typography.md §3: the prefix `twl`, a namespace, a key from the tokens.

Standard library only.
"""
import argparse
import json
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "typography" / "twilight.json"
OUT = {"vanilla": ROOT / "remix" / "remix.css", "min": ROOT / "remix" / "remix.min.css",
       "tailwind": ROOT / "remix" / "remix-tailwind.css"}
PROJECT = "https://github.com/iamdantz/twilight-theme"
PREFIX = "twl"
# Elements and the level they take (docs/design-system/typography.md §7)
LEVEL_OF = {**{f"h{i}": f"h{i}" for i in range(1, 7)}, "small, figcaption, caption": "body-sm"}
PLACEHOLDER_OPACITY = 0.54   # black at this opacity on white is 4.5:1 (docs/construction/remix.md §4)


def n(v):
    """A number without trailing zeros, at most four decimals."""
    return f"{v:.4f}".rstrip("0").rstrip(".")


def var(namespace, key=None):
    return f"--{PREFIX}-{namespace}" + (f"-{key}" if key and key != "default" else "")


def use(namespace, key=None):
    return f"var({var(namespace, key)})"


def rule(selector, decls):
    return f"{selector} {{\n" + "".join(f"  {k}: {v};\n" for k, v in decls) + "}"


def rules(*items):
    return "\n\n".join(rule(s, d) for s, d in items)


# Tokens ----------------------------------------------------------------------------------------
def faces(T):
    out = []
    for font in T["fonts"].values():
        for name, F in font["fallbacks"].items():
            for key, names in F["faces"].items():
                weight, style = key.split()
                out.append(rule("@font-face", [("font-family", f'"Twilight {name}"'),
                                               ("src", ", ".join(f'local("{x}")' for x in names)),
                                               ("font-weight", weight), ("font-style", style),
                                               ("size-adjust", f"{round(F['size-adjust'] * 100)}%")]))
    return "\n\n".join(out)


def stack(T, key, generic):
    F = T["fonts"][key]
    return ", ".join(f'"{x}"' for x in [F["family"], F["original"]] + [f"Twilight {x}" for x in F["fallbacks"]]) + f", {generic}"


def fit(T):
    F = T["fit"]
    return (F["narrowest"] - 2 * F["gutter"]) / F["em"], f"calc((100vw - {n(2 * F['gutter'] / 16)}rem) / {F['em']})"


def level_size(T, level):
    """A level's size: its step, bounded by `fit` where the step can be wider than the narrowest screen."""
    step = T["levels"][level]["size"]
    bound, _ = fit(T)
    widest = max(T["geometries"][g]["scale"][step] for g in ("desktop", "handheld"))
    return f"min({use('text', step)}, {use('text', 'fit')})" if widest > bound else use("text", step)


def scale(T, geometry, unit):
    S = T["geometries"][geometry]["scale"]
    value = (lambda v: f"{n(v / 16)}rem") if unit == "rem" else (lambda v: f"{n(v)}pt")
    return [(var("text", k), value(v)) for k, v in S.items()]


def tokens(T):
    root = [(var("font", "sans"), stack(T, "sans", "sans-serif")), (var("font", "mono"), stack(T, "mono", "monospace")),
            *scale(T, "desktop", "rem"), (var("text", "fit"), fit(T)[1]),
            *((var("text", level), level_size(T, level)) for level in T["levels"]),
            *((var("leading", k), n(v)) for k, v in T["leading"].items()),
            (var("spacing"), f"calc({use('text', 'base')} * {use('leading')})"),
            (var("container", "prose"), f"{n(T['container']['prose']['em'])}em")]
    media = lambda query, decls: f"@media {query} {{\n{textwrap.indent(rule(':root', decls), '  ')}\n}}"  # noqa: E731
    return "\n\n".join([rule(":root", root),
                        "/* Handheld screens: a coarse primary pointer. */\n" + media("(pointer: coarse)", scale(T, "handheld", "rem")),
                        "/* Pages: printed. */\n" + media("print", scale(T, "page", "pt"))])


# Blocks: (title, tailwind, css). tailwind=True: Preflight does not already give this result. ------
def blocks(T):
    L = T["levels"]
    bold = L["h1"]["weight"]
    controls = "button,\ninput,\nselect,\noptgroup,\ntextarea,\n::file-selector-button"
    return [
        ("Fallback fonts: the system fonts closest to Twilight Crystal, sized to its x-height", True, faces(T)),
        ("Tokens: fonts, the scale of the current geometry, levels, leading, spacing, the prose container", True,
         tokens(T)),

        ("Every element: sizes include padding and border, no outer spacing, borders ready to draw", False, rules(
            ("*,\n::before,\n::after,\n::backdrop,\n::file-selector-button",
             [("box-sizing", "border-box"), ("margin", "0"), ("padding", "0"), ("border", "0 solid")]))),

        ("Document: the same text size after rotation on iOS, tabs of four, no tap flash", False, rules(
            ("html,\n:host", [("-webkit-text-size-adjust", "100%"), ("tab-size", "4"),
                              ("-webkit-tap-highlight-color", "transparent")]))),
        ("Document: Twilight's font, leading and tracking; body text at the level body", True, rules(
            ("html,\n:host", [("font-family", use("font", "sans")), ("line-height", use("leading")),
                              ("letter-spacing", T["tracking"])]),
            ("body", [("font-size", use("text", "body"))]))),

        ("Headings and text levels", True, "\n\n".join(
            [rule(sel.replace(", ", ",\n"), [("font-size", use("text", lv))]) for sel, lv in LEVEL_OF.items()]
            + [rule("h1,\nh2,\nh3,\nh4,\nh5,\nh6", [("font-weight", bold), ("line-height", use("leading", L["h1"]["leading"]))]),
               rule("b,\nstrong", [("font-weight", bold)])])),

        ("Grouping: a rule one pixel thick in the text color; lists without markers", False, rules(
            ("hr", [("height", "0"), ("color", "inherit"), ("border-block-start-width", "1px")]),
            ("ol,\nul,\nmenu", [("list-style", "none")]))),

        ("Text: links take the text around them; abbreviations are marked; sub and sup keep the line", False, rules(
            ("a", [("color", "inherit"), ("-webkit-text-decoration", "inherit"), ("text-decoration", "inherit")]),
            ("abbr:where([title])", [("-webkit-text-decoration", "underline dotted"), ("text-decoration", "underline dotted")]),
            ("sub,\nsup", [("font-size", "75%"), ("line-height", "0"), ("position", "relative"), ("vertical-align", "baseline")]),
            ("sub", [("bottom", "-0.25em")]),
            ("sup", [("top", "-0.5em")]))),

        ("Literal text: Twilight Crystal Mono at the size of the text around it, without ligatures", True, rules(
            ("code,\nkbd,\nsamp,\npre", [("font-family", use("font", L["code"]["font"])), ("font-size", "1em"),
                                       ("font-variant-ligatures", "none")]),
            ("pre", [("line-height", use("leading", L["code"]["leading"])), ("overflow", "auto")]))),

        ("Embedded content: block boxes that never overflow their container", False, rules(
            ("img,\nsvg,\nvideo,\ncanvas,\naudio,\niframe,\nembed,\nobject", [("display", "block"), ("vertical-align", "middle")]),
            ("img,\nvideo", [("max-width", "100%"), ("height", "auto")]))),

        ("Tables: collapsed borders that take the table's color, no inherited indent", False, rules(
            ("table", [("text-indent", "0"), ("border-color", "inherit"), ("border-collapse", "collapse")]))),
        ("Figures: tabular in tables, times and outputs", True, rules(
            ("table,\ntime,\noutput", [("font-variant-numeric", "tabular-nums")]))),

        ("Forms: controls take the text around them and start without a surface", False, rules(
            (controls, [("font", "inherit"), ("font-feature-settings", "inherit"), ("font-variation-settings", "inherit"),
                        ("letter-spacing", "inherit"), ("color", "inherit"), ("border-radius", "0"),
                        ("background-color", "transparent"), ("opacity", "1")]),
            (":where(select:is([multiple], [size])) optgroup", [("font-weight", "bolder")]),
            (":where(select:is([multiple], [size])) optgroup option", [("padding-inline-start", "20px")]),
            ("::file-selector-button", [("margin-inline-end", "4px")]),
            ("textarea", [("resize", "vertical")]),
            ("button,\ninput:where([type='button'], [type='reset'], [type='submit']),\n::file-selector-button",
             [("appearance", "button")]),
            ("::-webkit-inner-spin-button,\n::-webkit-outer-spin-button", [("height", "auto")]),
            ("::-webkit-search-decoration", [("-webkit-appearance", "none")]),
            ("::-webkit-date-and-time-value", [("min-height", "1lh"), ("text-align", "inherit")]),
            ("::-webkit-datetime-edit", [("display", "inline-flex")]),
            ("::-webkit-datetime-edit-fields-wrapper", [("padding", "0")]),
            ("::-webkit-datetime-edit,\n::-webkit-datetime-edit-year-field,\n::-webkit-datetime-edit-month-field,\n"
             "::-webkit-datetime-edit-day-field,\n::-webkit-datetime-edit-hour-field,\n::-webkit-datetime-edit-minute-field,\n"
             "::-webkit-datetime-edit-second-field,\n::-webkit-datetime-edit-millisecond-field,\n::-webkit-datetime-edit-meridiem-field",
             [("padding-block", "0")]),
            ("::-webkit-calendar-picker-indicator", [("line-height", "1")]),
            (":-moz-ui-invalid", [("box-shadow", "none")]))),
        ("Forms: one-line controls at the leading of UI text; readable placeholders; plain search fields; "
         "fieldsets that shrink", True, rules(
            ("button,\ninput,\nselect,\n::file-selector-button", [("line-height", use("leading", L["ui"]["leading"]))]),
            ("::placeholder", [("color", "inherit"), ("opacity", n(PLACEHOLDER_OPACITY))]),
            ("[type='search']", [("-webkit-appearance", "textfield"), ("appearance", "textfield"), ("outline-offset", "-2px")]),
            ("fieldset", [("min-width", "0")]))),

        ("Interactive: the disclosure marker everywhere; focus rings in Firefox as in other browsers", False, rules(
            ("summary", [("display", "list-item")]),
            ("progress", [("vertical-align", "baseline")]),
            (":-moz-focusring:where(:not(iframe))", [("outline", "auto")]))),

        ("Hidden: the hidden attribute hides, whatever the element's display", False, rules(
            ("[hidden]:where(:not([hidden='until-found']))", [("display", "none !important")]))),
    ]


def section(title, css):
    return f"/* {title}. */\n\n{css}"


def header(T, extra=""):
    return (f"/*! Remix {T['version']}, Twilight Theme's CSS reset | MIT License | {PROJECT}\n"
            f"    Generated from typography/twilight.json by remix/build.py; do not edit.{extra} */")


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
    B = blocks(T)
    vanilla = header(T) + "\n\n" + "\n\n".join(section(t, c) for t, _, c in B) + "\n"
    tw = "\n\n".join(section(t, c) for t, keep, c in B if keep)
    tailwind = (header(T, "\n    For Tailwind CSS 4: import it after tailwindcss. Preflight gives the rest of Remix's result.")
                + "\n\n@layer base {\n" + textwrap.indent(tw, "  ", lambda line: line.strip() != "") + "\n}\n")
    return {"vanilla": vanilla, "min": minify(vanilla), "tailwind": tailwind}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    files = build()
    if a.check:
        bad = [str(OUT[k].relative_to(ROOT)) for k, v in files.items() if not OUT[k].exists() or OUT[k].read_text() != v]
        print("\n".join(f"{b} differs from remix/build.py" for b in bad) or "Remix matches the tokens")
        sys.exit(1 if bad else 0)
    for k, v in files.items():
        OUT[k].write_text(v)
    print("wrote", ", ".join(str(OUT[k].relative_to(ROOT)) for k in files))


if __name__ == "__main__":
    main()
