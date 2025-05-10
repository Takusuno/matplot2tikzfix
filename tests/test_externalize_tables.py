"""Test colorbar."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()
    with plt.style.context("ggplot"):
        t = np.arange(0.0, 2.0, 0.1)
        s = np.sin(2 * np.pi * t)
        s2 = np.cos(2 * np.pi * t)
        axes = plt.get_cmap("jet")(np.linspace(0, 1, 10))
        plt.plot(t, s, "o-", lw=1.5, color=axes[5])
        plt.plot(t, s2, "o-", lw=3, alpha=0.3)
        plt.xlabel("time(s)")
        plt.ylabel("Voltage (mV)")
        plt.title("Simple plot $\\frac{\\alpha}{2}$")
        plt.grid(visible=True)
    return fig


def test() -> None:
    assert_equality(plot, "test_externalize_tables_reference.tex", externalize_tables=True)
