from constants import BLACK, WHITE
from copy import deepcopy
import random


class GameState():
    def __init__(self, board, side, players):
        
        self._players = players
        self._turn_counter = 1
        # read only properties
        self._current_side = side
        self._board = board
        # public property
        self._draw_counter = 0

    @property
    def current_side(self):
        return self._current_side

    @property
    def board(self):
        return self._board

    @property
    def draw_counter(self):
        return self._draw_counter

    @draw_counter.setter
    def draw_counter(self, c):
        self._draw_counter = c

    def next_turn(self):
        self._current_side = not self._current_side
        self._turn_counter += 1

    def prev_turn(self):
        self._current_side = not self._current_side
        self._turn_counter -= 1

    def __str__(self):
        if self._current_side == WHITE:
            side_string = "white"
        elif self._current_side == BLACK:
            side_string = "black"
        else:
            raise ValueError("Current player is neither black nor white")
        return f"{self._board}\nTurn: {self._turn_counter}, {side_string}"

    def all_possible_moves(self, side=None):
        """Iterates over a side's pieces and returns a list containing all legal moves

        Args:
            side ([type], optional): side for which moves should be retrieved. Defaults to the game state's current side.

        Returns:
            list: list of Move objects 
        """
        if not side:
            side = self._current_side
        pieces = self._board.pieces_iterator(side)
        options = []
        for piece in pieces:
            options.extend(piece.enumerate_moves())

        return options

    def get_optimal_move(self, depth, best_so_far=-1000, side=None):
        """Applies the minimax algorith to recursively compute the expected gain/loss total of making a move. 

        Args:
            depth (int): how many steps of recursion you want to make
            side (bool, optional): Default gets replaced by the current side, either WHITE or BLACK
            best_so_far (int): The best utility from neighboring branches; for alpha-beta pruning
        Return:
            tuple([optimal_move, expected_value]): optimal_move is a Move instance; expected_value is an int
        """
        if side == None:
            side = self._current_side
        next_moves = self.all_possible_moves(side)  # Cannot be [] at this point
        options_list = []
        for poss_m in next_moves:  # poss_m means 'possible_move'
            current_utility = poss_m.val_of_captures()
            if depth == 0:
                new_option = (poss_m, current_utility)
            else:
                state_copy = deepcopy(self)
                move_copy = poss_m.copy_from(state_copy)
                move_copy.execute(state_copy)
                # Now you're in the oponent's shoes.
                opponent_move = state_copy.get_optimal_move(depth-1, best_so_far)
                new_option = (poss_m, current_utility-opponent_move[1])
                # Do the alpha-beta pruing
                if new_option[1] > best_so_far:
                    best_so_far = new_option[1]
                elif new_option[1] < best_so_far:
                    # break the loop here
                    options_list = [new_option]
                    break
            options_list.append(new_option)
        
        # Now pick the option with the highest utility
        best_option = options_list[0]
        for next_option in options_list[1:]:
            if next_option[1] > best_option[1]:
                best_option = next_option
            elif next_option[1] == best_option[1]:
                best_option = random.choice([next_option, best_option])
        return (best_option[0].copy_from(self), best_option[1])


    def check_draw(self, side=None):
        if not side:
            side = self._current_side
        # no moves available
        if len(self.all_possible_moves(side)) == 0:
            return True
        # 50 turn rule
        if self._draw_counter >= 50:
            return True
        # default to no draw
        return False

    def check_loss(self, side=None):
        # Specific rules for loss should be implemented per game
        raise NotImplementedError()
    
    def get_space(self, space):
        return self.board.get_space_from_coords((space.row, space.col))
