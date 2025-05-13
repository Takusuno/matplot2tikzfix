from __future__ import annotations

import enum
import logging
import sys
import tempfile
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple, TypedDict

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.axis import XAxis, YAxis
from matplotlib.collections import Collection, LineCollection, PathCollection, QuadMesh
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.spines import Spine
from matplotlib.text import Text
from typing_extensions import NotRequired, Unpack

if TYPE_CHECKING:
    from matplotlib.artist import Artist

from . import _axes, _legend, _line2d, _patch, _path, _text
from . import _image as img
from . import _quadmesh as qmsh
from .__about__ import __version__

# Set logger to be used to print some info
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
if not LOGGER.handlers:
    HANDLER = logging.StreamHandler(sys.stdout)
    FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    HANDLER.setFormatter(FORMATTER)
    LOGGER.addHandler(HANDLER)


class TikzArgs(TypedDict):
    figure: NotRequired[str | Figure]
    axis_width: NotRequired[str | None]
    axis_height: NotRequired[str | None]
    textsize: NotRequired[float]
    tex_relative_path_to_data: NotRequired[str | None]
    externalize_tables: NotRequired[bool]
    override_externals: NotRequired[bool]
    externals_search_path: NotRequired[str | None]
    strict: NotRequired[bool]
    wrap: NotRequired[bool]
    add_axis_environment: NotRequired[bool]
    extra_axis_parameters: NotRequired[List | Set | None]
    extra_groupstyle_parameters: NotRequired[dict]
    extra_tikzpicture_parameters: NotRequired[list | Set | None]
    extra_lines_start: NotRequired[List | Set | None]
    dpi: NotRequired[int | None]
    show_info: NotRequired[bool]
    include_disclaimer: NotRequired[bool]
    standalone: NotRequired[bool]
    float_format: NotRequired[str]
    table_row_sep: NotRequired[str]
    flavor: NotRequired[str]


