from piece import Piece
from piece_factory import PieceFactory
from constants import BLACK, WHITE
from chess_moves import ChessMove


class ChessPieceFactory(PieceFactory):
    """Generates the chess piece for a given slot when setting up the board"""

    def create_piece(self, board, space):
        x, y = space.row, space.col
        cvt_row_to_side = lambda row: BLACK if row < 2 else WHITE
        if x == 1 or x == board.size-2:
            return Pawn(cvt_row_to_side(x), board, space)
        elif x > 1 and x < board.size-2:
            return None
        elif y == 0 or y == board.size - 1:
            return Rook(cvt_row_to_side(x), board, space)
        elif y == 1 or y == board.size - 2:
            return Knight(cvt_row_to_side(x), board, space)
        elif y == 2 or y == board.size - 3:
            return Bishop(cvt_row_to_side(x), board, space)
        elif y == 3:
            return Queen(cvt_row_to_side(x), board, space)
        elif y == 4:
            return King(cvt_row_to_side(x), board, space)


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
        self._value = 1

    def enumerate_moves(self):
        """Used to find possible moves and captures that this piece can make"""
        add_ew = lambda x: [x+'e', x+'w']
        allowed_catches = add_ew(self._directions[0])
        moves = []
        # First add the one/two step forward moves
        new_slot = self._board.get_dir(self._current_space, self._directions[0])
        if new_slot and new_slot.is_free():
            moves.append(ChessMove(self._current_space, new_slot))
            if (self._side == BLACK and new_slot.row == self._board.size - 1) or \
                (self._side == WHITE and new_slot.row == 0):
                moves[-1].add_promotion()
        if (self._side == BLACK and self._current_space.row == 1) or \
            (self._side == WHITE and self._current_space.row == self._board.size -2):
            new_slot = self._board.get_dir(new_slot, self._directions[0])
            if new_slot and new_slot.is_free():
                moves.append(ChessMove(self._current_space, new_slot))

        # Now add all the captures.
        for direction in allowed_catches:
            new_slot = self._board.get_dir(self._current_space, direction)
            if new_slot and new_slot.has_opponent(self._side):
                moves.append(ChessMove(self._current_space, new_slot, [new_slot]))
                if (self._side == BLACK and new_slot.row == self._board.size - 1) or \
                    (self._side == WHITE and new_slot.row == 0):
                    moves[-1].add_promotion()
        return moves

    def promote(self):
        "Overrides promote to return a KingChecker in the same space for the same side"
        return Queen(self._side, self._board, self._current_space)


class King(Piece):
    "Can move only a single step in any of all 8 immediate directions"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._directions = ["n", "e", "s", "w", "ne", "nw", "se", "sw"]
        if self._side == WHITE:
            self._symbol = u"♔"
        if self._side == BLACK:
            self._symbol = u"♚"
        self._value = 100
    
    def enumerate_moves(self):
        moves = []
        for direction in self._directions:
            new_slot = self._board.get_dir(self._current_space, direction)
            if new_slot and new_slot.is_free():
                m = ChessMove(self._current_space, new_slot)
                moves.append(m)
            elif new_slot and new_slot.has_opponent(self._side):
                m = ChessMove(self._current_space, new_slot, [new_slot])
                moves.append(m)
        return moves


class Rook(Piece):
    """
    Concrete class for rooks. This will also be a template for pieces that 
    can move to any distance in a straight line from their position.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._side == WHITE:
            self._symbol = u"♖"
        if self._side == BLACK:
            self._symbol = u"♜"
        self._directions = ["n", "e", "s", "w"]  # But can move to any distance on the board.
        self._value = 5

    def enumerate_moves(self):
        moves = []
        for direction in self._directions:
            end_reached = False
            next_slot = self._current_space
            while not end_reached:
                next_slot = self._board.get_dir(next_slot, direction)
                if not next_slot:
                    end_reached = True
                elif next_slot.is_free():
                    moves.append(ChessMove(self._current_space, next_slot))
                elif next_slot.has_opponent(self._side):
                    moves.append(ChessMove(self._current_space, next_slot, [next_slot]))
                    end_reached = True
                else:
                    assert next_slot.piece._side == self._side  # TODO: remove later
                    end_reached = True
        return moves
    

class Bishop(Rook):
    """Concrete class for bishop"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._side == WHITE:
            self._symbol = u"♗"
        if self._side == BLACK:
            self._symbol = u"♝"
        self._directions = ["ne", "se", "sw", "nw"]
        self._value = 3


class Queen(Rook):
    """Concrete class for queen"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._side == WHITE:
            self._symbol = u"♕"
        if self._side == BLACK:
            self._symbol = u"♛"
        self._directions = ["n", "e", "s", "w", "ne", "se", "sw", "nw"]
        self._value = 9


class Knight(Piece):
    """Concrete class for knights"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._side == WHITE:
            self._symbol = u"♘"
        if self._side == BLACK:
            self._symbol = u"♞"
        self._value = 3

    def enumerate_moves(self):
        moves = []
        directions_array = [["n", "s"], ["e", "w"]]
        for k in range(2):
            first_directions = directions_array[k]
            for direction in first_directions:
                step1 = self._board.get_dir(self._current_space, direction)
                if not step1:
                    continue
                step2 = self._board.get_dir(step1, direction)
                if not step2:
                    continue
                next_dirs = directions_array[(k+1)%2]
                for next_direction in next_dirs:
                    step3 = self._board.get_dir(step2, next_direction)
                    if not step3:
                        continue
                    elif step3.is_free():
                        moves.append(ChessMove(self._current_space, step3))
                    elif step3.has_opponent(self._side):
                        moves.append(ChessMove(self._current_space, step3, [step3]))
        return moves