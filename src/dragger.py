import pygame
from const import *
from piece import Piece


class Dragger:
    def __init__(self):
        self.dragging = False
        self.piece = NONE
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
        self.img = None  # Store the image of the piece being dragged

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True
        # Load the piece image once and reuse it
        self.img = pygame.image.load(Piece.get_texture_path(piece))

    def undrag_piece(self):
        self.dragging = False
        self.piece = NONE
        self.img = None

    def update_blit(self, surface):
        if self.img:
            img_rect = self.img.get_rect(center=(self.mouseX, self.mouseY))
            surface.blit(self.img, img_rect)
