import numpy as np
from const import *


class Board:
    def __init__(self, fen: str = STARTING_FEN):
        self.__squares = np.zeros((ROWS, COLS), dtype="uint8")
        self.playerToMove = None
        self.castling_availability = None
        self.en_passant_target_sqaure = None
        self.halfmove_clock = None
        self.fullmove_clock = None
        self.fen_to_board(fen)
        self.valid_moves = []

    def __getitem__(self, pos: (int, int)):
        row, col = pos
        return self.__squares[col, row]

    def __setitem__(self, pos: (int, int), piece) -> None:
        row, col = pos
        self.__squares[col, row] = piece

    def fen_to_board(self, fen: str):
        char_to_piece = {
            'k': KING,
            'p': PAWN,
            'n': KNIGHT,
            'b': BISHOP,
            'r': ROOK,
            'q': QUEEN
        }

        _fen = fen.split(' ')
        fen_board = _fen[0]
        self.playerToMove = WHITE if _fen[1] == 'w' else BLACK
        self.castling_availability = _fen[2]
        self.en_passant_target_sqaure = (ord(_fen[3][0]) - 96, COLS - 1 - int(_fen[3][1])) if _fen[3] != '-' else None # e3 to (4, 5)
        self.halfmove_clock = int(_fen[4])
        self.fullmove_clock = int(_fen[5])

        row = 0
        col = 0
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
                    self[row, col] = color | piece
                    row += 1

    def move_piece(self, old_row: int, old_col: int, new_row: int, new_col: int) -> bool:
        capture = False
        if self[new_row, new_col] != NONE:
            capture = True
        self[new_row, new_col] = self[old_row, old_col]
        self[old_row, old_col] = NONE
        return capture

    def compute_valid_moves(self) -> None:
        """
        Stores valid moves in class variable
        """
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                target_piece = self[row, col]
                if target_piece == NONE:
                    moves.append((row, col))
        self.valid_moves = moves

    @staticmethod
    def in_range(*args):
        for (row, col) in args:
            return 0 <= row < ROWS and 0 <= col < COLS
