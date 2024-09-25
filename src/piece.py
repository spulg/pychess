from typing import List, Tuple
from const import *
import os

from src.board import Board


class Piece:

    @staticmethod
    def compute_valid_moves(board: Board, row: int, col: int):
        """
        Given row and column, computes all valid moves the occupying piece can make.
        """
        valid_moves = []
        piece = board[row, col]
        color = Piece.get_color(piece)

        horizontal_vertical_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # up, down, right, left
        diagonal_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # up-right, up-left, down-right, down-left

        def empty_or_capture(x: int, y: int):
            return board[x, y] == NONE or Piece.get_color(board[x, y]) != color

        def slide_in_directions(directions):
            for dx, dy in directions:
                x, y = row, col
                while True:
                    x += dx
                    y += dy
                    if not Board.in_range((x, y)) or not empty_or_capture(x, y):
                        break
                    valid_moves.append((x, y))

        def horizontal_vertical_sliding_piece():
            slide_in_directions(horizontal_vertical_directions)

        def diagonal_sliding_piece():
            slide_in_directions(diagonal_directions)

        if piece == PAWN:
            direction = -1 if color == WHITE else 1

            # Normal move: 1 square forward if empty
            if Board.in_range((row + direction, col)) and board[row + direction, col] == NONE:
                valid_moves.append((row + direction, col))
                # Initial 2-square move if both squares are empty
                if (row == 6 and color == WHITE) or (row == 1 and color == BLACK):
                    if board[row + 2 * direction, col] == NONE:
                        valid_moves.append((row + 2 * direction, col))

            # Capture diagonally
            for dx in [-1, 1]:
                if Board.in_range((row + direction, col + dx)) and board[row + direction, col + dx] != NONE:
                    if Piece.get_color(board[row + direction, col + dx]) != color:
                        valid_moves.append((row + direction, col + dx))
        elif piece == ROOK:
            horizontal_vertical_sliding_piece()
        elif piece == BISHOP:
            diagonal_sliding_piece()
        elif piece == KNIGHT:
            possible_moves = [(row + 2, col + 1), (row + 2, col - 1), (row - 2, col + 1), (row - 2, col - 1),
                              (row + 1, col + 2), (row + 1, col - 2), (row - 1, col + 2), (row - 1, col - 2)]

            valid_moves = [(x, y) for (x, y) in possible_moves if Board.in_range((x, y)) and empty_or_capture(x, y)]
        elif piece == QUEEN:
            horizontal_vertical_sliding_piece()
            diagonal_sliding_piece()
        elif piece == KING:
            pass
        elif piece == NONE:
            pass

        return valid_moves

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
