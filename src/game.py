import pygame
from const import *
from board import Board
from dragger import Dragger
from piece import Piece
from config import Config


class Game:
    @staticmethod
    def create_surface():
        surface = pygame.Surface((SQSIZE * ROWS, SQSIZE * COLS))

        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)  # light green
                else:
                    color = (119, 154, 88)  # dark green

                rect = pygame.Rect(row * SQSIZE, col * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
        return surface

    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    def show_pieces(self, screen):
        for col in range(COLS):
            for row in range(COLS):
                piece = self.board.squares[col][row]
                if piece != NONE:
                    texture_path = TEXTURE_PATHS[piece]
                    img = pygame.image.load(texture_path)
                    img_center = row * SQSIZE + SQSIZE // 2, col * SQSIZE + SQSIZE // 2
                    texture_rect = img.get_rect(center=img_center)
                    screen.blit(img, texture_rect)

    def show_valid_moves(self, screen, piece, row, col):
        self.board.compute_valid_moves(piece, row, col)
        for move_col, move_row in self.board.valid_moves:
            center_x = move_row * SQSIZE + SQSIZE // 2
            center_y = move_col * SQSIZE + SQSIZE // 2
            pygame.draw.circle(screen, (0, 0, 255), (center_x, center_y), SQSIZE // 5)

    def show_selector(self, screen, row, col):
        rect = (row * SQSIZE, col * SQSIZE, SQSIZE, SQSIZE)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)

    def play_sound(self, captured=False):
        # https://github.com/AlejoG10/python-chess-ai-yt/blob/master/src/game.py
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

