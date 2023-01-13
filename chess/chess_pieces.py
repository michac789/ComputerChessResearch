from chess.chess_constants import PIECES


_DIAGONAL_MOVES = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
_SIDE_MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
_KNIGHT_MOVES = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]


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

    def _valid_tile(self, i: int, j: int, board: list[list]) -> bool:
        return (
            0 <= i <= 7 and 0 <= j <= 7 and
            (
                board[i][j] == PIECES['EMPTY_TILE'] or
                board[i][j].player != self.player
            )
        )
    
    def move(self, p: int, q: int, board: list[list]) -> bool:
        capture = board[p][q] != PIECES['EMPTY_TILE']
        board[p][q] = self
        board[self.y][self.x] = PIECES['EMPTY_TILE']
        self.y = p
        self.x = q
        return capture
    
    def get_valid_moves(self, board: list[list]) -> list[tuple[int]]:
        valid_moves = []
        for p, q in self._valid_directions:
            i, j = self.y, self.x
            i, j = i + p, j + q
            if self._infinite_range:
                while self._valid_tile(i, j, board):
                    valid_moves.append((i, j))
                    if board[i][j] != PIECES['EMPTY_TILE']: break
                    i, j = i + p, j + q
            elif self._valid_tile(i, j, board):
                valid_moves.append((i, j))
        return valid_moves


class King(Piece):
    name = 'KING'
    _valid_directions = _DIAGONAL_MOVES + _SIDE_MOVES
    _infinite_range = False

    def __init__(self, player: int, y: int, x: int):
        super().__init__(player, y, x)
        self.has_moved = False
    
    def _move_castle_right(self, p: int, q: int, board: list[list]) -> None:
        board[p][q] = self
        board[p][q + 1].move(p, q - 1, board)
        board[p][q + 1] = PIECES['EMPTY_TILE']
        board[self.y][self.x] = PIECES['EMPTY_TILE']
        self.y = p
        self.x = q
    
    def _move_castle_left(self, p: int, q: int, board: list[list]) -> None:
        board[p][q] = self
        board[p][q - 2].move(p, q + 1, board)
        board[p][q - 2] = PIECES['EMPTY_TILE']
        board[self.y][self.x] = PIECES['EMPTY_TILE']
        self.y = p
        self.x = q

    def move(self, p: int, q: int, board: list[list]) -> bool:
        capture = False
        if not self.has_moved and p == self.y and q == 6:
            self._move_castle_right(p, q, board)
        elif not self.has_moved and p == self.y and q == 2:
            self._move_castle_left(p, q, board)
        else: capture = super().move(p, q, board)
        self.has_moved = True
        return capture
    
    def get_valid_moves(self, board: list[list]) -> list[tuple[int]]:
        valid_moves = super().get_valid_moves(board)
        # check for castling right
        if not self.has_moved and board[self.y][5] == PIECES['EMPTY_TILE'] and \
                board[self.y][6] == PIECES['EMPTY_TILE'] and board[self.y][7] != PIECES['EMPTY_TILE'] and \
                board[self.y][7].name == 'ROOK' and not board[self.y][7].has_moved:
            if not any([self.is_checked(board, (7, i)) for i in [4, 5, 6]]):
                valid_moves.append((self.y, 6))
        # check for castling left
        if not self.has_moved and board[self.y][3] == PIECES['EMPTY_TILE'] and board[self.y][2] == PIECES['EMPTY_TILE'] and \
                board[self.y][1] == PIECES['EMPTY_TILE'] and board[self.y][0] != PIECES['EMPTY_TILE'] and \
                board[self.y][0].name == 'ROOK' and not board[self.y][0].has_moved:
            if not any([self.is_checked(board, (7, i)) for i in [4, 3, 2]]):
                valid_moves.append((self.y, 2))
        return valid_moves

    def is_checked(self, board: list[list], alt_coor: tuple=None) -> bool:
        dy = (-1 if self.player == 0 else 1)
        PAWN_DIR = [(dy, -1), (dy, 1)]
        for DIRECTIONS, PIECE_LIST, INFINTE_RANGE in zip(
                [_DIAGONAL_MOVES, _SIDE_MOVES, _KNIGHT_MOVES, _DIAGONAL_MOVES, _SIDE_MOVES, PAWN_DIR],
                [['QUEEN', 'BISHOP'], ['QUEEN', 'ROOK'], ['KNIGHT'], ['KING'], ['KING'], ['PAWN']],
                [True, True, False, False, False, False]
                ):
            util_func = lambda: board[i][j] != PIECES['EMPTY_TILE'] and \
                                board[i][j].name in PIECE_LIST
            for p, q in DIRECTIONS:
                i, j = self.y, self.x
                if alt_coor: i, j = alt_coor
                i, j = i + p, j + q
                if INFINTE_RANGE:
                    while self._valid_tile(i, j, board):
                        if util_func():
                            return True
                        if board[i][j] != PIECES['EMPTY_TILE'] and \
                            board[i][j].player == (self.player + 1) % 2: break
                        i, j = i + p, j + q
                elif self._valid_tile(i, j, board) and util_func():
                    return True
        return False


