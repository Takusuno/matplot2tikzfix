"""Test loglog plot."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()
    x = np.logspace(0, 6, num=5)
    plt.loglog(x, x**2, lw=2.1)
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
