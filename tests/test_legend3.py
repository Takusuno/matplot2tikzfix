"""Test legend with 3 entries."""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot(111)
    ax.fill_between([1, 2], [2, 2], [3, 3], color="red", alpha=0.2, label="roh")
    ax.fill_between([1, 2], [4, 4], [5, 5], color="blue", alpha=0.2, label="kal")
    ax.plot([1, 2], [2, 5], "k", label="ref")
    ax.grid()
    plt.legend()
    return fig


def test() -> None:
    try:
        assert_equality(plot, __file__[:-3] + "_reference.tex")
    except AssertionError:
        # Try other output, which is the new output since Python 3.9.
        # With Python 3.9 and above, legend will be at center right (which makes more sense).
        assert_equality(plot, __file__[:-3] + "_reference2.tex")
