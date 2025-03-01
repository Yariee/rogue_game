import numpy as np  # type: ignore
from tcod.console import Console

import tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        # creating a 2D Array that will help fill self.tiles
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")
        # hard coding a wall for demonstration to see how it works.
        self.tiles[30:33, 22] = tile_types.wall

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of the map"""
        # ensures the player doesn't move beyond the scope of the map
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        # Allows us to render the whole map
        console.tiles_rgb[0: self.width, 0: self.height] = self.tiles["dark"]
