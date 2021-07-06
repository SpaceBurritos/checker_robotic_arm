from checkers_logic.board import Board

# board = Board()
RED = "red"
BLACK = "black"


class Game:

    def __init__(self, pieces):
        self.selected = None
        self.turn = self.get_computer_color(pieces)
        self.board = Board(pieces, self.turn)
        self.valid_moves = []
        self.computer_color = self.turn
        self.player_color = BLACK if self.computer_color == RED else RED
        # self.win = win

    def get_board(self):
        return self.board

    def change_turn(self):
        """
        Checks if the player is in middle of multiple jumps
        Parameters:
            computer_turn (boolean):
        """
        self.valid_moves = []
        if self.selected.can_jump:
            self.board.possible_moves(self.turn)
            return
        else:
            if self.turn == RED:
                self.turn = BLACK
                self.selected = None
            elif self.turn == BLACK:
                self.turn = RED
                self.selected = None

            self.board.possible_moves(self.turn)

    def move(self, pos):
        """
        Moves a selected piece
        Parameters:
            pos ([y, x]): future position of the piece
        """
        if self.selected:
            self.board.move(self.selected, pos)
            if self.selected.can_jump:
                skipped_pos = self.selected.get_skipped_pos(pos)
                color = RED if self.turn == BLACK else BLACK
                skipped = self.board.get_piece(skipped_pos[0], skipped_pos[1], color)
                self.board.remove(skipped, color)
                self.board.draw_board()
                self.board.possible_moves(self.turn)
                self.valid_moves = self.selected.next_moves

        else:
            return False

        return True

    def select(self, y, x):
        """
        Selects a piece so that it can be moved or shown possible moves
        Parameters:
            y (int): y-coordinate (0-7)
            x (int): x-coordinate (0-7)
        """
        piece = self.board.get_piece(y, x, self.turn)
        if piece:
            self.selected = piece
            self.valid_moves = piece.next_moves

    def draw_valid_moves(self):
        self.board.draw_piece_moves(self.selected)

    def ai_move(self, piece, pos):
        self.selected = piece
        self.move(pos)
        self.board.draw_board()
        self.change_turn()

    def set_player_move(self, board):
        """
        Compares the current board with the board obtained from the camera, and checks that only a move was done
        Parameters:
            board (Board): board obtained from the camera
        Return:
             (boolean): whether the move is valid or not
        """
        if self.board.compare_boards_and_move(board, self.player_color):
            self.change_turn(False)
            return True
        return False

    def get_computer_color(self, pieces):
        red_y = [p[0] for p in pieces[1]]
        mean_red = sum(red_y) / len(red_y)
        black_y = [p[0] for p in pieces[0]]
        mean_black = sum(black_y) / len(black_y)

        return RED if mean_red < mean_black else BLACK

    def is_computer_turn(self):
        return self.turn == self.computer_color

    def winner(self):
        return self.board.winner()
