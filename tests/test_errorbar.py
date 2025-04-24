"""Test errorbar."""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    # plot data
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x = [7.14, 7.36, 7.47, 7.52]
    y = [3.3, 4.4, 8.8, 5.5]
    ystd = [0.1, 0.5, 0.8, 0.3]

    ax.errorbar(x, y, yerr=ystd)
    return fig


def test() -> None:
    assert_equality(plot, "test_errorbar_reference.tex")
