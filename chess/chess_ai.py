import copy, random
from chess.chess_board import ChessBoard
from chess.chess_constants import PIECES


'''
Given a chessboard object, return list of all possible moves in the format:
<initial_tile_y, initial_tile_x, end_tile_y, end_tile_x>
'''
def get_all_possible_moves(cb: ChessBoard) -> tuple[int, int, int, int]:
    possible_moves = []
    for i in range(8):
        for j in range(8):
            tile = cb.board[i][j]
            if tile != PIECES['EMPTY_TILE'] and tile.player == cb.player:
                moves = tile.get_valid_moves(cb.board)
                for move in moves:
                    possible_moves.append((i, j, move[0], move[1]))
    return possible_moves


def computer_lvl1(cb: ChessBoard):
    return random.choice(get_all_possible_moves(cb))
