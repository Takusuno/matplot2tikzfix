"""Test subplots that have colorbars."""

import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    data = np.zeros((3, 3))
    data[:2, :2] = 1.0

    fig = plt.figure()

    ax1 = plt.subplot(131)
    ax2 = plt.subplot(132)
    ax3 = plt.subplot(133)
    axes = [ax1, ax2, ax3]

    for ax in axes:
        im = ax.imshow(data)
        fig.colorbar(im, ax=ax, orientation="horizontal")

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
