import pygame
import sys
from const import *
from game import Game


class Main:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board_surface = Game.create_surface()
        self.game = Game()
        self.clock = pygame.time.Clock()

    def get_mouse_square(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_row = int(mouse_pos[0] / SQSIZE)
        mouse_col = int(mouse_pos[1] / SQSIZE)
        return mouse_col, mouse_row

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:
            mouse_col, mouse_row = self.get_mouse_square()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEMOTION:
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if dragger.dragging:
                        if (mouse_col, mouse_row) in board.valid_moves:
                            captured = board.move_piece(dragger.initial_col, dragger.initial_row, mouse_col, mouse_row)
                            game.play_sound(captured)
                            dragger.undrag_piece()
                    else:
                        mouse_col, mouse_row = self.get_mouse_square()
                        piece = board.squares[mouse_col][mouse_row]
                        if piece != NONE:
                            dragger.save_initial((mouse_col, mouse_row))
                            dragger.drag_piece(piece)
                elif event.type == pygame.MOUSEBUTTONUP:
                    pass
                else:
                    pass

            screen.blit(self.board_surface, (0, 0))
            game.show_pieces(screen)
            game.show_selector(screen, mouse_row, mouse_col)

            if dragger.dragging:
                game.show_valid_moves(screen, dragger.piece, dragger.initial_col, dragger.initial_row)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    main = Main()
    main.mainloop()
