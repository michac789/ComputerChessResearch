from chess.chess_pieces import Piece, King, Queen, Rook, Knight, Bishop, Pawn
from chess.chess_constants import PIECES


class ChessBoard:
    def __init__(self):
        self.initialize_board()
    
    '''
    Utility function to place multiple pieces on the chess board.
    '''
    def _place_pieces(self, pieces: list[tuple[Piece, int, int, int]]):
        for piece in pieces:
            Class, player, i, j = piece
            self.board[i][j] = Class(player, i, j)

    '''
    Setup starting position of chess board, white moves first.
    '''
    def initialize_board(self) -> None:
        self.board = [[PIECES['EMPTY_TILE'] for _ in range(8)] for _ in range(8)]
        for player in range(2):
            row = 7 - 7 * player
            row2 = 6 - 5 * player
            self._place_pieces([
                (Rook, player, row, 0),
                (Knight, player, row, 1),
                (Bishop, player, row, 2),
                (Queen, player, row, 3),
                (King, player, row, 4),
                (Bishop, player, row, 5),
                (Knight, player, row, 6),
                (Rook, player, row, 7),
                *[(Pawn, player, row2, j) for j in range(8)],
            ])
        self.player = 0

    '''
    Return True if you select your own piece, otherwise false.
    '''
    def allow_select_tile(self, i, j) -> bool:
        return (self.board[i][j] != PIECES['EMPTY_TILE'] and
            self.board[i][j].player == self.player)

    '''
    Given a tile that you are allowed to move, return 2d list of booleans,
    True means you can move move the piece here, otherwise False.
    '''
    def get_valid_moves_list(self, i, j) -> list[list[bool]]:
        ret_list = [[False for _ in range(8)] for _ in range(8)]
        moves = self.board[i][j].get_valid_moves(self.player, self.board)
        for move in moves:
            ret_list[move[0]][move[1]] = True
        return ret_list
    
    '''
    Move a piece from position (i, j) to (p, q).
    Does not check if it is valid, so enforce validity before calling this.
    '''
    def move_piece(self, i, j, p, q) -> None:
        self.board[p][q] = self.board[i][j]
        self.board[i][j] = PIECES['EMPTY_TILE']
        self.board[p][q].y = p
        self.board[p][q].x = q
        self.player = (self.player + 1) % 2

'''
    TODO
    add winning
    forced move when king in check
    add castling feature
    add en passant
    add pawn promotion
'''
