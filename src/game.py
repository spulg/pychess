import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from src.piece import Piece


class Game:
    @staticmethod
    def create_surface():
        surface = pygame.Surface((SQSIZE * ROWS, SQSIZE * COLS))

        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (235, 209, 166)  # light brown
                else:
                    color = (165, 117, 80)  # dark brown

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
                piece = self.board[row, col]
                if piece != NONE:
                    texture_path = TEXTURE_PATHS[piece]
                    img = pygame.image.load(texture_path)
                    img_center = row * SQSIZE + SQSIZE // 2, col * SQSIZE + SQSIZE // 2
                    texture_rect = img.get_rect(center=img_center)
                    screen.blit(img, texture_rect)

    def show_valid_moves(self, screen, row, col):
        valid_moves = Piece.compute_valid_moves(self.board, row, col)
        for x, y in valid_moves:
            center_x = x * SQSIZE + SQSIZE // 2
            center_y = y * SQSIZE + SQSIZE // 2
            pygame.draw.circle(screen, (0, 0, 255), (center_x, center_y), SQSIZE // 5)

    @staticmethod
    def show_selector(screen, row, col):
        rect = (row * SQSIZE, col * SQSIZE, SQSIZE, SQSIZE)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)

    def play_sound(self, captured=False):
        # https://github.com/AlejoG10/python-chess-ai-yt/blob/master/src/game.py
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

