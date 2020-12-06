from constants import BLACK, CHECKERS, CHESS, WHITE
from board import Board
from players import Player, HumanPlayer
from copy import deepcopy
import sys

from checkers.pieces import CheckerFactory
from checkers.game_state import CheckersGameState


class GameHistory():
    def __init__(self):
        # stack of old game states that can be reached with undo
        self._undo_stack = []

        # temporary stack of game states built as undo is called
        self._redo_stack = []

    def push(self, gs):
        """Saves a new game state and invalidates any potential redos

        Args:
            gs GameState): current game state to add to undo stack
        """
        self._undo_stack.append(gs)
        self._redo_stack = []

    def undo(self, gs):
        """
        Args:
            gs (GameState): current game state to add to redo stack. 

        Returns:
            GameState: previous game state from undo stack
        """

        if len(self._undo_stack) == 0:
            return None
        x = self._undo_stack.pop()
        self._redo_stack.append(gs)
        return x

    def redo(self, gs):
        """
        Args:
            gs (GameState): current game state to add to undo stack

        Returns:
            GameState: game state most recently added to redo stack by an undo
        """

        if len(self._redo_stack) == 0:
            return None
        self._undo_stack.append(gs)
        return self._redo_stack.pop()


class GameDriver:
    def __init__(self, game_type="chess",
                 player1=HumanPlayer(),
                 player2=HumanPlayer(),
                 size=8,
                 history_enabled=False):

        # create board, set up, and initialize game state
        if not game_type in ["checkers", "chess"]:
            raise Exception(f"Invalid argument {game_type}")
        # TODO: Add options for Chess GameState, Board(?), PieceFactory
        if game_type == "chess":
            pass
        else:
            b = Board(int(size), CheckerFactory())
        b.set_up()
        self._game_state = CheckersGameState(b, WHITE, None)

        # set up players
        self._players = {
            WHITE: player1,
            BLACK: player2
        }
        player1.side = WHITE
        player2.side = BLACK

        # set up history
        if history_enabled:
            self._history = GameHistory()
        self.history_enabled = history_enabled

    def start_game(self):
        # game loop
        while(True):
            print(self._game_state)

            if self._game_state.check_loss():
                if self._game_state.current_side == WHITE:
                    print("black has won")
                else:
                    print("white has won")
                return

            if self._game_state.check_draw():
                print("draw")
                return

            if self.history_enabled:
                option = input("undo, redo, or next\n")
                while option not in ["undo", "redo", "next"]:
                    print(f"Please enter a valid command; given {option}")
                    option = input("undo, redo, or next\n")
            else:
                # continue as if next was entered
                option = "next"

            if option == "undo":
                last_state = self._history.undo(self._game_state)
                if last_state:
                    self._game_state = last_state
            elif option == "redo":
                next_state = self._history.redo(self._game_state)
                if next_state:
                    self._game_state = next_state
            elif option == "next":
                # copy the old state before making a move
                prev_state = deepcopy(self._game_state)

                player = self._players[self._game_state.current_side]
                player.take_turn(self._game_state)

                if self.history_enabled:
                    self._history.push(prev_state)


if __name__ == "__main__":

    # take in arguments and setup defaults if necessary
    # TODO: Change this to accommodate chess.
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
    if len(sys.argv) > 4:
        size = sys.argv[4]
    else:
        size = 8
    history = len(sys.argv) > 5 and sys.argv[5] == "history"

    # create driver and start game
    game = GameDriver(game_type, player1, player2, size, history)
    game.start_game()
