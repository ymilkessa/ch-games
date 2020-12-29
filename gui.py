import pygame
import os


class Gui():
    """
    The framework for an interactive chess board.
    """
    def __init__(self):
        self.board_and_pieces = pygame.image.load(os.path.join("pics", "board_and_pieces_cropped.png"))
        self.board_width = self.board_and_pieces.get_width()
        cell_width = self.board_width / 8
        print(f"Board width: {self.board_width}\nCell width: {cell_width}")
    
    def display(self):
        pygame.init()
        screen = pygame.display.set_mode((self.board_width, self.board_width))  # Creates a surface with the same dimensions as the board
        self.board_and_pieces.convert()  # Not sure what this does
        screen.blit(self.board_and_pieces, (0,0), (0, 0, self.board_width, self.board_width))  # Adds the board image to the surface
        pygame.display.update()  # Updates the change to `screen`
        # TODO: Add a frame, add a bar for showing status

        mainloop = True
        while mainloop:

            # TODO: Add all the remaining stuff here
            # including interacting with a computer player as well as a human agent.

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False

if __name__=="__main__":
    Gui().display()
