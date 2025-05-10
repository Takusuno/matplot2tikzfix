"""Test rotation of ticks."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> None:
    labels = ["lab1", "label 2", "another super label"]
    n = len(labels)
    x = np.arange(n)
    y = 1 / (x + 1)

    ax = plt.gca()
    ax.bar(x, y, 0.5)

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    plt.xticks(rotation=45, ha="right")


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
