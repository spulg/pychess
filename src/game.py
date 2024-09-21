import pygame
from const import *
from board import Board
from dragger import Dragger
from piece import Piece


class Game:

    @staticmethod
    def show_bg(surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)  # light green
                else:
                    color = (119, 154, 88)  # dark green

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.squares[row][col]
                if piece != NONE:
                    texture_path = Piece.get_texture_path(piece)
                    img = pygame.image.load(texture_path)
                    img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                    texture_rect = img.get_rect(center=img_center)
                    surface.blit(img, texture_rect)
