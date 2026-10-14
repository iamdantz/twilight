"""Reproduce the measured parameter β (construction.md §6.2) for both flavors.

β is the slope of a theme's ANSI color lightness against the sRGB cusp lightness of the six anchor hues.
The ANSI colors below were read from each theme's published VS Code color theme (terminal.ansiRed …
terminal.ansiMagenta). Sources are listed so the data can be checked; the measurement itself needs only
these values.

Rule: β = mean slope over the themes whose correlation r reaches 0.6 (the lowest accepted for Dusk).

Usage: python measure_beta.py      (about 1 minute)
"""
import numpy as np
from coloraide import Color

ANCHOR_HUES = [29.2, 109.8, 142.5, 194.8, 264.1, 328.4]       # RGB cube corners in OKLCH (§6.1), red → magenta order below

# order: red, yellow, green, cyan, blue, magenta
DUSK = {  # the three themes of the original Dusk study (their published palettes)
    "Dracula": ["#ff5555", "#f1fa8c", "#50fa7b", "#8be9fd", "#bd93f9", "#ff79c6"],
    "Catppuccin Mocha": ["#f38ba8", "#f9e2af", "#a6e3a1", "#94e2d5", "#89b4fa", "#f5c2e7"],
    "One Dark": ["#e06c75", "#e5c07b", "#98c379", "#56b6c2", "#61afef", "#c678dd"],
}
DAWN = {  # light themes that define terminal colors (One Light and Light Modern define none)
    "Catppuccin Latte": ["#d20f39", "#df8e1d", "#40a02b", "#179299", "#1e66f5", "#ea76cb"],
    "GitHub Light Default": ["#cf222e", "#4d2d00", "#116329", "#1b7c83", "#0969da", "#8250df"],
    "Solarized Light": ["#dc322f", "#b58900", "#859900", "#2aa198", "#268bd2", "#d33682"],
    "Rosé Pine Dawn": ["#b4637a", "#ea9d34", "#286983", "#d7827e", "#56949f", "#907aa9"],
    "Material Theme Lighter": ["#e53935", "#e2931d", "#91b859", "#39adb5", "#6182b8", "#9c3eda"],
    "Tokyo Night Light": ["#8c4351", "#8f5e15", "#33635c", "#006c86", "#2959aa", "#7b43ba"],
    "Ayu Light": ["#f06b6c", "#e7a100", "#6cbf43", "#4abc96", "#21a1e2", "#a176cb"],
    "Night Owl Light": ["#de3d3b", "#e0af02", "#08916a", "#2aa298", "#288ed7", "#d6438a"],
}
SOURCES = {
    "Catppuccin Latte": "github.com/catppuccin/vscode, as bundled in shiki 1.29.2 (tm-themes)",
    "GitHub Light Default": "github.com/primer/github-vscode-theme, as bundled in shiki 1.29.2",
    "Solarized Light": "github.com/microsoft/vscode extensions/theme-solarized-light, as bundled in shiki 1.29.2",
    "Rosé Pine Dawn": "github.com/rose-pine/vscode, as bundled in shiki 1.29.2",
    "Material Theme Lighter": "github.com/material-theme/vsc-material-theme, as bundled in shiki 1.29.2",
    "Tokyo Night Light": "github.com/enkia/tokyo-night-vscode-theme themes/tokyo-night-light-color-theme.json",
    "Ayu Light": "github.com/ayu-theme/vscode-ayu ayu-light.json",
    "Night Owl Light": "github.com/sdras/night-owl-vscode-theme themes/Night Owl-Light-color-theme.json",
}


def cmax(L, h):
    lo, hi = 0.0, 0.5
    for _ in range(40):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if Color("oklch", [L, m, h]).in_gamut("srgb") else (lo, m)
    return lo


def true_cusp(h):
    """L of maximum in-gamut chroma on a 0.001 grid over 0.200–0.999 (the sRGB cusp, §6.1 column)."""
    return max(((i / 1000, cmax(i / 1000, h)) for i in range(200, 1000)), key=lambda t: t[1])[0]


def fit(cols, cu):
    L = np.array([Color(c).convert("oklch")["lightness"] for c in cols])
    return np.polyfit(cu - cu.mean(), L, 1)[0], np.corrcoef(cu, L)[0, 1]


def main():
    cu = np.array([true_cusp(h) for h in ANCHOR_HUES])
    for flavor, themes in (("Dusk", DUSK), ("Dawn", DAWN)):
        rows = {n: fit(c, cu) for n, c in themes.items()}
        kept = [b for b, r in rows.values() if r >= 0.6]
        print(f"{flavor}:")
        for n, (b, r) in sorted(rows.items(), key=lambda x: -x[1][1]):
            print(f"  {n:24} β {b:+.3f}  r {r:+.2f}  {'kept' if r >= 0.6 else 'excluded'}")
        print(f"  β = {np.mean(kept):.3f} (mean of {len(kept)}) → {round(np.mean(kept), 2)}")


if __name__ == "__main__":
    main()
