from typing import Optional
import tcod.event

from actions import Action, EscapeAction, MovementAction

# creates a sub class of tcods EventDispatch class and allows us to send an event to its proper method based on what
# type of even it is.
class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    # receives key press events and returns either the Action subclass or None if no valid key was pressed.
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        # holds whatever subclass of Action we end up assigned, if non valid -> None
        action: Optional[Action] = None

        # holds the actual key that is pressed
        key = event.sym

        # going down the list of what is pressed, up-arrow, down-arrows, etc
        if key == tcod.event.KeySym.UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.KeySym.DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.KeySym.LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.KeySym.RIGHT:
            action = MovementAction(dx=1, dy=0)
        elif key == tcod.event.K_ESCAPE:    # if user presses escape key, exit the game
            action = EscapeAction()

        # No valid key was pressed
        return action