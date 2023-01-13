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
    Utility function to get list of pieces correspond to a given player and piece name.
    '''
    def _get_pieces(self, player: int, name: str) -> list[type]:
        ret_list = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece != PIECES['EMPTY_TILE']:
                    if piece.name == name and piece.player == player:
                        ret_list.append(piece)
        return ret_list

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
        self.turn = 1
    
    '''
    Change to next player, increment turn every time both players move.
    '''
    def _next_player(self):
        if self.player == 1: self.turn += 1
        self.player = (self.player + 1) % 2

    '''
    Return True if you select your own piece, otherwise false.
    '''
    def allow_select_tile(self, i, j) -> bool:
        return (self.board[i][j] != PIECES['EMPTY_TILE'] and
            self.board[i][j].player == self.player)
    
    '''
    Simulate one move ahead. Return True if king is not checked after
    making that move, otherwise False.
    '''
    def _simulate_move_safe(self, i, j, p, q):
        temp = self.board[p][q]
        self.move_piece(i, j, p, q, next=False)
        checked = self.is_king_checked()[0]
        self.move_piece(p, q, i, j, next=False)
        self.board[p][q] = temp
        return not checked

    '''
    Given a tile that you are allowed to move, return 2d list of booleans,
    True means you can move move the piece here, otherwise False.
    '''
    def get_valid_moves_list(self, i, j) -> list[list[bool]]:

        pawns = self._get_pieces(self.player, 'PAWN')
        for pawn in pawns:
            print(pawn.allow_en_passant, end='')
        print('')

        pawns = self._get_pieces((self.player + 1) % 2, 'PAWN')
        for pawn in pawns:
            print(pawn.allow_en_passant, end='')
        print('')

        ret_list = [[False for _ in range(8)] for _ in range(8)]
        moves = self.board[i][j].get_valid_moves(self.board)
        for move in moves:
            if self._simulate_move_safe(i, j, move[0], move[1]):
                ret_list[move[0]][move[1]] = True
        return ret_list
    
    '''
    Move a piece from position (i, j) to (p, q).
    Does not check if it is valid, so enforce validity before calling this.
    '''
    def move_piece(self, i: int, j: int, p: int, q: int, next: bool=True) -> None:
        pawns = self._get_pieces(self.player, 'PAWN')
        for pawn in pawns: pawn.allow_en_passant = False
        self.board[p][q] = self.board[i][j]
        self.board[i][j] = PIECES['EMPTY_TILE']
        self.board[p][q].move(p, q)
        if next: self._next_player()
    
    '''
    Check whether the king is on check or not at the current board state.
    Return boolean (True if on check, False otherwise) and king's position.
    '''
    def is_king_checked(self) -> tuple[bool, int, int]:
        king = self._get_pieces(self.player, 'KING')[0]
        return king.is_checked(self.board), king.y, king.x

'''
    TODO
    add winning
    add castling feature
    add en passant
    add pawn promotion
'''
