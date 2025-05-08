"""Test scatter plot with different colors."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()
    rng = np.random.default_rng(123)
    n = 4
    plt.scatter(
        rng.random(n),
        rng.random(n),
        color=np.array(
            [
                [1.0, 0.6, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [0.0, 1.0, 1.0],
            ]
        ),
        edgecolors=[
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (0.0, 1.0, 1.0),
            (1.0, 0.0, 0.0),
        ],
    )
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
