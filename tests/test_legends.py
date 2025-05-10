"""Test legend."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()

    x = np.ma.arange(0, 2 * np.pi, 0.4)
    y = np.ma.sin(x)
    y1 = np.sin(2 * x)
    y2 = np.sin(3 * x)
    limit = 0.5
    ym1 = np.ma.masked_where(y1 > limit, y1)
    ym2 = np.ma.masked_where(y2 < -limit, y2)

    lines = plt.plot(x, y, "r", x, ym1, "g", x, ym2, "bo")
    plt.setp(lines[0], linewidth=4)
    plt.setp(lines[1], linewidth=2)
    plt.setp(lines[2], markersize=10)

    plt.legend(("No mask", "Masked if > 0.5", "Masked if < -0.5"), loc="upper right")
    plt.title("Masked line demo")
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
