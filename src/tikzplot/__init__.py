"""Script to convert Matplotlib generated figures into TikZ/PGFPlots figures."""

from .__about__ import __version__
from ._cleanfigure import clean_figure
from ._save import Flavors, get_tikz_code, save

__all__ = [
    "Flavors",
    "__version__",
    "clean_figure",
    "get_tikz_code",
    "save",
]
