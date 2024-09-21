from const import *
import os

class Piece:
    @staticmethod
    def get_color(piece: int) -> int:
        return piece & 0b11000

    @staticmethod
    def get_piece_type(piece: int) -> int:
        return piece & 0b00111

    @staticmethod
    def get_texture_path(piece: int, size=80) -> str:
        return os.path.join(
            f"../assets/images/imgs-{size}px/{names[Piece.get_color(piece)]}_{names[Piece.get_piece_type(piece)]}.png"
        )
