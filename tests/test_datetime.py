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

    values = [50, 50.02]
    times = [
        date.datetime(2016, 10, 10, 18, 0, 0, tzinfo=date.timezone.utc),
        date.datetime(2016, 10, 10, 18, 15, 0, tzinfo=date.timezone.utc),
    ]
    plt.plot(np.array(times), values)
    hfmt = dates.DateFormatter("%H:%M")
    ax = plt.gca()
    ax.xaxis.set_major_formatter(hfmt)
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
