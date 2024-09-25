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

        while True:
            mouse_row, mouse_col = self.get_mouse_square()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEMOTION:
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if dragger.dragging:
                        if (mouse_row, mouse_col) in Piece.compute_valid_moves(board, dragger.initial_row, dragger.initial_col):
                            captured = board.move_piece(dragger.initial_row, dragger.initial_col, mouse_row, mouse_col)
                            game.play_sound(captured)
                            dragger.undrag_piece()
                    else:
                        mouse_row, mouse_col = self.get_mouse_square()
                        piece = board[mouse_row, mouse_col]
                        if piece != NONE:
                            dragger.save_initial((mouse_row, mouse_col))
                            dragger.drag_piece(piece)

                elif event.type == pygame.MOUSEBUTTONUP:
                    pass
                else:
                    pass

            screen.blit(self.board_surface, (0, 0))
            game.show_pieces(screen)
            game.show_selector(screen, mouse_row, mouse_col)

            if dragger.dragging:
                game.show_valid_moves(screen, dragger.initial_row, dragger.initial_col)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    main = Main()
    main.mainloop()
