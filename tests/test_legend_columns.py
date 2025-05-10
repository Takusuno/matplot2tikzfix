"""Test legend with labels horizontally."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig, ax = plt.subplots(figsize=(17, 6))
    ax.plot(np.array([1, 5]), label="Test 1")
    ax.plot(np.array([5, 1]), label="Test 2")
    ax.legend(ncol=2, loc="upper center")
    return fig


def test() -> None:
    assert_equality(plot, "test_legend_columns_reference.tex")
