class Action:
    pass

class EscapeAction(Action):   # hitting the esc key will exit the game.
    pass

class MovementAction(Action):   # used to describe our player moving around
    def __innit__(self, dx: int, dy: int):
        super().__init__()

        # used to describe which direction the player is moving in
        self.dx = dx
        self.dy = dy