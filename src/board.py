import numpy as np
from const import *


class Board:



    def __init__(self):
        self.squares = np.zeros((ROWS, COLS), dtype="uint8")
        self.__add_starting_pieces()
        self.valid_moves = []

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

    def move_piece(self, old_col, old_row, new_col, new_row) -> bool:
        capture = False
        if self.squares[new_col][new_row] != NONE:
            capture = True
        self.squares[new_col][new_row] = self.squares[old_col][old_row]
        self.squares[old_col][old_row] = NONE
        return capture

    def compute_valid_moves(self, piece, row, col) -> None:
        """
        Stores valid moves in class variable
        """
        moves = []
        def knight_moves():
            _moves = [
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row + 1, col + 2),
                (row + 1, col - 2),
                (row - 1, col + 2),
                (row - 1, col - 2)
            ]
            return filter(Board.in_range, _moves)

        if piece == PAWN:
            pass
        elif piece == KNIGHT:
            pass
        elif piece == ROOK:
            pass
        elif piece == QUEEN:
            pass
        elif piece == KING:
            pass

        for col in range(ROWS):
            for row in range(COLS):
                target_piece = self.squares[col][row]
                if target_piece == NONE:
                    moves.append((col, row))
        self.valid_moves = moves

    @staticmethod
    def in_range(*args):
        for (row, col) in args:
            return 0 <= row < ROWS and 0 <= col < COLS
