"""Test plot with line data set using set_data().

From <https://github.com/nschloe/tikzplotlib/issues/339>
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()
    line = plt.plot(0, 0, "kx")[0]
    line.set_data([0], [0])
    return fig


def test() -> None:
    assert_equality(plot, "test_line_set_data_reference.tex")
