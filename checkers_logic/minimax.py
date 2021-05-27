from copy import deepcopy

RED = "red"
BLACK = "black"


def minimax(board, depth, max_player):
    if depth == 0 or board.winner():
        return board.evaluate(), board

    if max_player:
        maxEval = float("-inf")
        best_move = None
        for move in get_all_moves(board, RED):
            evaluation = minimax(move[0], depth-1, False)[0]
            if maxEval < evaluation:
                maxEval = evaluation
                best_move = move

        return maxEval, best_move
    else:
        minEval = float("inf")
        best_move = None
        for move in get_all_moves(board, BLACK):
            evaluation = minimax(move[0], depth-1, True)[0]
            if minEval > evaluation:
                minEval = evaluation
                best_move = move

        return minEval, best_move


def simulate_move(piece, move, board, skip):
    board.move(piece, move[0])
    if skip:

        color = BLACK if piece.color == RED else RED
        board.remove(move[1], color)

    return board


def get_all_moves(board, color):
    moves = []
    board.possible_moves(color)
    if color == RED:
        pieces = board.red_pieces
    else:
        pieces = board.black_pieces
    for piece in pieces:
        valid_moves = piece.next_moves
        for move in valid_moves:
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.y, piece.x, piece.color)
            new_board = simulate_move(temp_piece, move, temp_board, piece.can_jump)
            moves.append(new_board, piece, move)

    return moves
