from chess.chess_constants import PIECES


_DIAGONAL_MOVES = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
_SIDE_MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class Piece:
    name = None
    _valid_directions = []
    _infinite_range = True

    def __init__(self, player: int, y: int, x: int):
        self.player = player
        self.y = y
        self.x = x
    
    def __str__(self):
        return PIECES[('WHITE' if self.player == 0 else 'BLACK') + f'_{self.name}']

    def _valid_tile(self, player: int, i: int, j: int, board: list[list]) -> bool:
        return (
            0 <= i <= 7 and 0 <= j <= 7 and
            (
                board[i][j] == PIECES['EMPTY_TILE'] or
                board[i][j].player != player
            )
        )
    
    def get_valid_moves(self, player: int, board: list[list]) -> list[tuple]:
        valid_moves = []
        for p, q in self._valid_directions:
            i, j = self.y, self.x
            i, j = i + p, j + q
            if self._infinite_range:
                while self._valid_tile(player, i, j, board):
                    valid_moves.append((i, j))
                    if board[i][j] != PIECES['EMPTY_TILE']: break
                    i, j = i + p, j + q
            elif self._valid_tile(player, i, j, board):
                valid_moves.append((i, j))
        return valid_moves


class King(Piece):
    name = 'KING'
    _valid_directions = _DIAGONAL_MOVES + _SIDE_MOVES
    _infinite_range = False


class Queen(Piece):
    name = 'QUEEN'
    _valid_directions = _DIAGONAL_MOVES + _SIDE_MOVES
    _infinite_range = True


class Rook(Piece):
    name = 'ROOK'
    _valid_directions = _SIDE_MOVES
    _infinite_range = True


class Knight(Piece):
    name = 'KNIGHT'
    _valid_directions = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
    _infinite_range = False


class Bishop(Piece):
    name = 'BISHOP'
    _valid_directions = _DIAGONAL_MOVES
    _infinite_range = True


class Pawn(Piece):
    name = 'PAWN'

    def get_valid_moves(self, player: int, board: list[list]) -> list[tuple]:
        valid_moves = []
        dy = (-1 if self.player == 0 else 1)
        i, j = self.y, self.x
        for p, q in [(dy, -1), (dy, 1)]:
            if self._valid_tile(player, i + p, j + q, board) and board[i + p][j + q] != PIECES['EMPTY_TILE']:
                valid_moves.append((i + p, j + q))
        if self._valid_tile(player, i + 1 * dy, j, board) and board[i + 1 * dy][j] == PIECES['EMPTY_TILE']:
            valid_moves.append((i + 1 * dy, j))
        if (3.5 - 2.5 * dy) == i and self._valid_tile(player, i + 2 * dy, j, board) and board[i + 2 * dy][j] == PIECES['EMPTY_TILE']:
            valid_moves.append((i + 2 * dy, j))
        return valid_moves
