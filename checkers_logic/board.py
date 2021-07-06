import numpy as np
from checkers_logic.piece import Piece
from copy import deepcopy

RED = "red"
BLACK = "black"


class Board:

    def __init__(self, pieces, color):
        directions = self.get_directions(pieces)
        self.black_pieces = [Piece(piece, BLACK, directions[0]) for piece in pieces[0]]
        self.red_pieces = [Piece(piece, RED, directions[1]) for piece in pieces[1]]
        self.all_pieces = self.black_pieces + self.red_pieces
        self.valid_pieces = []
        self.computer_color = color
        self.player_color = BLACK if color == RED else RED
        self.num_red = len(self.red_pieces)
        self.num_black = len(self.black_pieces)
        self.red_kings = 0
        self.black_kings = 0
        self.win = None
        self.board = self.draw_board()
        self.can_jump = False
        self.possible_moves(color)

    def draw_board(self):
        """Draws the board with the current position from the pieces
        Returns:
            (Arr[Arr[Strings]]): the position of all the pieces in a list of lists
        """
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
        """
        Draw the possible next_moves of a chosen piece, with numbers from 1 to 2 or 4
        Parameters:
            piece (Piece): piece that will be used to get the next moves
        """
        for i, move in enumerate(piece.next_moves):
            move = move[0]
            self.board[move[0]][move[1]] = i + 1

    def move(self, piece, n_pos):
        """
        First checks if a move is valid and then moves the chosen piece
        Parameters:
            piece (Piece): piece to be moved
            n_pos  ([pos_y, pos_x]) -> new position of the piece to be moved
        """
        moves = np.array(piece.next_moves)
        if n_pos in moves[:, 0]:
            if piece.can_jump:
                piece.set_is_jumping(True)
            piece.move(n_pos)
            if piece.make_king():
                if piece.color == RED:
                    self.add_red_king()
                elif piece.color == BLACK:
                    self.add_black_king()
            self.draw_board()
        else:
            print("Invalid move position")

    def remove(self, piece, color):
        """
        Generates a list of all the possible moves that the pieces on the board can do, if there are jump moves these
        will take priority
        Parameters:
            piece (Piece): piece that will be removed
            color (String): color of the pieces looking for the possible moves
        """
        self.all_pieces.remove(piece)
        if color == RED:
            if piece in self.red_pieces:
                if piece.king:
                    self.red_kings -= 1
                self.red_pieces.remove(piece)
                self.num_red = len(self.red_pieces)

        elif color == BLACK:
            if piece in self.black_pieces:
                if piece.king:
                    self.black_kings -= 1
                self.black_pieces.remove(piece)
                self.num_black = len(self.black_pieces)

    def possible_moves(self, color):
        self.valid_pieces = []
        [piece.del_next_moves() for piece in self.all_pieces]

        if self.get_jumping_piece_moves():
            return

        self.check_jumps(color)
        if len(self.valid_pieces) > 0:  # If there are jumps the only possible moves are the jumps
            self.can_jump = True
        else:
            self.can_jump = False
            if color == RED:
                for piece in self.red_pieces:
                    moves = piece.valid_moves
                    for move in moves:
                        if move not in self.all_pieces:
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

    def get_jumping_piece_moves(self):
        jumping_piece = [p for p in self.all_pieces if p.is_jumping]
        if jumping_piece:
            jumping_piece = jumping_piece[0]
            self.check_jump(jumping_piece)
            if len(self.valid_pieces) == 0:  # if there are no moves for the jumping piece, finish the turn
                jumping_piece.set_is_jumping(False)
                jumping_piece.poss_moves()
                self.can_jump = False
            return True
        else:
            return False

    def check_jumps(self, color):
        """
        Generating all the possible jumps of all the pieces
        Parameters:
            color (String): color of the pieces
        """
        if color == RED:
            for piece in self.red_pieces:
                self.check_jump(piece)
        elif color == BLACK:
            for piece in self.black_pieces:
                self.check_jump(piece)

    def check_jump(self, piece):  # board -> extra argument
        """
        Generates all the possible jumps for a piece
        Parameters:
            piece (Piece): piece that will be checked
        """
        piece.set_can_jump(False)
        if piece.color == RED:
            for move in piece.valid_moves:
                if move in self.black_pieces:
                    n_move = [move[0] + (move[0] - piece.y), move[1] + (move[1] - piece.x)]
                    if n_move not in self.red_pieces and n_move not in self.black_pieces:
                        if 7 >= n_move[0] >= 0 and 7 >= n_move[1] >= 0:
                            if piece not in self.valid_pieces:
                                self.valid_pieces.append(piece)
                            piece.add_next_move([n_move, move])
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

    def compare_boards_and_move(self, img_board):
        """
        Compares the current board with another board to check if the changes come from a valid move
        Parameters:
            img_board (Board): other board
        Returns:
            (boolean): whether the move was successful or not
        """
        b_pieces = deepcopy(self.black_pieces)
        r_pieces = deepcopy(self.red_pieces)

        n_move = []
        # Checks the differences between the black pieces, to get the piece that was moved
        # and where it moved
        if self.player_color == BLACK:
            for b in img_board.black_pieces:
                if b not in b_pieces:
                    n_move.append([b.y, b.x])
                else:
                    b_pieces.remove(b)
            #   Checks the difference between the red pieces, to search if any 
            #   red pieceS were removed
            for r in img_board.red_pieces:
                if r in r_pieces:
                    r_pieces.remove(r)
            if len(b_pieces) != 1 or len(n_move) != 1:
                print("More than one piece was moved")
                return False
            else:
                pos = [b_pieces[0].y, b_pieces[0].x]
                piece = self.get_piece(pos[0], pos[1], BLACK)
                if len(r_pieces) == 0:
                    self.move(piece, n_move[0])
                    return True
                elif piece.can_jump and len(r_pieces) > 0:
                    while piece.can_jump:
                        jump_moves = piece.next_moves
                        jump = None
                        for r in r_pieces:
                            jump = [x for x in jump_moves if x[1] == r]
                            if jump:
                                r_pieces.remove(r)
                                jump = jump[0]
                                break

                        if not jump:
                            return False

                        self.move(piece, jump[0])
                        piece2 = self.get_piece(jump[1][0], jump[1][1], RED)
                        self.remove(piece2, RED)
                        self.possible_moves(BLACK)
                        self.draw_board()
                    return True
                else:
                    print("something fishy happened")
                    return False
        else:
            #   Checks the difference between the black pieces, to check if any 
            #   black pieces were removed
            for b in img_board.black_pieces:
                if b in b_pieces:
                    b_pieces.remove(b)

            for r in img_board.red_pieces:
                if r not in r_pieces:
                    n_move.append([r.y, r.x])
                else:
                    r_pieces.remove(r)
            if len(r_pieces) != 1 or len(n_move) != 1:
                print("More than one piece was moved")
                return False
            else:
                pos = [r_pieces[0].y, r_pieces[0].x]
                piece = self.get_piece(pos[0], pos[1], RED)
                if len(b_pieces) == 0:
                    self.move(piece, n_move[0])
                    return True

                elif piece.can_jump and len(b_pieces) > 0:
                    while piece.can_jump:
                        jump_moves = piece.next_moves
                        jump = None
                        for b in b_pieces:
                            jump = [x for x in jump_moves if x[1] == b][0]
                            if jump:
                                b_pieces.remove(b)
                                jump = jump[0]
                                break

                        if not jump:
                            return False

                        self.move(piece, jump[0])
                        piece2 = self.get_piece(jump[1][0], jump[1][1], BLACK)
                        self.remove(piece2, BLACK)
                        self.possible_moves(RED)
                        self.draw_board()
                    return True

                else:
                    print("something fishy happened")
                    return False

    def winner(self):
        """
        Checks if any of the sides has 0 pieces
        Returns:
            (boolean): whether there is a winner or not
        """
        if self.num_red == 0:
            self.win = BLACK
            return True
        elif self.num_black == 0:
            self.win = RED
            return True
        else:
            return False

    def add_red_king(self):
        self.red_kings += 1

    def add_black_king(self):
        self.black_kings += 1

    def get_piece(self, y, x, color):
        """
        Get the Piece object from its coordinates
        Parameters:
            y (int): y-coordinate (0-7)
            x (int): x-coordinate (0-7)
            color (String): color of the piece (red or black)
        Returns:
            p (Piece): the respective piece with the given coordinates
        """
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
            return None

    def get_directions(self, pieces):
        red_y = [p[0] for p in pieces[1]]
        mean_red = sum(red_y) / len(red_y)
        black_y = [p[0] for p in pieces[0]]
        mean_black = sum(black_y) / len(black_y)

        return [-1, 1] if mean_red < mean_black else [1, -1]

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
        """
        Evaluates the board conditions for the computer
        Returns:
            (int): the value of the board's current structure with respect to the computer's pieces
        """
        if self.computer_color == BLACK:
            return sum([b.y for b in self.black_pieces if not b.king]) - sum(
                [7 - r.y for r in self.red_pieces if not r.king]) + \
                   8 * self.black_kings - 8 * self.red_kings
        else:
            return sum([r.y for r in self.red_pieces if not r.king]) - sum(
                [7 - b.y for b in self.black_pieces if not b.king]) + \
                   8 * self.red_kings - 8 * self.black_kings


if __name__ == "__main__":
    piecesN = [[[1, 3], [1, 5], [3, 1], [3, 3], [2, 0], [3, 5], [2, 4]],
               [[6, 4], [6, 0], [4, 2], [7, 1], [4, 6], [6, 6], [4, 4]]]
    piecesN2 = [[[1, 3], [1, 5], [3, 1], [5, 1], [2, 0], [3, 5], [2, 4]],
                [[6, 4], [6, 0], [7, 1], [4, 6], [6, 6], [4, 4]]]
    # pieces[0] -> black
    # pieces[1] -> red
    game = Board(piecesN)
    game.possible_moves(BLACK)
    game2 = Board(piecesN2)
    print(game)
    print(game2)
    game.compare_boards_and_move(game2)
    print(game)
    # game.possible_moves(RED)
    # print(game.valid_pieces)
    # game.move([7, 1], [6,2])
    # pic = game.get_piece(6,0, RED)
    # print(pic.valid_moves)
