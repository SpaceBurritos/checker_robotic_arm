import numpy as np
from checkers_logic.piece import Piece
from copy import deepcopy

LEFT = "left"
RIGHT = "right"
RED = "red"
BLACK = "black"


class Board:

    def __init__(self, pieces=[], color=RED):

        self.black_pieces = [Piece(piece, BLACK) for piece in pieces[0]]
        self.red_pieces = [Piece(piece, RED) for piece in pieces[1]]
        self.valid_pieces = []
        self.valid_moves = {}
        self.color = color
        self.num_red = len(self.red_pieces)
        self.num_black = len(self.black_pieces)
        self.red_kings = 0
        self.black_kings = 0
        self.win = None
        self.board = self.draw_board()
        self.possible_moves(color)

    def draw_board(self):
        row = ['-' for i in range(8)]
        self.board = [row for i in range(8)]
        self.board = np.array(self.board)

        for black in self.black_pieces:
            if black.king:
                self.board[black.y][black.x] = "B"
            else:
                self.board[black.y][black.x] = "b"
        for red in self.red_pieces:
            if red.king:
                self.board[red.y][red.x] = "R"
            else:
                self.board[red.y][red.x] = "r"
        return self.board

    def draw_piece_moves(self, piece):
        for i, move in enumerate(piece.next_moves):
            move = move[0]
            self.board[move[0]][move[1]] = i + 1

    '''
    pos = [pos_y, pos_x] -> position of the piece to be moved
    n_pos = [pos_y, pos_x] -> new position of the piece 
    to be moved
    '''

    def move(self, piece, n_pos):
        moves = np.array(piece.next_moves)
        if n_pos in moves[:, 0]:
            piece.move(n_pos)
            piece.make_king()
            self.draw_board()
        else:
            print("Invalid move position")

    '''
    Generates a list of all the possible moves that the pieces on the board can do, if there are jump moves these will
    take priority
    :param
    color = string -> color of the pieces looking for the possible moves
    '''

    def remove(self, piece, color):
        if color == RED:
            if piece in self.red_pieces:
                self.red_pieces.remove(piece)
        elif color == BLACK:
            if piece in self.black_pieces:
                self.black_pieces.remove(piece)

    def possible_moves(self, color):
        self.valid_pieces = []
        [piece.del_next_moves() for piece in self.red_pieces]
        [piece.del_next_moves() for piece in self.black_pieces]
        self.check_jumps(color)
        if len(self.valid_pieces) > 0:  # If there are jumps the only possible moves are the jumps
            return
        else:
            if color == RED:
                for piece in self.red_pieces:
                    moves = piece.valid_moves
                    for move in moves:
                        if move not in self.black_pieces and move not in self.red_pieces:
                            piece.add_next_move([move])
                            if piece not in self.valid_pieces:
                                self.valid_pieces.append(piece)
            elif color == BLACK:
                for piece in self.black_pieces:
                    moves = piece.valid_moves
                    for move in moves:
                        if move not in self.black_pieces and move not in self.red_pieces:
                            piece.add_next_move([move])
                            if piece not in self.valid_pieces:
                                self.valid_pieces.append(piece)
            else:
                print("Color not available")

    '''
    Generating all the possible jumps, including multiple jumps on a same turm
    :param
    color = string -> color of the pieces
    '''

    def check_jumps(self, color):
        if color == RED:
            for piece in self.red_pieces:
                piece.set_can_jump(False)
                self.check_jump(piece)
        elif color == BLACK:
            for piece in self.black_pieces:
                piece.set_can_jump(False)
                self.check_jump(piece)

    def check_jump(self, piece, board):
        if piece.color == RED:
            for move in piece.valid_moves:
                if move in self.black_pieces:
                    n_move = [move[0] + (move[0] - piece.y), move[1] + (move[1] - piece.x)]
                    if n_move not in self.red_pieces and n_move not in self.black_pieces:
                        if 7 >= n_move[0] >= 0 and 7 >= n_move[1] >= 0:
                            if piece not in self.valid_pieces:
                                self.valid_pieces.append(piece)
                            piece.add_next_move([n_move, move])
                            temp_board = deepcopy(board)
                            temp_piece = piece.move(n_move)
                            temp_board.red_pieces.append(temp_piece)
                            self.check_jump(temp_piece, temp_board)
                            piece.set_can_jump(True)
            return

        elif piece.color == BLACK:
            for move in piece.valid_moves:
                if move in self.red_pieces:
                    n_move = [move[0] + (move[0] - piece.y), move[1] + (move[1] - piece.x)]
                    if n_move not in self.red_pieces and n_move not in self.black_pieces:
                        if 7 >= n_move[0] >= 0 and 7 >= n_move[1] >= 0:
                            if piece not in self.valid_pieces:
                                self.valid_pieces.append(piece)
                            piece.add_next_move([n_move, move])
                            piece.set_can_jump(True)

    def get_key(self, pos):
        y, x = pos
        return y*7 + x

    def winner(self):
        if self.black_pieces == 0:
            self.win = BLACK
            return True
        elif self.red_pieces == 0:
            self.win = RED
            return True
        else:
            return False

    def add_red_king(self):
        self.red_kings += 1

    def add_black_king(self):
        self.black_kings += 1

    def get_piece(self, y, x, color):
        if color == RED:
            for p in self.red_pieces:
                if p.y == y and p.x == x:
                    return p
        elif color == BLACK:
            for p in self.black_pieces:
                if p.y == y and p.x == x:
                    return p
        else:
            print("No such piece")

    def __str__(self):
        n = 0
        str_board = "x  0  1  2  3  4  5  6  7 \n"
        for y in self.board:
            str_board += str(n) + " "
            for x in y:
                str_board += " " + x + " "
            str_board += "\n"
            n += 1
        return str_board

    def evaluate(self):
        #return self.num_red - self.num_black + (self.red_kings * 2 - self.black_kings * 2)
        return sum([7 - r.y + 5 for r in self.red_pieces if not r.king]) - sum([b.y + 5 for b in self.black_pieces if not b.king]) +\
            sum([7 - r.y + 7 for r in self.red_pieces if r.king]) - sum([b.y + 7 for b in self.black_pieces if b.king])

if __name__ == "__main__":
    pieces = [[[1, 3], [1, 5], [3, 1], [3, 3], [2, 0], [3, 5], [2, 4]],
              [[6, 4], [6, 0], [4, 2], [7, 1], [4, 6], [6, 6], [4, 4]]]

    # pieces[0] -> black
    # pieces[1] -> red
    game = Board(pieces)
    print(game)
    game.possible_moves(RED)
    print(game.valid_pieces)
    # game.move([7, 1], [6,2])
    pic = game.get_piece(6,0, RED)
    print(pic.valid_moves)