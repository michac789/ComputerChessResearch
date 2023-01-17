import copy, random
from chess.chess_board import ChessBoard
from chess.chess_constants import PIECES, SCORES


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


def computer_lvl2(cb: ChessBoard):
    moves = get_all_possible_moves(cb)
    score_move = [-999999, []]
    for move in moves:
        temp_cb = copy.deepcopy(cb)
        temp_cb.move_piece(*move)
        mult = 1 if temp_cb.player == 0 else -1
        new_score = negamax(temp_cb, 2, -999999, 999999) * mult
        if new_score > score_move[0]: score_move = [new_score, [move]]
        elif new_score == score_move[0]: score_move[1].append(move)
    return random.choice(score_move[1])


def negamax(cb: ChessBoard, depth: int, alpha: int, beta: int):
    if depth == 0 or cb.game_ended == True:
        return evaluate_position(cb.board)
    moves = get_all_possible_moves(cb)
    score = -999999
    for move in moves:
        temp_cb = copy.deepcopy(cb)
        temp_cb.move_piece(*move)
        new_score = negamax(temp_cb, depth - 1, -beta, -alpha) * (1 if cb.player == 1 else -1)
        score = max(score, new_score)
        alpha = max(alpha, score)
        if beta <= alpha: break
    return score * (1 if cb.turn == 1 else -1)


def evaluate_position(board):
    score = 0
    for i in range(8):
        for j in range(8):
            tile = board[i][j]
            score += SCORES[str(tile)]
    return score
