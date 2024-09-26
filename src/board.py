import numpy as np
from const import *
from piece import Piece

class Board:
    def __init__(self, fen: str = STARTING_FEN):
        self.__squares = np.zeros((ROWS, COLS), dtype="uint8")
        self.playerToMove = None
        self.castling_availability = None
        self.en_passant_target_square = None
        self.halfmove_clock = None
        self.fullmove_clock = None
        self.fen_to_self(fen)

    def __getitem__(self, pos: (int, int)):
        row, col = pos
        return self.__squares[col, row]

    def __setitem__(self, pos: (int, int), piece) -> None:
        row, col = pos
        self.__squares[col, row] = piece

    def fen_to_self(self, fen: str):
        char_to_piece = {
            'k': KING,
            'p': PAWN,
            'n': KNIGHT,
            'b': BISHOP,
            'r': ROOK,
            'q': QUEEN
        }

        _fen = fen.split(' ')
        fen_self = _fen[0]
        self.playerToMove = WHITE if _fen[1] == 'w' else BLACK
        self.castling_availability = _fen[2]
        self.en_passant_target_square = (ord(_fen[3][0]) - 96, COLS - 1 - int(_fen[3][1])) if _fen[3] != '-' else None # e3 to (4, 5)
        self.halfmove_clock = int(_fen[4])
        self.fullmove_clock = int(_fen[5])

        row = 0
        col = 0
        for symbol in fen_self:
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

    def is_empty(self, row: int, col: int) -> bool:
        return self[row, col] == NONE

    def move_piece(self, old_row: int, old_col: int, new_row: int, new_col: int) -> bool:
        piece = Piece.get_piece_type(self[old_row, old_col])

        if piece == PAWN and (new_row, new_col) == self.en_passant_target_square:
            capture = True
            capture_col = new_col + 1 if Piece.get_piece_color(self[old_row, old_col]) == WHITE else new_col - 1
            self[new_row, capture_col] = NONE

        # regular captures
        elif self[new_row, new_col] != NONE:
            capture = True
        else:
            capture = False

        # en passant capture
        if piece == PAWN and abs(new_col - old_col) == 2:
            if Piece.get_piece_color(self[old_row, old_col]) == WHITE:
                self.en_passant_target_square = (new_row, new_col + 1)
            else:
                self.en_passant_target_square = (new_row, new_col - 1)
        else:
            self.en_passant_target_square = None

        self[new_row, new_col] = self[old_row, old_col]
        self[old_row, old_col] = NONE

        return capture

    def compute_valid_moves(self, row: int, col: int):
        """
        Given row and column, computes all valid moves the occupying piece can make.
        """
        valid_moves = []
        piece = Piece.get_piece_type(self[row, col])
        color = Piece.get_piece_color(self[row, col])

        horizontal_vertical_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # up, down, right, left
        diagonal_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # up-right, up-left, down-right, down-left

        def empty_or_capture(x: int, y: int) -> bool:
            return self[x, y] == NONE or Piece.get_piece_color(self[x, y]) != color

        def contains_opponent_piece(x: int, y: int) -> bool:
            if Piece.get_piece_color(self[x, y]) == color or self[x, y] == NONE:
                return False
            return True

        def contains_allied_piece(x: int, y: int) -> bool:
            return Piece.get_piece_color(self[x, y]) == color

        def slide_in_directions(directions):
            for dx, dy in directions:
                x, y = row, col
                while True:
                    x += dx
                    y += dy
                    if not self.in_range(x, y) or contains_allied_piece(x, y):
                        break
                    if contains_opponent_piece(x, y):
                        valid_moves.append((x, y))
                        break
                    valid_moves.append((x, y))

        def horizontal_vertical_sliding_piece():
            slide_in_directions(horizontal_vertical_directions)

        def diagonal_sliding_piece():
            slide_in_directions(diagonal_directions)

        if piece == PAWN:
            dy = -1 if color == WHITE else 1

            # Normal move: 1 square forward if empty
            if self.in_range(row, col + dy) and self[row, col + dy] == NONE:
                valid_moves.append((row, col + dy))

                # Initial 2-square move if both squares are empty
                if (col == 6 and color == WHITE) or (col == 1 and color == BLACK):
                    if self[row, col + 2 * dy] == NONE:
                        valid_moves.append((row, col + 2 * dy))

            for dx in [-1, 1]:
                if self.in_range(row + dx, col + dy):
                    target_piece = self[row + dx, col + dy]

                    # diagonal capture
                    if target_piece != NONE and Piece.get_piece_color(target_piece) != color:
                        valid_moves.append((row + dx, col + dy))

                    # en passant capture
                    if self.en_passant_target_square == (row + dx, col + dy):
                        valid_moves.append((row + dx, col + dy))
        elif piece == ROOK:
            horizontal_vertical_sliding_piece()
        elif piece == BISHOP:
            diagonal_sliding_piece()
        elif piece == KNIGHT:
            possible_moves = [(row + 2, col + 1), (row + 2, col - 1), (row - 2, col + 1), (row - 2, col - 1),
                              (row + 1, col + 2), (row + 1, col - 2), (row - 1, col + 2), (row - 1, col - 2)]

            valid_moves = [(x, y) for (x, y) in possible_moves if self.in_range(x, y) and empty_or_capture(x, y)]
        elif piece == QUEEN:
            horizontal_vertical_sliding_piece()
            diagonal_sliding_piece()
        elif piece == KING:
            king_moves = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1),
                          (row + 1, col + 1), (row + 1, col - 1), (row - 1, col + 1), (row - 1, col - 1)]

            valid_moves = [(x, y) for (x, y) in king_moves if self.in_range(x, y) and empty_or_capture(x, y)]
        elif piece == NONE:
            pass

        return valid_moves

    @staticmethod
    def in_range(row, col):
        return 0 <= row < ROWS and 0 <= col < COLS
