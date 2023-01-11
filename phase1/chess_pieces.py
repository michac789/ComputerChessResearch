# import sys; import os;
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

from constants import PIECES


class Piece:
    def __init__(self, player: int, x: int, y: int):
        self.player = player
        self.x = x
        self.y = y
    
    def __str__(self):
        return PIECES[('WHITE' if self.player == 0 else 'BLACK') + f'_{self.name}']


class King(Piece):
    name = 'KING'


class Queen(Piece):
    name = 'QUEEN'


class Rook(Piece):
    name = 'ROOK'


class Knight(Piece):
    name = 'KNIGHT'


class Bishop(Piece):
    name = 'BISHOP'


class Pawn(Piece):
    name = 'PAWN'


if __name__ == '__main__':
    x = King(0, 1, 1)
    print(x)
    print(x.player)
    print(x.x)
    print(x.y)
    print('hello \u25FB')
