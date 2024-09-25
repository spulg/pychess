import os

WIDTH = 800
HEIGHT = WIDTH

ROWS = 8
COLS = ROWS

SQSIZE = WIDTH // ROWS

NONE = 0
KING = 1
PAWN = 2
KNIGHT = 3
BISHOP = 4
ROOK = 5
QUEEN = 6

WHITE = 8
BLACK = 16

names = {
    0: "none",
    1: "king",
    2: "pawn",
    3: "knight",
    4: "bishop",
    5: "rook",
    6: "queen",
    8: "white",
    16: "black"
}

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# castling availability
WHITE_KINGSIDE = 'K'
WHITE_QUEENSIDE = 'Q'
BLACK_KINGSIDE = 'k'
BLACK_QUEENSIDE = 'q'


TEXTURE_PATHS = dict()


def init_textures():
    for color in [WHITE, BLACK]:
        for piece_type in range(KING, QUEEN + 1):
            piece = color | piece_type
            TEXTURE_PATHS[piece] = os.path.join(
                f"../assets/images/imgs-{80}px/{names[color]}_{names[piece_type]}.png")


init_textures()
