"""Test rotation of ticks."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    # Make plot with vertical (default) colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)

    rng = np.random.default_rng(123)
    ax.hist(10 + 2 * rng.normal(size=1000), label="men")
    ax.hist(12 + 3 * rng.normal(size=1000), label="women", alpha=0.5)
    ax.legend()
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