class Queen(Piece):
    name = 'QUEEN'
    _valid_directions = _DIAGONAL_MOVES + _SIDE_MOVES
    _infinite_range = True


class Rook(Piece):
    name = 'ROOK'
    _valid_directions = _SIDE_MOVES
    _infinite_range = True

    def __init__(self, player: int, y: int, x: int):
        super().__init__(player, y, x)
        self.has_moved = False

    def move(self, p: int, q: int, board: list[list]) -> bool:
        self.has_moved = True
        return super().move(p, q, board)


class Knight(Piece):
    name = 'KNIGHT'
    _valid_directions = _KNIGHT_MOVES
    _infinite_range = False


class Bishop(Piece):
    name = 'BISHOP'
    _valid_directions = _DIAGONAL_MOVES
    _infinite_range = True


class Pawn(Piece):
    name = 'PAWN'

    def __init__(self, player: int, y: int, x: int):
        super().__init__(player, y, x)
        self.allow_en_passant = False
        self.dy = -1 if self.player == 0 else 1
        self.promotion_row = 0 if self.player == 0 else 7
    
    def _move_en_passant(self, p: int, q: int, board: list[list]) -> bool:
        for dir in [-1, 1]:
            if self._valid_tile(self.y, self.x + dir, board) and \
                    board[self.y][self.x + dir] != PIECES['EMPTY_TILE'] and \
                    board[self.y][self.x + dir].name == 'PAWN' and \
                    self.x + dir == q:
                board[self.y][self.x + dir] = PIECES['EMPTY_TILE']
                return True
    
    def _move_pawn_promotion(self, p: int, q: int, board: list[list]) -> None:
        board[p][q] = Queen(self.player, p, q)
        board[self.y][self.x] = PIECES['EMPTY_TILE']
    
    def move(self, p: int, q: int, board: list[list]) -> bool:
        if abs(self.y - p) == 2: self.allow_en_passant = True
        if self._move_en_passant(p, q, board): return True
        elif p == self.promotion_row: self._move_pawn_promotion(p, q, board)
        else: return super().move(p, q, board)

    def get_valid_moves(self, board: list[list]) -> list[tuple]:
        valid_moves = []
        i, j = self.y, self.x

        # allow capture pieces diagonally
        for p, q in [(self.dy, -1), (self.dy, 1)]:
            if self._valid_tile(i + p, j + q, board) and board[i + p][j + q] != PIECES['EMPTY_TILE']:
                valid_moves.append((i + p, j + q))
        
        # allow move one step forward if tile is empty
        if self._valid_tile(i + 1 * self.dy, j, board) and board[i + 1 * self.dy][j] == PIECES['EMPTY_TILE']:
            valid_moves.append((i + 1 * self.dy, j))
        
        # allow move two step forward if next two tiles are empty and still on original position
        if (3.5 - 2.5 * self.dy) == i and self._valid_tile(i + 2 * self.dy, j, board) and \
                board[i + 2 * self.dy][j] == PIECES['EMPTY_TILE'] and board[i + self.dy][j] == PIECES['EMPTY_TILE']:
            valid_moves.append((i + 2 * self.dy, j))
        
        # en passant
        for p, q in [(0, -1), (0, 1)]:
            if self._valid_tile(i + p, j + q, board):
                tile = board[i + p][j + q]
                if tile != PIECES['EMPTY_TILE'] and \
                        tile.name == 'PAWN' and tile.allow_en_passant:
                    valid_moves.append((i + p + self.dy, j + q))

        return valid_moves
