import pygame
import os


class Gui():
    """
    The framework for an interactive chess board.
    """
    def __init__(self, board_reference):
        # TODO: Now start writing about what happens here to the gui
        self.cell_width = 45  # 45 pixel width for each cell
        cell_dim = tuple([self.cell_width, self.cell_width])
        self.green_cell, self.white_cell = pygame.Surface(cell_dim), pygame.Surface(cell_dim)
        self.green_cell.fill((0, 200, 0))
        self.white_cell.fill((255, 255, 255))
        self.board_width = self.cell_width*8
        self.current_move = None
        self.board_reference = board_reference

        pygame.init()
        self.screen = pygame.display.set_mode((self.board_width, self.board_width))
        matrix = board_reference.board_matrix()
        rows = len(matrix)
        for i in range(rows):
            for j in range(rows):
                x = j*self.cell_width
                y = i*self.cell_width
                if matrix[i][j]:
                    self.screen.blit(self.green_cell, (x, y))
                else:
                    self.screen.blit(self.white_cell, (x, y))
        self.insert_pieces()
        pygame.display.update()
        self.display()
    
    def display(self):
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
                # if there is a current move, display it.
                elif self.current_move:
                    # TODO: Do stuff to display the move.
                    pass
                    self.current_move = None
            pygame.display.update()  # Update after every change

    def insert_pieces(self):
        "Draws the chess pieces to the board"
        raise NotImplementedError
    
    def show_path(self, path: list):
        "Puts a glow in each of the contiguous cells listed in `path` to indicate a possible move"
        raise NotImplementedError
    
    def show_move(self, move):
        "Saves a move so that it gets picked up by the pygame loop and shown on the display"
        self.current_move = move

# For testing:
if __name__=="__main__":
    func = lambda row, col: 1 if abs(row-col) %2 == 0 else 0
    matrix = [[func(i, j) for j in range(8)] for i in range(8)]
    Gui(matrix)
