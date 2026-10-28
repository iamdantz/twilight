# Ligaturizer: Fira Code's programming ligatures for other monospaced fonts.
#
# Copyright (C) the Ligaturizer contributors (https://github.com/ToxicFrog/Ligaturizer)
# Copyright (C) 2026 José D. Gutiérrez
#
# This program is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License (LICENSE) for more details.
#
# Modified in 2026 from Ligaturizer's ligatures.py: instead of a list of Fira Code ligature
# glyphs to copy, the default selection of Fira Code 6's contextual lookups.
"""Which of Fira Code's calt lookups a font receives by default.

Fira Code 6 keeps its ligatures and its arbitrary-length sequences (arrows, rows of # and _)
in lookups of its calt feature, and in the same feature some contextual forms of single
characters drawn for Fira Code itself. Those are left out by default, as Ligaturizer leaves out
Fira Code's traditional letter ligatures, because they replace the receiving font's own design
of a character rather than join characters:
"""
EXCLUDED = {
    "hexadecimal_x": "x drawn as a multiplication sign between digits (0xFF, 1920x1080)",
    "lowercase_hyphen": "hyphen lowered between lowercase letters",
    "lowercase_plus": "plus lowered between lowercase letters",
    "lowercase_asterisk": "asterisk lowered between lowercase letters",
    "lowercase_asteriskmath": "math asterisk lowered between lowercase letters",
    "uppercase_colon": "colon raised next to capitals and digits",
    "caltGreekUC": "Greek capital forms",
    "caltGreekUCdiph": "Greek capital diphthong forms",
    "w_w_w": "the only ligature of letters (www), in Fira Code's w",
}
