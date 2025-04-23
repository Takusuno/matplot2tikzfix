"""Test tick positioning."""

import itertools

import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    x = [1, 2, 3, 4]
    y = [1, 4, 9, 6]

    fig = plt.figure()
    for i, (bottom, top, left, right) in enumerate(itertools.product(["off", "on"], repeat=4)):
        plt.subplot(4, 4, i + 1)
        plt.plot(x, y, "ro")
        plt.tick_params(axis="x", which="both", bottom=bottom, top=top)
        plt.tick_params(axis="y", which="both", left=left, right=right)

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
