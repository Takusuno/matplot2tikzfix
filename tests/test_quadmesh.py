"""Test quad mesh."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    x = np.linspace(0 * np.pi, 2 * np.pi, 128)
    y = np.linspace(0 * np.pi, 2 * np.pi, 128)
    X, Y = np.meshgrid(x, y)
    nu = 1e-5

    def force(t: float):
        return np.exp(-2 * nu * t)

    def u(x: float, y: float, t: float):
        return np.sin(x) * np.cos(y) * force(t)

    def v(x: float, y: float, t: float):
        return -np.cos(x) * np.sin(y) * force(t)

    fig, axs = plt.subplots(2, figsize=(8, 12))
    axs[0].pcolormesh(X, Y, u(X, Y, 0), shading="gouraud")
    axs[1].pcolormesh(X, Y, v(X, Y, 0), shading="gouraud")
    for ax in axs:
        ax.set_xlim(x[0], x[-1])
        ax.set_ylim(y[0], y[-1])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    axs[0].set_title("Taylor--Green Vortex")

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
