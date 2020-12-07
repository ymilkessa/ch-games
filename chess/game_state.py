from game_state import GameState
from chess.moves import ChessMove
from constants import BLACK, WHITE
from chess.pieces import King


class ChessGameState(GameState):

    # the method 'all_possible_moves' is the same as the parent version
    def check_loss(self, side=None):
        if not side:
            side = self._current_side
        pieces = self._board.pieces_iterator(side)
        for piece in pieces:
            if isinstance(piece, King):
                return False
        return True
