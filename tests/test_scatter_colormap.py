"""Test scatter plot with colormap."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()
    rng = np.random.default_rng(123)
    plt.scatter(
        rng.normal(size=10),
        rng.normal(size=10),
        rng.random(size=10) * 90 + 10,
        rng.normal(size=10),
    )
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
