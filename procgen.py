from typing import Tuple

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
        """ Returning the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)