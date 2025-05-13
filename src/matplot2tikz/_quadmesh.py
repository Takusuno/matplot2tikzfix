from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.collections import QuadMesh
from PIL import Image

from . import _files


def draw_quadmesh(data: dict, obj: QuadMesh) -> list:
    """Returns the PGFPlots code for a graphics environment holding a rendering of the object."""
    content = []

    # Generate file name for current object
    filepath, rel_filepath = _files.new_filepath(data, "img", ".png")

    # Get the dpi for rendering and store the original dpi of the figure
    dpi = data["dpi"]
    fig_dpi = obj.figure.get_dpi()
    obj.figure.set_dpi(dpi)

    # Render the object and save as png file
    cbox = obj.get_clip_box()
    if cbox is None:
        raise ValueError
    width = round(cbox.extents[2])
    height = round(cbox.extents[3])
    ren = RendererAgg(width, height, dpi)
    obj.draw(ren)

    # Generate a image from the render buffer
    image = Image.frombuffer(
        "RGBA", ren.get_canvas_width_height(), ren.buffer_rgba(), "raw", "RGBA", 0, 1
    )
    # Crop the image to the actual content (removing the regions otherwise
    # used for axes, etc.)
    # 'image.crop' expects the crop box to specify the left, upper, right, and
    # lower pixel. 'cbox.extents' gives the left, lower, right, and upper
    # pixel.
    box = (
        round(cbox.extents[0]),
        0,
        round(cbox.extents[2]),
        round(cbox.extents[3] - cbox.extents[1]),
    )
    cropped = image.crop(box)
    cropped.save(filepath)

    # Restore the original dpi of the figure
    obj.figure.set_dpi(fig_dpi)

    # write the corresponding information to the TikZ file
    axes = obj.axes
    if axes is None:
        msg = "Object has no axes."
        raise ValueError(msg)
    extent = axes.get_xlim() + axes.get_ylim()

    # Explicitly use \pgfimage as includegrapics command, as the default
    # \includegraphics fails unexpectedly in some cases
    ff = data["float format"]
    posix_filepath = rel_filepath.as_posix()
    content.append(
        "\\addplot graphics [includegraphics cmd=\\pgfimage,"
        f"xmin={extent[0]:{ff}}, xmax={extent[1]:{ff}}, "
        f"ymin={extent[2]:{ff}}, ymax={extent[3]:{ff}}] {{{posix_filepath}}};\n"
    )

    return content
