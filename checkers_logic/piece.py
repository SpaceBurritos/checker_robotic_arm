import numpy as np

LEFT = -1
RIGHT = 1


class Piece:

    def __init__(self, pos, color, is_king=False):
        self.y = pos[0]
        self.x = pos[1]
        self.color = color
        self.king = is_king
        self.forward = 1 if color == "black" else -1
        self.valid_moves = self.poss_moves()
        self.next_moves = []
        self.can_jump = False
        self.del_pieces = []
        pass

    def move(self, pos):
        self.y = pos[0]
        self.x = pos[1]
        self.valid_moves = self.poss_moves()

    def poss_moves(self):
        moves = []
        left = [self.y + self.forward, self.x + LEFT]
        right = [self.y + self.forward, self.x + RIGHT]
        if 7 >= left[0] >= 0 and left[1] >= 0:
            moves.append(left)
        if 7 >= right[0] >= 0 and 7 >= right[1]:
            moves.append(right)
        if self.king:
            left = [self.y - self.forward, self.x + LEFT]
            right = [self.y - self.forward, self.x + RIGHT]
            if 7 >= left[0] >= 0 and left[1] >= 0:
                moves.append(left)
            if 7 >= right[0] >= 0 and 7 >= right[1]:
                moves.append(right)
        return moves

    def add_next_move(self, move):
        self.next_moves.append(move)
        

    def del_next_moves(self):
        self.next_moves = []

    def make_king(self):
        king_y = 7 if self.forward == 1 else 0
        if self.y == king_y and not self.king:
            self.king = True
        elif self.y == king_y:
            print("Already a king")

    def set_can_jump(self, val):
        self.can_jump = val

    def get_skipped_pos(self, n_pos):
        if self.can_jump:
            arr = np.array(self.next_moves)
            for a in arr:
                if n_pos in a[0]:
                    return a[1]
        else:
            print("There is no skipped position")

    def __eq__(self, other):
        return [other.y, other.x] == [self.y, self.x]

    def __str__(self):
        return "[" + str(self.y) + ", " + str(self.x) + "]"
