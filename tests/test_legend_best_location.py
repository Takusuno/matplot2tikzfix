"""Test different locations of legend based on 'best location'."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig, ax = plt.subplots(3, 3, sharex="col", sharey="row")
    axes = [ax[i][j] for i in range(len(ax)) for j in range(len(ax[i]))]
    t = np.arange(0.0, 2.0 * np.pi, 0.4)

    # Legend best location is "upper left"
    line = axes[0].plot(t, np.cos(t) * np.exp(0.15 * t), linewidth=0.5)[0]
    axes[0].legend((line,), ("UL",), loc=0)

    # Legend best location is "upper center"
    line = axes[1].plot(t, 3 * np.cos(t), linewidth=0.5)[0]
    axes[1].legend((line,), ("UC",), loc=0)

    # Legend best location is "upper right"
    line = axes[2].plot(t, np.cos(t) * np.exp(-t), linewidth=0.5)[0]
    axes[2].legend((line,), ("UR",), loc=0)

    # Legend best location is "center left"
    line = axes[3].plot(t[10:], 2 * np.cos(10 * t[10:]), linewidth=0.5)[0]
    axes[3].plot(t, -1.5 * np.ones_like(t), t, 1.5 * np.ones_like(t))
    axes[3].legend((line,), ("CL",), loc=0)

    # Legend best location is "center"
    line = axes[4].plot(t[:4], 2 * np.cos(10 * t[:4]), linewidth=0.5)[0]
    axes[4].plot(t[-4:], 2 * np.cos(10 * t[-4:]), linewidth=0.5)
    axes[4].plot(t, -2 + 0.5 * np.cos(10 * t), t, 2 + 0.5 * np.cos(10 * t))
    axes[4].legend((line,), ("C",), loc=0)

    # Legend best location is "center right"
    line = axes[5].plot(t[:-10], 2 * np.cos(10 * t[:-10]), linewidth=0.5)[0]
    axes[5].plot(t, -1.5 * np.ones_like(t), t, 1.5 * np.ones_like(t))
    axes[5].legend((line,), ("CR",), loc=0)

    # Legend best location is "lower left"
    line = axes[6].plot(t, np.cos(5.0 * t) + 1, linewidth=0.5)[0]
    axes[6].legend((line,), ("LL",), loc=0)

    # Legend best location is "lower center"
    (line,) = axes[7].plot(t, -3 * np.cos(t) * np.exp(-0.1 * t), linewidth=0.5)
    axes[7].legend((line,), ("LC",), loc=0)

    # Legend best location is "lower right"
    line = axes[8].plot(t, 3 * np.cos(6 * t) * np.exp(-0.5 * t) + 0.5 * t - 0.5, linewidth=0.5)[0]
    axes[8].legend((line,), ("LR",), loc=0)

    return fig


def test() -> None:
    assert_equality(plot, "test_legend_best_location_reference.tex")
