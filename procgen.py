from __future__ import annotations
import random
from typing import Iterator, List, Tuple, TYPE_CHECKING
import tcod

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entity import Entity

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

# function definition
def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        player: Entity,
) -> GameMap:
    """Helps generate a new dungeon map."""
    dungeon = GameMap(map_width, map_height)

    # keeping a list of all the rooms
    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        # use the given min and max room sizes to set rooms height and width. We can a random x and y coordinate to
        # try and place the room down, coordinates must be between 0 and the maps width and height
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        # Check to see if other rooms intersect with the one we're making
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue    # Room intersects, go to next attempt. If no intersects, room is valid

        # digging out inner room area if the room is valid.
        dungeon.tiles[new_room.inner] = tile_types.floor

        # player starting room
        if len(rooms) == 0:
            player.x, player.y = new_room.center
        # every other room after the first
        else:
            # Digging out tunnel between this room and previous ones
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        # append room to the list
        rooms.append(new_room)

    return dungeon