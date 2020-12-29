import random


class Player:
    "Abstract player class"

    def __init__(self, side=None) -> None:
        self.side = side

    def take_turn(self):
        raise NotImplementedError()

    @staticmethod
    def create_player(player_type):
        "Factory method for creating players"
        if player_type == "human":
            return HumanPlayer()
        elif player_type == "random":
            return RandomCompPlayer()
        elif player_type == "simple":
            return SimpleCompPlayer()
        elif player_type.startswith("minimax"):
            return MinimaxCompPlayer(int(player_type[7:]))
        else:
            return None


class HumanPlayer(Player):
    "Concrete player class that prompts for moves via the command line"

    def take_turn(self, game_state):
        b = game_state.board
        while True:
            chosen_piece = input("Select a piece to move\n")
            chosen_piece = b.get_space(chosen_piece).piece
            if chosen_piece is None:
                print("no piece at that location")
                continue
            if chosen_piece.side != self.side:
                print("that is not your piece")
                continue
            options = chosen_piece.enumerate_moves()
            if len(options) == 0 or options[0] not in game_state.all_possible_moves():

                print("that piece cannot move")
                continue

            self._prompt_for_move(options).execute(game_state)
            return

    def _prompt_for_move(self, options):
        while True:
            for idx, op in enumerate(options):
                print(f"{idx}: {op}")
            chosen_move = input(
                "Select a move by entering the corresponding index\n")
            try:
                chosen_move = options[int(chosen_move)]
                return chosen_move
            except ValueError:
                print("not a valid option")


class RandomCompPlayer(Player):
    "Concrete player class that picks random moves"

    def take_turn(self, game_state):
        options = game_state.all_possible_moves()
        m = random.choice(options)
        print(m)
        m.execute(game_state)


class SimpleCompPlayer(Player):
    "Concrete player class that chooses moves that capture the most pieces while breaking ties randomly"

    def take_turn(self, game_state):
        options = game_state.all_possible_moves()
        max_captures = 0
        potential_moves = []
        for m in options:
            if m.val_of_captures() > max_captures:
                potential_moves = [m]
                max_captures = m.num_captures()
            elif m.val_of_captures() == max_captures:
                potential_moves.append(m)

        selected_move = random.choice(potential_moves)
        print(selected_move)
        selected_move.execute(game_state)


class MinimaxCompPlayer(Player):
    """Uses the minimax algorithm to pick a move"""

    def __init__(self, depth=1):
        super().__init__()
        self._depth = depth
    
    def take_turn(self, game_state):
        best_option = game_state.get_optimal_move(self._depth)
        selected_move = best_option[0]
        print(selected_move)
        selected_move.execute(game_state)        
