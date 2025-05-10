"""Test plotting of pandas dataframe."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


def plot() -> Figure:
    fig = plt.figure(1, figsize=(8, 5))
    df_test = pd.DataFrame(index=["one", "two", "three"], data={"data": [1, 2, 3]})
    plt.plot(df_test, "o")
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")


if __name__ == "__main__":
    plot()
    plt.show()
