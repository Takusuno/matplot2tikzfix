"""Test escaping of some characters.

https://github.com/nschloe/tikzplotlib/issues/332
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure()
    plt.plot(0, 0, "kx")
    plt.title("Foo & Bar Dogs_N_Cats %")
    plt.xlabel("Foo & Bar Dogs_N_Cats %")
    plt.ylabel("Foo & Bar Dogs_N_Cats %")
    return fig


def test() -> None:
    assert_equality(plot, "test_escape_chars_reference.tex")
