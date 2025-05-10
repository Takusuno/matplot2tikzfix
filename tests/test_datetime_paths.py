"""Test plot with datetimes."""

import datetime as date

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import dates
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()

    times = np.array(
        [
            date.datetime(2020, 1, 1, 12, 0, 0, tzinfo=date.timezone.utc),
            date.datetime(2020, 1, 2, 12, 0, 0, tzinfo=date.timezone.utc),
        ]
    )
    line = [2, 2]
    upper = [3, 4]
    lower = [1, 0]

    plt.plot(times, line)
    plt.fill_between(times, lower, upper)
    ax = plt.gca()
    ax.fmt_xdata = dates.DateFormatter("%d %b %Y %H:%M:%S")

    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
