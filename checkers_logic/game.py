from checkers_logic.board import Board

# board = Board()
RED = "red"
BLACK = "black"


class Game:

    def __init__(self, pieces):
        self.selected = None
        self.board = Board(pieces)
        self.turn = RED
        self.valid_moves = []
        # self.win = win

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = []

    def reset(self):
        self._init()

    def get_board(self):
        return self.board

    def change_turn(self):
        self.valid_moves = []
        #if self.selected.can_jump:
        #    return
        if self.turn == RED:
            self.turn = BLACK
            self.board.possible_moves(self.turn)
        elif self.turn == BLACK:
            self.turn = RED
            self.board.possible_moves(RED)

    def move(self, pos):
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
        piece = self.board.get_piece(y, x, self.turn)
        if piece:
            self.selected = piece
            self.valid_moves = piece.next_moves

    def draw_valid_moves(self, piece):
        self.board.draw_piece_moves(piece)

    def ai_move(self, board):
        self.board = board
        self.board.draw_board()
        self.change_turn()

    def winner(self):
        return self.board.winner()
