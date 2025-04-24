"""Test colorbar."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    da = np.zeros((3, 3))
    da[:2, :2] = 1.0

    fig = plt.figure()
    ax = plt.gca()

    im = ax.imshow(da, cmap="viridis")
    plt.colorbar(im, aspect=5, shrink=0.5)
    return fig


def test() -> None:
    assert_equality(plot, "test_fancy_colorbar_reference.tex")
