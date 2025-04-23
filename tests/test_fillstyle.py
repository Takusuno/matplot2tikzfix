"""Test fill style of markers."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()

    n = 10
    t = np.linspace(0, 1, n)
    x = np.arange(n)
    plt.plot(t, x, "-o", fillstyle="none")
    plt.tight_layout()
    return fig


def test() -> None:
    assert_equality(plot, "test_fillstyle_reference.tex")
