from chess.chess_pieces import Piece, King, Queen, Rook, Knight, Bishop, Pawn
from chess.chess_constants import PIECES


class ChessBoard:
    def __init__(self):
        self.board = [[PIECES['EMPTY_TILE'] for _ in range(8)] for _ in range(8)]
        self.player = 0
    
    def __repr__(self):
        return self.board
    
    def _place_pieces(self, pieces: list[tuple[Piece, int, int, int]]):
        for piece in pieces:
            Class, player, i, j = piece
            self.board[i][j] = Class(player, i, j)
    
    def initialize_board(self) -> None:
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

    def display_board(self) -> None:
        for i in range(8):
            print(f'{8 - i} ', end='')
            for j in range(8):
                print(f'{self.board[i][j]} ', end='')
            print('')
        print('  A B C D E F G H')

    def _get_coordinate(self, msg: str='Enter tile: ', allow_exit: bool=False) -> tuple[int] | None:
        while True:
            tile = input(msg)
            if allow_exit and tile == '-1': return None, None
            if len(tile) == 2:
                try: tile_x = int(tile[1])
                except ValueError: tile_x = -1
                if 65 <= ord(tile[0]) <= 72 and 1 <= tile_x <= 8:
                    break
            print('Invalid tile entered, try again!')
        return (8 - tile_x, ord(tile[0]) - 65)

    # def move_piece(self) -> None:
    #     print(f"It is {('white' if self.player == 0 else 'black')}'s turn to move.")
    #     while True:
    #         y, x = chess._get_coordinate(msg='Enter your piece tile to move: ')
    #         if self.board[y][x] != PIECES['EMPTY_TILE'] and self.board[y][x].player == self.player:
    #             while True:
    #                 valid_moves = self.board[y][x].get_valid_moves(self.player, self.board)
    #                 print(f'valid moves: {valid_moves}')
    #                 print(f'valid moves: {"".join(chr(move[1] + 65) + str(8 - move[0]) + " " for move in valid_moves)}')
    #                 p, q = chess._get_coordinate(msg='Enter valid tile to move this piece: (type -1 to cancel) ', allow_exit=True)
    #                 if not p: break
    #                 if (p, q) in valid_moves:
    #                     chess.board[p][q] = chess.board[y][x]
    #                     chess.board[y][x] = PIECES['EMPTY_TILE']
    #                     chess.board[p][q].y = p
    #                     chess.board[p][q].x = q
    #                     self.player = (self.player + 1) % 2
    #                     return
    #                 print('Invalid tile selected, try again!')
    #         print('Invalid piece selected, try again!')

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


if __name__ == "__main__":
    chess = ChessBoard()
    chess.initialize_board()

    while True:
        chess.display_board()
        chess.move_piece()

'''
    TODO
    add winning
    forced move when king in check
    add castling feature
    add en passant
    add pawn promotion
'''
