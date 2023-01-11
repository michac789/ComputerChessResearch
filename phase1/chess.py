from chess_pieces import Piece, King, Queen, Rook, Knight, Bishop, Pawn
from constants import PIECES


class ChessBoard:
    def __init__(self):
        self.board = [[PIECES['EMPTY_TILE'] for _ in range(8)] for _ in range(8)]
        self.player = 0
    
    def _place_pieces(self, pieces: list[tuple[Piece, int, int, int]]):
        for piece in pieces:
            Class, player, i, j = piece
            self.board[i][j] = Class(player, i, j)
    
    def initialize_board(self):
        for p in range(2):
            row = 7 - 7 * p
            row2 = 6 - 5 * p
            self._place_pieces([
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

    def move_piece(self):
        print(f"It is {('white' if self.player == 0 else 'black')}'s turn to move.")
        while True:
            y, x = chess._get_coordinate(msg='Enter your piece tile to move: ')
            if self.board[y][x] != PIECES['EMPTY_TILE'] and self.board[y][x].player == self.player:
                while True:
                    valid_moves = self.board[y][x].get_valid_moves(self.player, self.board)
                    print(f'valid moves: {valid_moves}')
                    print(f'valid moves: {"".join(chr(move[1] + 65) + str(8 - move[0]) + " " for move in valid_moves)}')
                    p, q = chess._get_coordinate(msg='Enter valid tile to move this piece: (type -1 to cancel) ', allow_exit=True)
                    if not p: break
                    if (p, q) in valid_moves:
                        chess.board[p][q] = chess.board[y][x]
                        chess.board[y][x] = PIECES['EMPTY_TILE']
                        self.player = (self.player + 1) % 2
                        return
                    print('Invalid tile selected, try again!')
            print('Invalid piece selected, try again!')


if __name__ == "__main__":
    chess = ChessBoard()
    chess.initialize_board()

    while True:
        chess.display_board()
        chess.move_piece()
