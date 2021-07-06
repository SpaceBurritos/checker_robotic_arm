from copy import deepcopy

RED = "red"
BLACK = "black"


def minimax(board, depth, max_player, color):
    """
    Gets the value of the position of the game, based on future actions
    Parameters:
         board (Board): board with the information of the pieces
         depth (int): number of moves in the future
         max_player (bool): if its the player looking for the max eval
         color (String): color of the pieces
    Returns:
        maxEval (int): return the best evaluation with the given depth
        best_move ([new_board, piece, move]): returns the best move with the piece with that move and the board
    """
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
        #print("maxEval:", maxEval, best_move)
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
        #print("minEval", minEval, best_move)
        return minEval, best_move


def simulate_move(piece, move, board, skip):
    """
    Simulates one move
    Parameters:
        piece (Piece):
        move ([[next position y, next position x],[piece removed y, piece removed x]]): move to be simulated and the
        position of the piece that will be removed
        board (Board):
        skip (bool): if the piece can jump
    Returns:
        board (Board): the board with the moves done
    """
    board.move(piece, move[0])
    if skip:

        color = BLACK if piece.color == RED else RED
        rm_piece = board.get_piece(move[1][0], move[1][1], color)

        board.remove(rm_piece, color)
        piece.del_next_moves()
        board.check_jump(piece)
        if len(piece.next_moves) == 0:
            piece.set_can_jump(False)
            piece.set_is_jumping(False)
    return board


def get_all_moves(board, color):
    """
    Goes through all the possible moves for one round
    Parameters:
        board (Board): board with all the information
        color (String): color of the pieces
    Returns:
        moves ([new_board, piece, move]): the board with the changes, the piece that was moved and the position where it
        was move
        can_jump (bool): whether one of the pieces can keep jumping
    """
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
                if temp_piece.is_jumping:
                    can_jump = True
                moves.append([new_board, piece, move])
        return moves, can_jump

