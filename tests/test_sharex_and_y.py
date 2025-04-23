"""Test with plot that share x and y axes."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(8, 5))
    t = np.arange(0.0, 5.0, 0.1)
    s = np.cos(2 * np.pi * t)
    axes[0][0].plot(t, s, color="blue")
    axes[0][1].plot(t, s, color="red")
    axes[1][0].plot(t, s, color="green")
    axes[1][1].plot(t, s, color="black")
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
