from game_state import GameState
from chess.moves import ChessMove
from constants import BLACK, WHITE


class ChessGameState(GameState):

    # the method 'all_possible_moves' is the same as the parent version
    def check_loss(self, side=None):
        if not side:
            side = self._current_side
        pieces = self._board.pieces_iterator(side)
        array = [1 for piece in pieces if isinstance(piece, King) else 0]
        return sum(array) == 0
