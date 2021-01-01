import sys

from players import Player
from main import GameDriver
from gui import Gui

class VisualGameDriver(GameDriver):
    """
    Extends the game driver to utilitize a pygame window for the board.
    """
    def __init__(self, *args):
        super().__init__(*args)
        self._game_state.use_gui()  # TODO: Still haven't defined this yet.

if __name__ == "__main__":

    # take in arguments and setup defaults if necessary
    if len(sys.argv) > 1:
        game_type = sys.argv[1]
    else:
        game_type = "chess"
    if len(sys.argv) > 2:
        player1 = Player.create_player(sys.argv[2])
        if not player1:
            sys.exit()
    else:
        player1 = Player.create_player("human")
    if len(sys.argv) > 3:
        player2 = Player.create_player(sys.argv[3])
        if not player2:
            sys.exit()
    else:
        player2 = Player.create_player("human")
    if game_type != "chess" and len(sys.argv) > 4:
        size = sys.argv[4]
    else:
        size = 8
    history = len(sys.argv) > 5 and sys.argv[5] == "history"

    # create driver and start game
    game = VisualGameDriver(game_type, player1, player2, size, history)
    game.start_game()