def get_tikz_code(  # noqa: PLR0913
    figure: str | Figure = "gcf",
    filepath: str | Path | None = None,
    axis_width: str | None = None,
    axis_height: str | None = None,
    textsize: float = 10.0,
    tex_relative_path_to_data: str | None = None,
    externalize_tables: bool = False,  # noqa: FBT001, FBT002
    override_externals: bool = False,  # noqa: FBT001, FBT002
    externals_search_path: str | None = None,
    strict: bool = False,  # noqa: FBT001, FBT002
    wrap: bool = True,  # noqa: FBT001, FBT002
    add_axis_environment: bool = True,  # noqa: FBT001, FBT002
    extra_axis_parameters: List | Set | None = None,
    extra_groupstyle_parameters: Optional[dict] = None,
    extra_tikzpicture_parameters: List | Set | None = None,
    extra_lines_start: List | Set | None = None,
    dpi: int | None = None,
    show_info: bool = False,  # noqa: FBT001, FBT002
    include_disclaimer: bool = True,  # noqa: FBT001, FBT002
    standalone: bool = False,  # noqa: FBT001, FBT002
    float_format: str = ".15g",
    table_row_sep: str = "\n",
    flavor: str = "latex",
) -> str:
    r"""Main function that converts a matplotlib Figure to tikz.

    :param figure: either a Figure object or 'gcf' (default).

    :param axis_width: If not ``None``, this will be used as figure width within the
                       TikZ/PGFPlots output. If ``axis_height`` is not given,
                       ``matplot2tikz`` will try to preserve the original width/height
                       ratio.  Note that ``axis_width`` can be a string literal, such as
                       ``'\\axis_width'``.
    :type axis_width: str

    :param axis_height: If not ``None``, this will be used as figure height within the
                        TikZ/PGFPlots output. If ``axis_width`` is not given,
                        ``matplot2tikz`` will try to preserve the original width/height
                        ratio.  Note that ``axis_width`` can be a string literal, such
                        as ``'\\axis_height'``.
    :type axis_height: str

    :param textsize: The text size (in pt) that the target latex document is using.
                     Default is 10.0.
    :type textsize: float

    :param tex_relative_path_to_data: In some cases, the TikZ file will have to refer to
                                      another file, e.g., a PNG for image plots. When
                                      ``\\input`` into a regular LaTeX document, the
                                      additional file is looked for in a folder relative
                                      to the LaTeX file, not the TikZ file.  This
                                      arguments optionally sets the relative path from
                                      the LaTeX file to the data.
    :type tex_relative_path_to_data: str

    :param externalize_tables: Whether or not to externalize plot data tables into dat
                               files.
    :type externalize_tables: bool

    :param override_externals: Whether or not to override existing external files (such
                               as dat or images) with conflicting names (the alternative
                               is to choose other names).
    :type override_externals: bool

    :param strict: Whether or not to strictly stick to matplotlib's appearance. This
                   influences, for example, whether tick marks are set exactly as in the
                   matplotlib plot, or if TikZ/PGFPlots can decide where to put the
                   ticks.
    :type strict: bool

    :param wrap: Whether ``'\\begin{tikzpicture}'``/``'\\starttikzpicture'`` and
                 ``'\\end{tikzpicture}'``/``'\\stoptikzpicture'`` will be
                 written. One might need to provide custom arguments to the environment
                 (eg. scale= etc.).  Default is ``True``.
    :type wrap: bool

    :param add_axis_environment: Whether ``'\\begin{axis}[...]'``/`'\\startaxis[...]'`
                                 and ``'\\end{axis}'``/``'\\stopaxis'``
                                 will be written. One needs to set the environment in
                                 the document. If ``False`` additionally sets
                                 ``wrap=False``. Default is ``True``.
    :type add_axis_environment: bool

    :param extra_axis_parameters: Extra axis options to be passed (as a list or set)
                                  to pgfplots. Default is ``None``.
    :type extra_axis_parameters: a list or set of strings for the pfgplots axes.

    :param extra_tikzpicture_parameters: Extra tikzpicture options to be passed
                                         (as a set) to pgfplots.
    :type extra_tikzpicture_parameters: a set of strings for the pfgplots tikzpicture.

    :param dpi: The resolution in dots per inch of the rendered image in case
                of QuadMesh plots. If ``None`` it will default to the value
                ``savefig.dpi`` from matplotlib.rcParams. Default is ``None``.
    :type dpi: int

    :param show_info: Show extra info on the command line. Default is ``False``.
    :type show_info: bool

    :param include_disclaimer: Include matplot2tikz disclaimer in the output.
                               Set ``False`` to make tests reproducible.
                               Default is ``True``.
    :type include_disclaimer: bool

    :param standalone: Include wrapper code for a standalone LaTeX file.
    :type standalone: bool

    :param float_format: Format for float entities. Default is ```".15g"```.
    :type float_format: str

    :param table_row_sep: Row separator for table data. Default is ```"\\n"```.
    :type table_row_sep: str

    :param flavor: TeX flavor of the output code.
                   Supported are ``"latex"`` and``"context"``.
                   Default is ``"latex"``.
    :type flavor: str

    :returns: None

    The following optional attributes of matplotlib's objects are recognized
    and handled:

     - axes.Axes._tikzplotlib_anchors
       This attribute can be set to a list of ((x,y), anchor_name) tuples.
       Invisible nodes at the respective location will be created which can be
       referenced from outside the axis environment.
    """
    # not as default value because gcf() would be evaluated at import time
    if figure == "gcf":
        figure = plt.gcf()
    elif not isinstance(figure, Figure):
        msg = "Argument 'figure' must be a Figure or string 'gcf'."
        raise ValueError(msg)

    data = {
        "axis width": axis_width,
        "axis height": axis_height,
        "rel data path": None
        if tex_relative_path_to_data is None
        else Path(tex_relative_path_to_data),
        "externalize tables": externalize_tables,
        "override externals": override_externals,
        "externals search path": externals_search_path,
        "strict": strict,
        "tikz libs": set(),
        "pgfplots libs": set(),
        "font size": textsize,
        "custom colors": {},
        "legend colors": [],
        "add axis environment": add_axis_environment,
        "show_info": show_info,
        "extra groupstyle options [base]": {}
        if extra_groupstyle_parameters is None
        else extra_groupstyle_parameters,
        # rectangle_legends is used to keep track of which rectangles have already
        # had \addlegendimage added. There should be only one \addlegendimage per
        # bar chart data series.
        "rectangle_legends": set(),
        "float format": float_format,
        "table_row_sep": table_row_sep,
        "include_disclaimer": include_disclaimer,
        "wrap": wrap,
        "extra_tikzpicture_parameters": extra_tikzpicture_parameters,
        "extra_lines_start": extra_lines_start,
        "standalone": standalone,
    }

    if filepath:
        filepath = Path(filepath)
        data["output dir"] = filepath.parent
        data["base name"] = filepath.stem
    else:
        directory = tempfile.mkdtemp()
        data["output dir"] = Path(directory)
        data["base name"] = "tmp"

    if extra_axis_parameters:
        data["extra axis options [base]"] = set(extra_axis_parameters).copy()
    else:
        data["extra axis options [base]"] = set()

    if dpi:
        data["dpi"] = dpi
    else:
        savefig_dpi = mpl.rcParams["savefig.dpi"]
        data["dpi"] = savefig_dpi if isinstance(savefig_dpi, int) else mpl.rcParams["figure.dpi"]

    try:
        data["flavor"] = Flavors[flavor.lower()]  # type: ignore[assignment]
    except KeyError:
        msg = (
            f"Unsupported TeX flavor {flavor!r}. Please choose from {', '.join(map(repr, Flavors))}"
        )
        raise ValueError(msg) from None

    # print message about necessary pgfplot libs to command line
    if show_info:
        _print_pgfplot_libs_message(data)

    # gather the file content
    data, content = _recurse(data, figure)

    # Check if there is still an open groupplot environment. This occurs if not
    # all of the group plot slots are used.
    if data.get("is_in_groupplot_env"):
        content.extend(data["flavor"].end("groupplot") + "\n\n")  # type: ignore[union-attr]

    return _generate_code(data, content)


