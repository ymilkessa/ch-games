
class Piece:
    "Abstract piece class"

    def __init__(self, side, board, space):
        self._current_space = space
        self._board = board
        # read only property
        self._side = side
        self._symbol = None  # Gets added in concrete class
        self._value = 1  # This gets replaced in concrete classes

    @property
    def side(self):
        return self._side
    
    @property
    def value(self):
        return self._value  # This will get over-ridden by subclasses.

    def __str__(self):
        return self._symbol

    def move(self, space):
        self._current_space = space

    def promote(self):
        "Promote returns the current piece by default (doing nothing), but may be overridden for specific piece rules"
        return self

    def enumerate_moves(self):
        """Abstract method
        Concrete implementations should return a list of valid Move objects
        """
        raise NotImplementedError()

    def is_valid_move(self, new_space):
        return new_space in self.enumerate_moves()

