"""Test scatter plot."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()
    with plt.style.context("fivethirtyeight"):
        rng = np.random.default_rng(123)
        plt.scatter(
            np.linspace(0, 100, 101),
            np.linspace(0, 100, 101) + 15 * rng.random(size=101),
        )
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
