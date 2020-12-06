from piece import Piece
from piece_factory import PieceFactory
from constants import BLACK, WHITE


class ChessPieceFactory(PieceFactory):
    """Generates the chess piece for a given slot when setting up the board"""
    def create_pieces(self, board, space):
        x, y = space.row, space.col
        if x == 1:
            # TODO


# Whites:
# ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
# ♙

# Blacks:
# ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
# ♟
class Pawn(Piece):
    "Concrete piece class for a pawn"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._side == WHITE:
            self._symbol = u"♙"
            self._directions = ["n"]
        if self._side == BLACK:
            self._symbol = u"♟"
            self._directions = ["s"]

    def enumerate_moves(self):
        # moves = CheckersMoveSet() # TODO

        # jump moves
        # done first since we can skip singles if we find any jumps
        self._enumerate_jumps(moves, self._current_space, [])

        # basic moves
        if len(moves) == 0:
            for direction in self._directions:
                one_step = self._board.get_dir(self._current_space, direction)
                if one_step and one_step.is_free():
                    m = CheckersMove(self._current_space, one_step)
                    moves.append(m)
                    if (self._side == WHITE and one_step.row == 0) or \
                            (self._side == BLACK and one_step.row == self._board.size - 1):
                        m.add_promotion()

        return moves

    def _enumerate_catches(self, moves, current_space, captured, midjump=False):
        """Used to find possible captures that your piece can make"""
        if self._side == WHITE:
            allowed_directions = ["nw", "ne"]
        else:
            allowed_directions = ["sw", "se"]
        catch_moves = []
        for direction in allowed_directions:
            self._board.get_dir(current_space, direction)
            


    def promote(self):
        "Overrides promote to return a KingChecker in the same space for the same side"
        return KingChecker(self._side, self._board, self._current_space)


class KingChecker(Checker):
    "Same as a basic checker except that it can move in all 4 directions, has a different symbol, and cannot be promoted further"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._directions = ["ne", "nw", "se", "sw"]
        if self._side == WHITE:
            self._symbol = u"⚇"
        if self._side == BLACK:
            self._symbol = u"⚉"

    def promote(self):
        "Override promote to return self since a king cannot be promoted further"
        return self

