from gui import Gui
import pygame
import os

class ChessGui(Gui):
    """
    The Gui implementation for chess
    """
    def __init__(self, *args):
        super().__init__(*args)

    def insert_pieces(self):
        pics_file = os.path.join(*["pics", "board_and_pieces_cropped.png"])
        pieces_image = pygame.image.load(pics_file)
        # Start creating surfaces for the pieces.
        for color, row in [["white", 0], ["black", 1]]:
            # create 6 transparent surfaces (the number 32 is 'depth' and makes it transparent??)
            _list = [pygame.Surface((45, 45), pygame.SRCALPHA, 32) for i in range(6)]
            names = ["king", "queen", "bishop", "knight", "rook", "pawn"]
            for i in range(len(names)):
                exec(f"{color}{names[i]} = _list[i]")
                exec(f"{color}{names[i]}.blit(pieces_image, (0,0), (self.board_width + row*self.cell_width, i*self.cell_width, self.cell_width, self.cell_width))")
        # Now start filling in the pieces
        for piece in self.board_reference.pieces_iterator():
            matrix_coordinates = piece.coordinates()
            coordinates = tuple([self.cell_width*val for val in matrix_coordinates])
            exec(f"self.screen.blit({piece.type_string()}, {coordinates})")
