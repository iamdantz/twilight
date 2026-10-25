"""Syntax roles (construction.md §8) from the corpus statistics in syntax/stats.json. No corpus, no tree-sitter.

Five roles follow the ANSI convention; the study resolves the one choice the convention leaves open: of parameter
and property, which takes Ember and which stays uncolored. The one with the larger mean screen share stays uncolored,
so the least code is colored. The distinctness ranking of every assignment is reported in §8 for transparency.
"""
import itertools
import json
from collections import Counter
from pathlib import Path

STATS = Path(__file__).resolve().parent / "syntax" / "stats.json"
CONVENTION = {"keyword": "orchid", "string": "grove", "function": "sky", "type": "sea-salt", "constant": "gold"}
FREE = ("parameter", "property")
LANGS = ("python", "javascript", "typescript")


def aggregate(stats, drop=(), weights=None):
    """Per language, the mean over packages of each category's share of characters and of each adjacent pair's share;
    every package weighs 1 (or `weights[package]`)."""
    out = {}
    for lang in LANGS:
        pk = [(p, d[lang]) for p, d in stats.items() if lang in d and p not in drop and sum(d[lang]["chars"].values())]
        share, adj, total = Counter(), Counter(), 0
        for p, d in pk:
            w = (weights or {}).get(p, 1)
            chars, pairs = sum(d["chars"].values()), sum(d["adjacent"].values()) or 1
            for c, v in d["chars"].items():
                share[c] += w * v / chars
            for c, v in d["adjacent"].items():
                adj[c] += w * v / pairs
            total += w
        if total:
            out[lang] = {"share": {c: v / total for c, v in share.items()}, "adjacent": {k: v / total for k, v in adj.items()}}
    return out


def mean_share(agg, cat):
    return sum(agg[l]["share"].get(cat, 0) for l in agg) / len(agg)


def uncolored(stats=None):
    """The free category with the larger mean screen share across the languages."""
    agg = aggregate(stats or json.loads(STATS.read_text()))
    return max(FREE, key=lambda c: mean_share(agg, c))


def assignment(stats=None):
    u = uncolored(stats)
    return {**CONVENTION, u: "body", next(c for c in FREE if c != u): "ember"}


def ranking(palette, stats=None):
    """Every assignment of the six code colors and Body to the seven categories, ranked by distinctness alone: in each
    scenario (language × flavor × vision), the adjacency-weighted mean ΔE OKLab between the inks of neighboring
    categories (variables are Body); an assignment's score is its worst ratio to the best score of each scenario.
    Returns [(score, assignment)], best first."""
    import construct as k
    agg = aggregate(stats or json.loads(STATS.read_text()))
    cats = ("keyword", "string", "function", "type", "constant", "parameter", "property")
    inks = ("orchid", "grove", "sky", "sea-salt", "gold", "ember", "body")
    hexes = {f: {i: (F["neutrals"]["body"] if i == "body" else F["colors"][i]) for i in inks} for f, F in palette.items()}
    de = {(f, v, a, b): k.de_ok(k.sim(hexes[f][a], v), k.sim(hexes[f][b], v)) if v else k.de_ok(hexes[f][a], hexes[f][b])
          for f in palette for v in k.VISIONS for a in inks for b in inks}
    scen = [(l, f, v) for l in agg for f in palette for v in k.VISIONS]

    def scores(assign):
        ink = dict(assign, variable="body")
        out = []
        for l, f, v in scen:
            pairs = [(w, *key.split("|")) for key, w in agg[l]["adjacent"].items()]
            pairs = [(w, a, b) for w, a, b in pairs if a in ink and b in ink]
            out.append(sum(w * de[f, v, ink[a], ink[b]] for w, a, b in pairs) / sum(w for w, _, _ in pairs))
        return out

    every = [dict(zip(cats, p)) for p in itertools.permutations(inks)]
    table = [scores(a) for a in every]
    best = [max(col) for col in zip(*table)]
    ranked = [(min(s / b for s, b in zip(row, best)), a) for row, a in zip(table, every)]
    return sorted(ranked, key=lambda x: -x[0])


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    palette = json.loads((Path(__file__).resolve().parents[4] / "palette" / "twilight.json").read_text())["flavors"]
    r = ranking(palette)
    cur = assignment()
    pos = next(i for i, (_, a) in enumerate(r) if a == cur)
    print(f"best {r[0][0]:.4f} {r[0][1]}\npublished assignment: rank {pos + 1} of {len(r)}, score {r[pos][0]:.4f}")
