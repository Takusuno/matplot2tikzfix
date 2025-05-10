"""Test semilogy plot with base 2."""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    a = [pow(10, i) for i in range(10)]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.semilogy(a, color="blue", lw=0.25, base=2)

    plt.grid(visible=True, which="major", color="g", linestyle="-", linewidth=0.25)
    plt.grid(visible=True, which="minor", color="r", linestyle="--", linewidth=0.5)
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
