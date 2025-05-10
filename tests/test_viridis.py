"""Test _quadmesh.py."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

mpl.use("Agg")


def plot() -> Figure:
    x, y = np.meshgrid(np.linspace(0, 1), np.linspace(0, 1))
    z = x**2 - y**2

    fig = plt.figure()
    plt.pcolormesh(x, y, z, cmap=plt.get_cmap("viridis"), shading="gouraud")

    return fig


def test() -> None:
    from .helpers import assert_equality

    # test relative data path
    assert_equality(
        plot,
        __file__[:-3] + "_reference.tex",
    )