def save(
    filepath: str | Path,
    encoding: str | None = None,
    **kwargs: Unpack[TikzArgs],
) -> None:
    """Same as `get_tikz_code()`, but actually saves the code to a file.

    :param filepath: The file to which the TikZ output will be written.
    :type filepath: str

    :param encoding: Sets the text encoding of the output file, e.g. 'utf-8'.
                     For supported values: see ``codecs`` module.
    :returns: None
    """
    code = get_tikz_code(filepath=filepath, **kwargs)
    if isinstance(filepath, str):
        filepath = Path(filepath)
    with filepath.open("w", encoding=encoding) as f:
        f.write(code)


def _generate_code(data: dict, content: list) -> str:
    # write disclaimer to the file header
    code = """"""

    if data["include_disclaimer"]:
        disclaimer = f"This file was created with matplot2tikz v{__version__}."
        code += _tex_comment(disclaimer)

    # write the contents
    if data["wrap"] and data["add axis environment"]:
        code += data["flavor"].start("tikzpicture")
        if data["extra_tikzpicture_parameters"]:
            code += "[\n" + ",\n".join(data["extra_tikzpicture_parameters"]) + "\n]"
        code += "\n"
        if data["extra_lines_start"]:
            code += "\n".join(data["extra_lines_start"]) + "\n"
        code += "\n"

    coldefs = _get_color_definitions(data)
    if coldefs:
        code += "\n".join(coldefs) + "\n\n"

    code += "".join(content)

    if data["wrap"] and data["add axis environment"]:
        code += data["flavor"].end("tikzpicture") + "\n"

    if data["standalone"]:
        # When using pdflatex, \\DeclareUnicodeCharacter is necessary.
        code = data["flavor"].standalone(code)
    return code


def _tex_comment(comment: str) -> str:
    """Prepends each line in string with the LaTeX comment key, '%'."""
    return "% " + str.replace(comment, "\n", "\n% ") + "\n"


def _get_color_definitions(data: dict) -> list:
    """Returns the list of custom color definitions for the TikZ file."""
    # sort by key
    sorted_keys = sorted(data["custom colors"].keys(), key=lambda x: x.lower())
    d = {key: data["custom colors"][key] for key in sorted_keys}
    return [f"\\definecolor{{{name}}}{{{space}}}{{{val}}}" for name, (space, val) in d.items()]


def _print_pgfplot_libs_message(data: dict) -> None:
    """Prints message to screen indicating the use of PGFPlots and its libraries."""
    LOGGER.info("Please add the following lines to your LaTeX preamble:")
    LOGGER.info(data["flavor"].preamble(data))


class _ContentManager:
    """Basic Content Manager for matplot2tikz.

    This manager uses a dictionary to map z-order to an array of content
    to be drawn at the z-order.
    """

    def __init__(self) -> None:
        self._content: Dict[float, List[str]] = {}

    def extend(self, content: list, zorder: float) -> None:
        """Extends with a list and a z-order."""
        if zorder not in self._content:
            self._content[zorder] = []
        self._content[zorder].extend(content)

    def flatten(self) -> list:
        content_out = []
        all_z = sorted(self._content.keys())
        for z in all_z:
            content_out.extend(self._content[z])
        return content_out


