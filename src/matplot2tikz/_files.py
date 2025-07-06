from pathlib import Path

from ._save import TikzData


def _gen_filepath(data: TikzData, nb_key: str, ext: str) -> tuple[Path, Path]:
    rel_filepath = Path(f"{data.base_name}-{data.nb_keys[nb_key]:03d}{ext}")

    if data.rel_data_path:
        rel_filepath = data.rel_data_path / rel_filepath

    return data.output_dir / rel_filepath, rel_filepath


def new_filepath(data: TikzData, file_kind: str, ext: str) -> tuple[Path, Path]:
    """Returns an available filepath.

    :param data: TikzData with various config options.
    :param file_kind: Name under which numbering is recorded, such as 'img' or 'table'.
    :param ext: Filename extension.

    :returns: (filepath, rel_filepath) where filepath is a path in the
              filesystem and rel_filepath is the path to be used in the tex
              code.
    """
    nb_key = file_kind + "number"
    if nb_key not in data.nb_keys:
        data.nb_keys[nb_key] = -1

    data.nb_keys[nb_key] += 1
    filepath, rel_filepath = _gen_filepath(data, nb_key, ext)
    if not data.override_externals:
        # Make sure not to overwrite anything.
        while filepath.is_file():
            data.nb_keys[nb_key] += 1
            filepath, rel_filepath = _gen_filepath(data, nb_key, ext)

    return filepath, rel_filepath
