"""Test different line types."""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()
    linestyles = ["-", "--", "-.", ":", (0, (10, 1)), (5, (10, 1)), (0, (1, 2, 3, 4))]
    for idx, ls in enumerate(linestyles):
        plt.plot([idx, idx + 1], linestyle=ls)
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
