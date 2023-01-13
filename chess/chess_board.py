from copy import deepcopy
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
            
            # FOR TESTING ONLY - TODO remove this when done
            # self._place_pieces([
            #     (Rook, player, row, 0),
            #     (Queen, player, row, 3),
            #     (King, player, row, 4),
            #     *[(Pawn, player, row2, j) for j in range(0)],
            # ])

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
        cb = deepcopy(self)
        cb.move_piece(i, j, p, q)
        cb.player = (cb.player + 1) % 2
        return not cb.is_king_checked()[0]

    '''
    Given a tile that you are allowed to move, return 2d list of booleans,
    True means you can move move the piece here, otherwise False.
    '''
    def get_valid_moves_list(self, i, j) -> tuple[list[list[bool]], bool]:
        ret_list = [[False for _ in range(8)] for _ in range(8)]
        available_move = False
        moves = self.board[i][j].get_valid_moves(self.board)
        for move in moves:
            if self._simulate_move_safe(i, j, move[0], move[1]):
                ret_list[move[0]][move[1]] = True
                available_move = True
        return ret_list, available_move
    
    '''
    Move a piece from position (i, j) to (p, q).
    Reset all own pawns 'allow_en_passant' attribute to False.
    Does not check if it is valid, so enforce validity before calling this.
    '''
    def move_piece(self, i: int, j: int, p: int, q: int) -> None:
        pawns = self._get_pieces(self.player, 'PAWN')
        for pawn in pawns: pawn.allow_en_passant = False
        self.board[i][j].move(p, q, self.board)
        if next: self._next_player()
    
    '''
    Check whether the king is on check or not at the current board state.
    Return boolean (True if on check, False otherwise) and king's position.
    '''
    def is_king_checked(self) -> tuple[bool, int, int]:
        king = self._get_pieces(self.player, 'KING')[0]
        return king.is_checked(self.board), king.y, king.x
    
    '''
    Return True if there is any available move, otherwise False.
    '''
    def _is_available_move(self) -> bool:
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece != PIECES['EMPTY_TILE'] and piece.player == self.player:
                    _, avail_move = self.get_valid_moves_list(i, j)
                    if avail_move: return True
        return False
    
    '''
    Check status of current game. Return -1 if game is still going.
    If ended, return 0 (white wins) or 1 (black wins) or 2 (draw).
    '''
    def check_ended(self) -> int:
        if not self._is_available_move():
            return (self.player + 1) % 2 if self.is_king_checked()[0] else 2
        return -1

'''
    TODO
    add castling feature
    draw after 3 consecutive repeated moves
'''
