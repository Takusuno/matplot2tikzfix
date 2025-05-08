"""Test heatmap."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()
    x = np.array([np.linspace(-10, 10, 100)]).T
    y = np.array([np.linspace(-10, 10, 100)])
    extent = (x.min(), x.max(), y.min(), y.max())
    cmap = mpl.colormaps.get_cmap("gray")
    plt.imshow(x * y, extent=extent, cmap=cmap)
    plt.colorbar()
    return fig


def test() -> None:
    assert_equality(plot, "test_heat_reference.tex")
