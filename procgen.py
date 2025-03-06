from __future__ import annotations
import random
from typing import Iterator, Tuple
import tcod

from game_map import GameMap
import tile_types

# used to create our rooms
class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        # taking the x and y coordinates of the top left hand corner and computing the bottom right hand corner
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        # acts as a "read-only" variable that describes the coordinates of the center of the room
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        # inner portion of the room where we will be "digging" out
        # slices return selected elements in an array
        """ Returning the inner area of this room as a 2D array index.
            This also allows us to ensure that we'll have at least a one tile wide wall
            between our rooms with self.x1 + 1 and self.y1 + 1
        """
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """ Return True if  this rooms overlaps with another RectangularRooms.
            Checks if our other rooms intersect with each other. True if they
            do, False if they dont
        """
        return(
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

# Tuples will return coordinates
def tunnel_between(
        start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """ Return a L-Shaped tunnel between two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:   # 50% chance
        # Move horizontally then vertically
        corner_x, corner_y = x2, y1
    else:
        # Move vertically then horizontally
        corner_x, corner_y = x1, y2

    # Generate the coordinates for the tunnel using the Bresenham algo that gets a line from one point to another
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        # yield allows us to return a "generator". We return values and keep the local state. When the function is
        # called again, it picks up where we left off rather than starting over.
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(map_width, map_height) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    room1 = RectangularRoom(x=20, y=15, width=10, height=15)
    room2 = RectangularRoom(x=35, y=15, width=10, height=15)

    dungeon.tiles[room1.inner] = tile_types.floor
    dungeon.tiles[room2.inner] = tile_types.floor

    for x, y in tunnel_between(room2.center, room1.center):
        dungeon.tiles[x, y] = tile_types.floor

    return dungeon