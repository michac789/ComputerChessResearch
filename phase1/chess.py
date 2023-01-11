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
        for p in range(2):
            row = 7 - 7 * p
            row2 = 6 - 5 * p
            self.place_pieces([
                (Rook, p, row, 0),
                (Knight, p, row, 1),
                (Bishop, p, row, 2),
                (Queen, p, row, 3),
                (King, p, row, 4),
                (Bishop, p, row, 5),
                (Knight, p, row, 6),
                (Rook, p, row, 7),
                *[(Pawn, p, row2, j) for j in range(8)],
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
    chess.board[4][1] = Queen(0, 4, 1)
    a = chess.board[4][1].get_valid_moves(0, chess.board)
    print(a)
    chess.display_board()
    print("Hello World ♟")
    print('\u25FB \u265F')
