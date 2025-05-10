"""Test plot with image and horizontal colorbar."""

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
    data = np.clip(rng.normal(size=(250, 250)), -1, 1)

    cax = ax.imshow(data, interpolation="nearest")
    ax.set_title("Gaussian noise with vertical colorbar")

    # Add colorbar, make sure to specify tick locations to match desired ticklabels.
    cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
    # vertically oriented colorbar
    cbar.ax.set_yticklabels(["< -1", "0", "> 1"])
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
