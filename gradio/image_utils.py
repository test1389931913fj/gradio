from __future__ import annotations

from pathlib import Path
from typing import Literal

import numpy as np
from PIL import Image as _Image  # using _ to minimize namespace pollution

from gradio import processing_utils

_Image.init()


def format_image(
    im: _Image.Image | None,
    type: Literal["numpy", "pil", "filepath"],
    cache_dir: str,
    name: str = "image",
    format: str = "png",
) -> np.ndarray | _Image.Image | str | None:
    """Helper method to format an image based on self.type"""
    if im is None:
        return im
    fmt = im.format
    if type == "pil":
        return im
    elif type == "numpy":
        return np.array(im)
    elif type == "filepath":
        try:
            path = processing_utils.save_pil_to_cache(
                im, cache_dir=cache_dir, name=name, format=fmt or format  # type: ignore
            )
        # Catch error if format is not supported by PIL
        except (KeyError, ValueError):
            path = processing_utils.save_pil_to_cache(
                im, cache_dir=cache_dir, name=name, format="png"  # type: ignore
            )
        return path
    else:
        raise ValueError(
            "Unknown type: "
            + str(type)
            + ". Please choose from: 'numpy', 'pil', 'filepath'."
        )


def save_image(y: np.ndarray | _Image.Image | str | Path, cache_dir: str):
    # numpy gets saved to png as default format
    # PIL gets saved to its original format if possible
    if isinstance(y, np.ndarray):
        path = processing_utils.save_img_array_to_cache(y, cache_dir=cache_dir)
    elif isinstance(y, _Image.Image):
        fmt = y.format
        try:
            path = processing_utils.save_pil_to_cache(
                y, cache_dir=cache_dir, format=fmt  # type: ignore
            )
        # Catch error if format is not supported by PIL
        except (KeyError, ValueError):
            path = processing_utils.save_pil_to_cache(
                y, cache_dir=cache_dir, format="png"
            )
    elif isinstance(y, Path):
        path = str(y)
    elif isinstance(y, str):
        path = y
    else:
        raise ValueError(
            "Cannot process this value as an Image, it is of type: " + str(type(y))
        )

    return path
