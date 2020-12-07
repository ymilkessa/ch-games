from move import Move


class ChessMove(Move):
    def __repr__(self):
        return str(self)

    def __str__(self):
        if not self._captures:
            return f"basic move: {self._start}->{self._end}"
        else:
            return f"jump move: {self._start}->{self._end}, capturing {self._captures}"

    def is_jump(self):
        return len(self._captures) > 0
