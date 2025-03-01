import tcod

from actions import EscapeAction, MovementAction
from entity import Entity
from input_handlers import EventHandler
def main():

    # screen size
    screen_width = 80
    screen_height = 50

    # telling tcod which font we are going to be using.
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # used to receive events and process them
    event_handler = EventHandler()

    # initializing a new player and a NPC from the Entity class
    player = Entity(int(screen_width / 2), int (screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int (screen_height / 2), "@", (255, 255, 255))
    entities = {npc, player}

    # Creating the screen
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        # creating our "console" which is what we're drawing to.
        root_console = tcod.Console(screen_width, screen_height, order="F")
        # game loop, won't end unless we exit the screen.
        while True:
            # Tells the program to put the "@" on the screen in its proper coordinates.
            root_console.print(x=player.x, y=player.y, string=player.char, fg=player.color)
            context.present(root_console)

            # when we move, it allows us to not leave a trail/tail
            root_console.clear()

            for event in tcod.event.wait():
                # allows us to the event to its proper place
                action = event_handler.dispatch(event)
                if action is None:
                    continue

                # if action is an instance of MovementClass, we move our "@" symbol
                if isinstance(action, MovementAction):
                    player.move(dx=action.dx, dy=action.dy)
                # if user hits esc key, program exits
                elif isinstance(action, EscapeAction):
                    raise SystemExit()

if __name__ == "__main__":
    main()