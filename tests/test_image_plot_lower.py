"""Test plot with an image."""

import pathlib

import matplotlib as mpl
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


# the picture 'lena.png' with origin='lower' is flipped upside-down.
# So it has to be upside-down in the pdf-file as well.


def plot() -> Figure:
    this_dir = pathlib.Path(__file__).resolve().parent
    img = mpimg.imread(this_dir / "lena.png")

    dpi = rcParams["figure.dpi"]
    figsize = img.shape[0] / dpi, img.shape[1] / dpi
    fig = plt.figure(figsize=figsize)
    ax = plt.axes((0, 0, 1, 1), frameon=False)
    ax.set_axis_off()
    plt.imshow(img, cmap="viridis", origin="lower")
    plt.colorbar()
    return fig


def test() -> None:
    assert_equality(plot, __file__[:-3] + "_reference.tex")
