import pygame
from const import *


class Dragger:
    def __init__(self):
        self.img = None
        self.dragging = False
        self.piece = NONE
        self.initial_row = 0
        self.initial_col = 0

    def save_initial(self, pos):
        self.initial_row = pos[0]
        self.initial_col = pos[1]

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True
        self.img = pygame.image.load(TEXTURE_PATHS[piece])

    def undrag_piece(self):
        self.dragging = False
        self.piece = NONE
        self.img = None
