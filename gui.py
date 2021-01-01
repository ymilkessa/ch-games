import pygame
import os


class Gui():
    """
    The framework for an interactive chess board.
    """
    def __init__(self, matrix):
        # TODO: Now start writing about what happens here to the gui
        self.cell_width = 45
        cell_dim = tuple([self.cell_width, self.cell_width])
        self.green_cell, self.white_cell = pygame.Surface(cell_dim), pygame.Surface(cell_dim)
        self.green_cell.fill((0, 200, 0))
        self.white_cell.fill((255, 255, 255))
        # self.board_and_pieces = pygame.image.load(os.path.join("pics", "board_and_pieces_cropped.png"))
        self.board_width = self.cell_width*8  # self.board_and_pieces.get_width()
        # cell_width = self.board_width / 8
        # print(f"Board width: {self.board_width}\nCell width: {self.cell_width}")

        pygame.init()
        screen = pygame.display.set_mode((self.board_width, self.board_width))
        rows = len(matrix)
        for i in range(rows):
            for j in range(rows):
                x = j*self.cell_width
                y = i*self.cell_width
                if matrix[i][j]:
                    screen.blit(self.green_cell, (x, y))
                else:
                    screen.blit(self.white_cell, (x, y))
        pygame.display.update()
        self.display()
    
    def display(self):
        # pygame.init()
        # screen = pygame.display.set_mode((self.board_width, self.board_width))  # Creates a surface with the same dimensions as the board
        # self.board_and_pieces.convert()  # Not sure what this does
        # screen.blit(self.board_and_pieces, (0,0), (0, 0, self.board_width, self.board_width))  # Adds the board image to the surface
        # pygame.display.update()  # Updates the change to `screen`
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
    
    def show_path(self, path: list):
        "Puts a glow in each of the contiguous cells listed in `path` to indicate a possible move"
        raise NotImplementedError
    
    def show_move(self, path: list):
        "Shows a piece moving along the board along the specified path"
        raise NotImplementedError

# For testing:
if __name__=="__main__":
    func = lambda row, col: 1 if abs(row-col) %2 == 0 else 0
    matrix = [[func(i, j) for j in range(8)] for i in range(8)]
    Gui(matrix)
