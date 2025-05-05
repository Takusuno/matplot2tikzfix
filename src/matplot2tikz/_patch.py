from typing import Sequence

from matplotlib.collections import Collection
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Patch, Rectangle
from matplotlib.transforms import Affine2D

from . import _path as mypath
from ._text import _get_arrow_style


def draw_patch(data: dict, obj: Patch) -> str:
    """Return the PGFPlots code for patches."""
    if isinstance(obj, FancyArrowPatch):
        draw_options = mypath.get_draw_options(
            data,
            mypath.LineData(
                obj=obj,
                ec=obj.get_edgecolor(),
                fc=None,  # get_fillcolor for the arrow refers to the head, not the path
                ls=obj.get_linestyle(),
                lw=obj.get_linewidth(),
                hatch=obj.get_hatch(),
            ),
        )
        return _draw_fancy_arrow(data, obj, draw_options)

    # Gather the draw options.
    draw_options = mypath.get_draw_options(
        data,
        mypath.LineData(
            obj=obj,
            ec=obj.get_edgecolor(),
            fc=obj.get_facecolor(),
            ls=obj.get_linestyle(),
            lw=obj.get_linewidth(),
            hatch=obj.get_hatch(),
        ),
    )

    if isinstance(obj, Rectangle):
        # rectangle specialization
        return _draw_rectangle(data, obj, draw_options)
    if isinstance(obj, Ellipse):
        # ellipse specialization
        return _draw_ellipse(data, obj, draw_options)
    # regular patch
    return _draw_polygon(data, obj, draw_options)


def _is_in_legend(obj: Collection) -> bool:
    label = obj.get_label()
    leg = obj.axes.get_legend()
    if leg is None:
        return False
    return label in [txt.get_text() for txt in leg.get_texts()]


def _patch_legend(obj: Collection, draw_options: list, legend_type: str) -> str:
    """Decorator for handling legend of mpl.Patch."""
    legend = ""
    if _is_in_legend(obj):
        # Unfortunately, patch legend entries need \addlegendimage in Pgfplots.
        do = ", ".join([legend_type, *draw_options]) if draw_options else ""
        label = obj.get_label()
        legend += f"\\addlegendimage{{{do}}}\n\\addlegendentry{{{label}}}\n\n"

    return legend


def zip_modulo(*seqs: Sequence) -> tuple:
    n = max(len(seq) for seq in seqs)
    for i in range(n):
        yield tuple((seq[i % len(seq)] if len(seq) != 0 else None) for seq in seqs)


def draw_patchcollection(data: dict, obj: Collection) -> str:
    """Returns PGFPlots code for a number of patch objects."""
    content = []

    # recompute the face colors
    obj.update_scalarmappable()

    def ensure_list(x: Sequence) -> Sequence:
        return [None] if len(x) == 0 else x

    ecs = ensure_list(obj.get_edgecolor())
    fcs = ensure_list(obj.get_facecolor())
    lss = ensure_list(obj.get_linestyle())
    ws = ensure_list(obj.get_linewidth())
    ts = ensure_list(obj.get_transforms())
    offs = obj.get_offsets()

    paths = obj.get_paths()
    for path, ec, fc, ls, w, t, off in zip_modulo(paths, ecs, fcs, lss, ws, ts, offs):
        draw_options = mypath.get_draw_options(
            data, mypath.LineData(obj=obj, ec=ec, fc=fc, ls=ls, lw=w)
        )
        cont, draw_options, is_area = mypath.draw_path(
            data,
            path.transformed(Affine2D(t).translate(*off)) if t is not None else path,
            draw_options=draw_options,
        )
        content.append(cont)

    legend_type = "area legend" if is_area else "line legend"
    legend = _patch_legend(obj, draw_options, legend_type) or "\n"
    content.append(legend)

    return content


