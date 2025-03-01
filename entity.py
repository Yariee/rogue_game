from typing import Tuple

class Entity:
    # Generic object to represent players, enemies, items, etc etc

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        # x and y represent the entities coordinates on the map
        self.x = x
        self.y = y
        # char is the character we'll use to represent the entity
        self.char = char
        # color defined as a tuple of RGB
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        # move entity by given amount
        self.x += dx
        self.y += dy