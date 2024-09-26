from typing import List, Tuple
from const import *
import os

class Piece:

    @staticmethod
    def get_piece_color(square) -> int:
        return square & 0b11000

    @staticmethod
    def get_piece_type(square) -> int:
        return square & 0b00111

    @staticmethod
    def get_opposite_color(square) -> int:
        return WHITE if square & 0b11000 == BLACK else BLACK

    @staticmethod
    def get_texture_path(piece, size=80) -> str:
        return os.path.join(
            f"assets/images/imgs-{size}px/{names[Piece.get_piece_color(piece)]}_{names[Piece.get_piece_type(piece)]}.png"
        )
