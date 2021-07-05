from copy import deepcopy

RED = "red"
BLACK = "black"


def minimax(board, depth, max_player, color):
    if depth == 0 or board.winner():
        return board.evaluate(), board

    if max_player:
        maxEval = float("-inf")
        best_move = None
        moves, can_jump = get_all_moves(board, color)
        if can_jump:
            max_player = True
        else:
            max_player = False
            depth = depth - 1
            color = RED if color == BLACK else RED
        if moves:

            for move in moves:
                evaluation = minimax(move[0], depth, max_player, color)[0]
                if maxEval < evaluation:
                    maxEval = evaluation
                    best_move = move

        return maxEval, best_move
    else:
        minEval = float("inf")
        best_move = None
        moves, can_jump = get_all_moves(board, color)
        if can_jump:
            max_player = False
        else:
            max_player = True
            depth = depth - 1
            color = RED if color == BLACK else RED
        if moves:
            for move in moves:
                evaluation = minimax(move[0], depth, max_player, color)[0]
                if minEval > evaluation:
                    minEval = evaluation
                    best_move = move
        return minEval, best_move


def simulate_move(piece, move, board, skip):

    board.move(piece, move[0])
    if skip:

        color = BLACK if piece.color == RED else RED
        rm_piece = board.get_piece(move[1][0], move[1][1], color)

        board.remove(rm_piece, color)
        piece.del_next_moves()
        board.check_jump(piece)
        if len(piece.next_moves) == 0:
            piece.set_can_jump(False)
            board.last_jump = None
            board.is_jumping = False
    return board


def get_all_moves(board, color):
    moves = []
    board.possible_moves(color)
    can_jump = False
    pieces = board.valid_pieces
    if pieces:
        for piece in pieces:
            valid_moves = piece.next_moves
            for move in valid_moves:
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.y, piece.x, piece.color)
                new_board = simulate_move(temp_piece, move, temp_board, piece.can_jump)
                if new_board.is_jumping:
                    can_jump = True
                moves.append([new_board, piece, move])

        return moves, can_jump