def _draw_polygon(data: dict, obj: Patch, draw_options: list) -> str:
    content, _, is_area = mypath.draw_path(data, obj.get_path(), draw_options=draw_options)
    legend_type = "area legend" if is_area else "line legend"
    content += _patch_legend(obj, draw_options, legend_type)

    return content


def _draw_rectangle(data: dict, obj: Rectangle, draw_options: list) -> str:
    """Return the PGFPlots code for rectangles."""
    # Objects with labels are plot objects (from bar charts, etc).  Even those without
    # labels explicitly set have a label of "_nolegend_".  Everything else should be
    # skipped because they likely correspong to axis/legend objects which are handled by
    # PGFPlots
    label = obj.get_label()
    if label == "":
        return []

    # Get actual label, bar charts by default only give rectangles labels of
    # "_nolegend_". See <https://stackoverflow.com/q/35881290/353337>.
    handles, labels = obj.axes.get_legend_handles_labels()
    labels_found = [label for h, label in zip(handles, labels) if obj in h.get_children()]
    if len(labels_found) == 1:
        label = labels_found[0]

    left_lower_x = obj.get_x()
    left_lower_y = obj.get_y()
    ff = data["float format"]
    do = ",".join(draw_options)
    right_upper_x = left_lower_x + obj.get_width()
    right_upper_y = left_lower_y + obj.get_height()
    cont = (
        f"\\draw[{do}] (axis cs:{left_lower_x:{ff}},{left_lower_y:{ff}}) "
        f"rectangle (axis cs:{right_upper_x:{ff}},{right_upper_y:{ff}});\n"
    )

    if label != "_nolegend_" and label not in data["rectangle_legends"]:
        data["rectangle_legends"].add(label)
        draw_opts = ",".join(draw_options)
        cont += f"\\addlegendimage{{ybar,ybar legend,{draw_opts}}}\n"
        cont += f"\\addlegendentry{{{label}}}\n\n"
    return cont


def _draw_ellipse(data: dict, obj: Ellipse, draw_options: list) -> str:
    """Return the PGFPlots code for ellipses."""
    if isinstance(obj, Circle):
        # circle specialization
        return _draw_circle(data, obj, draw_options)
    x, y = obj.center
    ff = data["float format"]

    if obj.angle != 0:
        draw_options.append(f"rotate around={{{obj.angle:{ff}}:(axis cs:{x:{ff}},{y:{ff}})}}")

    do = ",".join(draw_options)
    content = (
        f"\\draw[{do}] (axis cs:{x:{ff}},{y:{ff}}) ellipse "
        f"({0.5 * obj.width:{ff}} and {0.5 * obj.height:{ff}});\n"
    )
    content += _patch_legend(obj, draw_options, "area legend")

    return content


def _draw_circle(data: dict, obj: Circle, draw_options: list) -> str:
    """Return the PGFPlots code for circles."""
    x, y = obj.center
    ff = data["float format"]
    do = ",".join(draw_options)
    content = f"\\draw[{do}] (axis cs:{x:{ff}},{y:{ff}}) circle ({obj.get_radius():{ff}});\n"
    content += _patch_legend(obj, draw_options, "area legend")
    return content


def _draw_fancy_arrow(data: dict, obj: FancyArrowPatch, draw_options: list) -> str:
    style = _get_arrow_style(obj, data)
    ff = data["float format"]
    if obj._posA_posB is not None:  # noqa: SLF001  (no known method to obtain posA and posB)
        pos_a, pos_b = obj._posA_posB  # noqa: SLF001
        do = ",".join(style)
        content = (
            f"\\draw[{do}] (axis cs:{pos_a[0]:{ff}},{pos_a[1]:{ff}}) -- "
            f"(axis cs:{pos_b[0]:{ff}},{pos_b[1]:{ff}});\n"
        )
    else:
        content, _, _ = mypath.draw_path(
            data,
            obj._path_original,  # noqa: SLF001  (no known method to obtain posA and posB)
            draw_options=draw_options + style,
        )
    content += _patch_legend(obj, draw_options, "line legend")
    return content
