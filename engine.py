# Engine will take responsibility for drawing the map, entities and handling player input
from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from actions import EscapeAction, MovementAction
from entity import Entity
from input_handlers import EventHandler

class Engine:
    '''
    entities is a set of entities that helps enforce uniqueness, that is we can't add an Entity twice.
    event_handler handles events and player is the player Entity.
    '''
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            if isinstance(action, MovementAction):
                self.player.move(dx=action.dx, dy=action.dy)
            elif isinstance(action, EscapeAction):
                raise SystemExit()

    def render(self, console: Console, context: Context) -> None:
        # The Render Method handles drawing our screen.
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)
        context.present(console)
        console.clear()