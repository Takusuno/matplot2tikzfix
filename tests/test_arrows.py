"""Test plot with fancy arrow."""

import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from .helpers import assert_equality

mpl.use("Agg")


# https://matplotlib.org/examples/pylab_examples/fancyarrow_demo.html
def plot() -> Figure:
    styles = mpatches.ArrowStyle.get_styles()

    ncol = 2
    nrow = (len(styles) + 1) // ncol
    figheight = nrow + 0.5
    fig1 = plt.figure(1, (4.0 * ncol / 1.5, figheight / 1.5))
    fontsize = 0.2 * 70

    ax = fig1.add_axes((0, 0, 1, 1), frameon=False, aspect=1.0)

    ax.set_xlim(0, 4 * ncol)
    ax.set_ylim(0, figheight)

    def to_texstring(s: str) -> str:
        s = s.replace("<", r"$<$")
        s = s.replace(">", r"$>$")
        return s.replace("|", r"$|$")

    for i, stylename in enumerate(sorted(styles)):
        x = 3.2 + (i // nrow) * 4
        y = figheight - 0.7 - i % nrow  # /figheight
        p = mpatches.Circle((x, y), 0.2)
        ax.add_patch(p)

        ax.annotate(
            to_texstring(stylename),
            (x, y),
            (x - 1.2, y),
            ha="right",
            va="center",
            size=fontsize,
            arrowprops={
                "arrowstyle": stylename,
                "patchB": p,
                "shrinkA": 5,
                "shrinkB": 5,
                "fc": "k",
                "ec": "k",
                "connectionstyle": "arc3,rad=-0.05",
            },
            bbox={"boxstyle": "square", "fc": "w"},
        )

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    return plt.gcf()


def test() -> None:
    assert_equality(plot, "test_arrows_reference.tex")
