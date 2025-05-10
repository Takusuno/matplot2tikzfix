"""Test fill_between."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig, ax = plt.subplots()
    with plt.style.context("ggplot"):
        t = np.linspace(0, 2 * np.pi, 11)
        s = np.sin(t)
        ax.plot(t, s, "k-")
        ax.fill_between(t, s + 0.1, s - 0.1, facecolor="k", alpha=0.2)
        ax.set_xlim(t[0], t[-1])
        ax.set_xlabel("t")
        ax.set_ylabel("sin(t)")
        ax.set_title("Simple plot")
        ax.grid(visible=True)
    return fig


def test() -> None:
    assert_equality(plot, "test_errorband_reference.tex")
