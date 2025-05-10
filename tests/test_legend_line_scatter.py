"""Test legend with scatter plot."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()
    t = np.arange(5)
    x = t
    plt.plot(t, x, label="line")
    plt.scatter(t, x, label="scatter")
    plt.legend()
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
