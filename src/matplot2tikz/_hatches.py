r"""Map matplotlib hatches to tikz patterns.

For matplotlib hatches, see:
https://matplotlib.org/3.1.1/gallery/shapes_and_collections/hatch_demo.html

For patterns in tikzpgf:
Ch 26 Pattern Lbrary in the manual
Requires \usetikzlibrary{patterns}
"""

# These methods exist, and might be relevant (in the future?):
# matplotlib.backend_bases.GraphicsContextBase.set/get_hatch_color
# matplotlib.backend_bases.GraphicsContextBase.set/get_hatch_linewidth
# hatch_density is mentioned in mpl API Changes in 2.0.1

import warnings
from typing import Dict, List

import numpy as np

BAD_MP_HATCH = ["o", "O"]  # Bad hatch/pattern correspondence
UNUSED_PGF_PATTERN = ["dots"]
_MP_HATCH2PGF_PATTERN = {
    "-": "horizontal lines",
    "|": "vertical lines",
    "/": "north east lines",
    "\\": "north west lines",
    "+": "grid",
    "x": "crosshatch",
    ".": "crosshatch dots",
    "*": "fivepointed stars",
    "o": "sixpointed stars",
    "O": "bricks",
}


def __validate_hatch(hatch: str) -> str:
    """Warn about the shortcomings of patterns."""
    if len(hatch) > 1:
        warnings.warn(
            f"matplot2tikz: Hatch '{hatch}' cannot be rendered. "
            "Only single character hatches are supported, e.g., "
            r"{'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}. "
            f"Hatch '{hatch[0]}' will be used.",
            stacklevel=2,
        )
        hatch = hatch[0]

    if hatch in BAD_MP_HATCH:
        warnings.warn(
            f"matplot2tikz: The hatches {BAD_MP_HATCH} do not have good PGF counterparts.",
            stacklevel=2,
        )
    return hatch


def _mpl_hatch2pgfp_pattern(
    data: Dict, hatch: str, color_name: str, color_rgba: np.ndarray
) -> List[str]:
    r"""Translates a hatch from matplotlib to the corresponding pattern in PGFPlots.

    Input:
        hatch - str, like {'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}
        color_name - str, xcolor or custom color name
        color_rgba - np.ndarray, the rgba value of the color
    Output:
        draw_options - list, empty or with a post action string
    """
    hatch = __validate_hatch(hatch)
    try:
        pgfplots_pattern = _MP_HATCH2PGF_PATTERN[hatch]
    except KeyError:
        warnings.warn(f"matplot2tikz: The hatch {hatch} is ignored.", stacklevel=2)
        return []

    data["tikz libs"].add("patterns")

    pattern_options = [f"pattern={pgfplots_pattern}"]
    if color_name != "black":
        # PGFPlots render patterns in 'pattern color' (default: black)
        pattern_options += [f"pattern color={color_name}"]
    if color_rgba[3] != 1:
        ff = data["float format"]
        # PGFPlots render patterns according to opacity fill.
        # This change is within the scope of the postaction
        pattern_options.append(f"fill opacity={color_rgba[3]:{ff}}")

    # Add pattern as postaction to allow color fill and pattern together
    # https://tex.stackexchange.com/questions/24964/
    # how-to-combine-fill-and-pattern-in-a-pgfplot-bar-plot
    postaction = f"postaction={{{', '.join(pattern_options)}}}"

    return [postaction]
