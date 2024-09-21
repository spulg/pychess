import numpy as np
from const import *


class Board:

    @staticmethod
    def in_range(*args):
        for (row, col) in args:
            return 0 <= row < ROWS and 0 <= col < COLS

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS), dtype="uint8")
        self.__add_starting_pieces()

    def fen_to_board(self, fen: str):
        char_to_piece = {
            'k': KING,
            'p': PAWN,
            'n': KNIGHT,
            'b': BISHOP,
            'r': ROOK,
            'q': QUEEN
        }

        row = 0
        col = 0
        fen_board = fen.split(' ')[0]
        for symbol in fen_board:
            if symbol == '/':
                row = 0
                col += 1
            else:
                if symbol.isdigit():
                    row += int(symbol)
                else:
                    color = WHITE if symbol.isupper() else BLACK
                    piece = char_to_piece[symbol.lower()]
                    self.squares[col][row] = color | piece
                    row += 1

    def __add_starting_pieces(self):
        self.fen_to_board(STARTING_FEN)

    def valid_moves(self, piece, row, col):
        def knight_moves():
            moves = [
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row + 1, col + 2),
                (row + 1, col - 2),
                (row - 1, col + 2),
                (row - 1, col - 2)
            ]
            return filter(Board.in_range, moves)

        if piece == PAWN:
            pass
        elif piece == KNIGHT:
            return knight_moves()
        elif piece == ROOK:
            pass
        elif piece == QUEEN:
            pass
        elif piece == KING:
            pass
