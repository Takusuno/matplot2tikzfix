"""Custom collection test.

This tests plots a subclass of Collection, which contains enough information
as a base class to be rendered.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import RendererBase
from matplotlib.collections import Collection
from matplotlib.figure import Figure
from matplotlib.path import Path
from matplotlib.transforms import Affine2D, IdentityTransform

from .helpers import assert_equality

mpl.use("Agg")


class TransformedEllipseCollection(Collection):
    """A gutted version of matplotlib.collections.EllipseCollection.

    This one lets us pass the transformation matrix directly.
    This is useful for plotting cholesky factors of covariance matrices.
    """

    def __init__(self, matrices: np.ndarray, **kwargs) -> None:  # type: ignore[no-untyped-def]  # noqa: ANN003
        """Initialize TransformedEllipseCollection."""
        super().__init__(**kwargs)
        self.set_transform(IdentityTransform())
        self._transforms = np.zeros(matrices.shape[:-2] + (3, 3))
        self._transforms[..., :2, :2] = matrices
        self._transforms[..., 2, 2] = 1
        self._paths = [Path.unit_circle()]

    def _set_transforms(self) -> None:
        """Calculate transforms immediately before drawing."""
        if self.axes is None:
            msg = "Axes not set."
            raise ValueError(msg)
        m = self.axes.transData.get_affine().get_matrix().copy()
        m[:2, 2:] = 0
        self.set_transform(Affine2D(m))

    @mpl.artist.allow_rasterization
    def draw(self, renderer: RendererBase) -> None:
        """Draw ellipse."""
        self._set_transforms()
        super().draw(renderer)


def rot(theta: np.ndarray) -> np.ndarray:
    """Get a stack of rotation matrices."""
    return np.stack(
        [
            np.stack([np.cos(theta), -np.sin(theta)], axis=-1),
            np.stack([np.sin(theta), np.cos(theta)], axis=-1),
        ],
        axis=-2,
    )


def plot() -> Figure:
    fig = plt.figure()
    ax = fig.add_subplot(111)

    theta = np.linspace(0, 2 * np.pi, 6, endpoint=False)
    mats = rot(theta) @ np.diag([0.1, 0.2])
    x = np.cos(theta)
    y = np.sin(theta)

    c = TransformedEllipseCollection(
        mats,
        offsets=np.stack((x, y), axis=-1),
        edgecolor="tab:red",
        alpha=0.5,
        facecolor="tab:blue",
        transOffset=ax.transData,
    )
    ax.add_collection(c)
    ax.set(xlim=[-1.5, 1.5], ylim=[-1.5, 1.5])

    return fig


def test() -> None:
    assert_equality(plot, "test_custom_collection_reference.tex")