def _draw_collection(data: Dict, child: Collection) -> List[str]:
    if isinstance(child, PathCollection):
        return _path.draw_pathcollection(data, child)
    if isinstance(child, LineCollection):
        return _line2d.draw_linecollection(data, child)
    if isinstance(child, QuadMesh):
        return qmsh.draw_quadmesh(data, child)
    return _patch.draw_patchcollection(data, child)


def _recurse(data: Dict, obj: Artist) -> Tuple[Dict, List]:
    """Iterates over all children of the current object and gathers the contents.

    Data and content are returned.
    """
    content = _ContentManager()
    for child in obj.get_children():
        # Some patches are Spines, too; skip those entirely.
        # See <https://github.com/nschloe/tikzplotlib/issues/277>.
        if isinstance(child, (Spine, XAxis, YAxis)):
            continue

        if isinstance(child, Axes):
            _process_axes(data, child, content)
        elif isinstance(child, Legend):
            _legend.draw_legend(data, child)
            if data["legend colors"]:
                content.extend(data["legend colors"], 0)
        else:
            for child_type, process_func in (
                (Line2D, _line2d.draw_line2d),
                (AxesImage, img.draw_image),
                (Patch, _patch.draw_patch),
                (Collection, _draw_collection),
                (Text, _text.draw_text),
            ):
                if isinstance(child, child_type):
                    content.extend(process_func(data, child), child.get_zorder())
                    break
            else:
                warnings.warn(
                    f"matplot2tikz: Don't know how to handle object {type(child)}.", stacklevel=2
                )

    return data, content.flatten()


def _process_axes(data: dict, obj: Axes, content: _ContentManager) -> None:
    ax = _axes.MyAxes(data, obj)

    if ax.is_colorbar:
        return

    # add extra axis options
    if data["extra axis options [base]"]:
        ax.axis_options.extend(data["extra axis options [base]"])

    data["current mpl axes obj"] = obj
    data["current axes"] = ax

    # Run through the child objects, gather the content.
    data, children_content = _recurse(data, obj)

    # populate content and add axis environment if desired
    if data["add axis environment"]:
        content.extend(ax.get_begin_code() + children_content + [ax.get_end_code()], 0)
    else:
        content.extend(children_content, 0)
        # print axis environment options, if told to show infos
        if data["show_info"]:
            LOGGER.info("These would have been the properties of the environment:")
            LOGGER.info("".join(ax.get_begin_code()[1:]))


class Flavors(enum.Enum):
    latex = (
        r"\begin{{{}}}",
        r"\end{{{}}}",
        "document",
        """\
\\documentclass{{standalone}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{pgfplots}}
\\DeclareUnicodeCharacter{{2212}}{{-}}
\\usepgfplotslibrary{{{pgfplotslibs}}}
\\usetikzlibrary{{{tikzlibs}}}
\\pgfplotsset{{compat=newest}}
""",
    )
    context = (
        r"\start{}",
        r"\stop{}",
        "text",
        """\
\\setupcolors[state=start]
\\usemodule[tikz]
\\usemodule[pgfplots]
\\usepgfplotslibrary[{pgfplotslibs}]
\\usetikzlibrary[{tikzlibs}]
\\pgfplotsset{{compat=newest}}
% groupplot doesn't define ConTeXt stuff
\\unexpanded\\def\\startgroupplot{{\\groupplot}}
\\unexpanded\\def\\stopgroupplot{{\\endgroupplot}}
""",
    )

    def start(self, what: str) -> str:
        return self.value[0].format(what)

    def end(self, what: str) -> str:
        return self.value[1].format(what)

    def preamble(self, data: dict | None = None) -> str:
        if data is None:
            data = {
                "pgfplots libs": ("groupplots", "dateplot"),
                "tikz libs": ("patterns", "shapes.arrows"),
            }
        pgfplotslibs = ",".join(data["pgfplots libs"])
        tikzlibs = ",".join(data["tikz libs"])
        return self.value[3].format(pgfplotslibs=pgfplotslibs, tikzlibs=tikzlibs)

    def standalone(self, code: str) -> str:
        docenv = self.value[2]
        return f"{self.preamble()}{self.start(docenv)}\n{code}\n{self.end(docenv)}"
