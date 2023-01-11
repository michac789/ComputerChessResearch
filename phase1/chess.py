from typing import Tuple
from chess_pieces import Piece, King, Queen, Rook, Knight, Bishop, Pawn
from constants import PIECES


class ChessBoard:
    def __init__(self):
        self.board = [[PIECES['EMPTY_TILE'] for _ in range(8)] for _ in range(8)]
    
    def place_pieces(self, pieces: list[Tuple[Piece, int, int, int]]):
        for piece in pieces:
            Class, player, i, j = piece
            self.board[i][j] = Class(player, i, j)
    
    def initialize_board(self):
        for i in range(2):
            row = 7 - 7 * i
            row2 = 6 - 5 * i
            self.place_pieces([
                (Rook, i, row, 0),
                (Knight, i, row, 1),
                (Bishop, i, row, 2),
                (Queen, i, row, 3),
                (King, i, row, 4),
                (Bishop, i, row, 5),
                (Knight, i, row, 6),
                (Rook, i, row, 7),
                *[(Pawn, i, row2, j) for j in range(8)],
            ])

    def display_board(self):
        for i in range(8):
            for j in range(8):
                print(f'{self.board[i][j]} ', end='')
            print('')
        print('')

if __name__ == "__main__":
    chess = ChessBoard()
    chess.initialize_board()
    chess.display_board()
    print("Hello World ♟")
    print('\u25FB \u265F')
