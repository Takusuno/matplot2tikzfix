"""Helper functions for running the tests."""

from pathlib import Path
from typing import Callable

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import matplot2tikz


def print_tree(obj: Figure, indent: str = "") -> None:
    """Recursively prints the tree structure of the matplotlib object."""
    if isinstance(obj, mpl.text.Text):
        print(indent, type(obj).__name__, f'("{obj.get_text()}")')  # noqa: T201
    else:
        print(indent, type(obj).__name__)  # noqa: T201

    for child in obj.get_children():
        print_tree(child, indent + "  ")


# https://stackoverflow.com/a/845432/353337
def _unidiff_output(expected: str, actual: str) -> str:
    import difflib

    expected = expected.splitlines(1)
    actual = actual.splitlines(1)
    diff = difflib.unified_diff(expected, actual)
    return "".join(diff)


def assert_equality(
    plot: Callable,
    filename: str,
    flavor: str = "latex",
    **extra_get_tikz_code_args,  # noqa: ANN003
) -> None:
    plot()
    code = matplot2tikz.get_tikz_code(
        include_disclaimer=False,
        float_format=".8g",
        flavor=flavor,
        **extra_get_tikz_code_args,
    )
    plt.close("all")

    this_dir = Path(__file__).resolve().parent
    with (this_dir / filename).open(encoding="utf-8") as f:
        reference = f.read()
    assert reference == code, filename + "\n" + _unidiff_output(reference, code)
