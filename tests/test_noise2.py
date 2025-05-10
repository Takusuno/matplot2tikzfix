"""Test plot with image and horizontal colorbar."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    # Make plot with horizontal colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)

    rng = np.random.default_rng(123)
    data = np.clip(rng.normal(size=(250, 250)), -1, 1)

    cax = ax.imshow(data, interpolation="nearest")
    ax.set_title("Gaussian noise with horizontal colorbar")

    cbar = fig.colorbar(cax, ticks=[-1, 0, 1], orientation="horizontal")
    # horizontal colorbar
    # Use comma in label
    cbar.ax.set_xticklabels(["Low", "Medium", "High,Higher"])
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
