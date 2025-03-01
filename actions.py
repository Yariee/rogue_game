from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform action with the objects needed to determine the scope"""
        raise NotImplementedError()
class EscapeAction(Action):   # hitting the esc key will exit the game.
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()

class MovementAction(Action):   # used to describe our player moving around
    def __init__(self, dx: int, dy: int):
        super().__init__()

        # used to describe which direction the player is moving in
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        # Double checking that move is inbounds and walkable
        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination out of bounds
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by tile.

        entity.move(self.dx, self.dy)