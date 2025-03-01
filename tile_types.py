from typing import Tuple

import numpy as np # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
# dtype is a type of data type that Numpy can use which behaves like a struct
graphic_dt = np.dtype(
    [
        ("ch", np.int32),   # the character represented in integer format that will be translated into unicode
        ("fg", "3B"),   # the foreground color. "3B" is unsigned bytes which can be used for RGB
        ("bg", "3B"),   # Background color, similar to foreground color as above.
    ]
)

# Tile struct used for statically defined tile data. Another of type dtype.
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if tile can be walked over
        ("transparent", np.bool),   # True if tile doesn't block FOV
        ("dark", graphic_dt),   # Graphics for when tile is not in the FOV
    ]
)

def new_tile(
        *,  # enforce the use of keywords
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types"""
    return np.array((walkable, transparent, dark), dtype=tile_dt)

floor = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
)

wall = new_tile(
    walkable=False, transparent=False, dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
)