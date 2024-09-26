from typing import Tuple

import pygame
import sys
from const import *
from game import Game
from piece import Piece

class Main:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board_surface = Game.create_surface()
        self.game = Game()
        self.clock = pygame.time.Clock()

    @staticmethod
    def get_mouse_square():
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_row = int(mouse_pos[0] / SQSIZE)
        mouse_col = int(mouse_pos[1] / SQSIZE)
        return mouse_row, mouse_col

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        selected_square: Tuple[int, int] = (-1, -1)
        while True:
            current_mouse_square: Tuple[int, int] = self.get_mouse_square()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEMOTION:
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if dragger.dragging:
                        if current_mouse_square in board.compute_valid_moves(dragger.initial_row, dragger.initial_col):
                            if board[current_mouse_square] == WHITE | KING or board[current_mouse_square] == BLACK | KING:
                                game.play_sound(WIN)
                            captured = board.move_piece(dragger.initial_row, dragger.initial_col, current_mouse_square[0], current_mouse_square[1])
                            if captured:
                                game.play_sound(CAPTURE)
                            else:
                                game.play_sound(MOVE)
                        elif Piece.get_piece_color(board[current_mouse_square]) != Piece.get_piece_color(board[dragger.initial_row, dragger.initial_col]):
                            game.play_sound(ERROR)
                        dragger.undrag_piece()
                    else:
                        piece = board[current_mouse_square]
                        if piece != NONE:
                            dragger.save_initial(current_mouse_square)
                            dragger.drag_piece(piece)
                            selected_square = current_mouse_square

                elif event.type == pygame.MOUSEBUTTONUP:
                    pass
                else:
                    pass

            screen.blit(self.board_surface, (0, 0))
            game.show_pieces(screen)
            game.show_selector(screen, current_mouse_square[0], current_mouse_square[1])

            if dragger.dragging:
                game.show_valid_moves(screen, dragger.initial_row, dragger.initial_col)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    main = Main()
    main.mainloop()
