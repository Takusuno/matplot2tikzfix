"""Test histogram with axv line."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()
    rng = np.random.default_rng(123)
    s = rng.normal(0, 1, size=10)
    plt.gca().set_ylim(-1.0, +1.0)
    plt.hist(s, 30)
    plt.axvline(1.96)
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
