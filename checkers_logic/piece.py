import numpy as np

LEFT = -1
RIGHT = 1


class Piece:

    def __init__(self, pos, color, direction):
        self.y = pos[0]
        self.x = pos[1]
        self.color = color  # two possible colors - RED or BLACK
        self.forward = direction
        self.king = False
        self.can_jump = False
        self.is_jumping = False
        self.valid_moves = self.poss_moves()
        self.next_moves = []



    def move(self, pos):
        """
        Sets the position of the piece
        Arguments:
            pos ([y, x]): position where the piece will be moved
        """
        self.y = pos[0]
        self.x = pos[1]
        self.valid_moves = self.poss_moves()

    def poss_moves(self):
        """
        Generates the possible moves of the piece, without taking into account other pieces
        Returns:
            moves (List[[y,x]]): possible moves, taking just into account the dimensions of the board
        """
        moves = []
        left = [self.y + self.forward, self.x + LEFT]
        right = [self.y + self.forward, self.x + RIGHT]
        if 7 >= left[0] >= 0 and left[1] >= 0:
            moves.append(left)
        if 7 >= right[0] >= 0 and 7 >= right[1]:
            moves.append(right)
        if self.king or self.is_jumping:
            left = [self.y - self.forward, self.x + LEFT]
            right = [self.y - self.forward, self.x + RIGHT]
            if 7 >= left[0] >= 0 and left[1] >= 0:
                moves.append(left)
            if 7 >= right[0] >= 0 and 7 >= right[1]:
                moves.append(right)
        return moves

    def add_next_move(self, move):
        """Appends a move into the list next_moves"""
        self.next_moves.append(move)
        

    def del_next_moves(self):
        """Deletes all the elements from next_moves"""
        self.next_moves = []

    def make_king(self):
        """
        Checks if a piece can be made a king, returns a boolean
        Returns:
            (bool): whether the piece can become a king
        """
        king_y = 7 if self.forward == 1 else 0
        if self.y == king_y and not self.king:
            self.king = True
            self.valid_moves = self.poss_moves()
            return True

        return False

    def set_can_jump(self, val):
        self.can_jump = val

    def set_is_jumping(self, val):
        self.is_jumping = val

    def get_skipped_pos(self, n_pos):
        if self.can_jump:
            arr = np.array(self.next_moves)
            for a in arr:
                if n_pos in a[0]:
                    return a[1]
        else:
            print("There is no skipped position")

    def __eq__(self, other):
        """Can be compared with other Piece objects or with lists with [y,x] structure"""
        if type(other) is list:
            return other == [self.y, self.x]
        else:
            return [other.y, other.x] == [self.y, self.x]

    def __str__(self):
        """ Returns the position of the piece """
        return "[" + str(self.y) + ", " + str(self.x) + "]"
        
        
if __name__ == "__main__":
    ls = np.array([2,3])
    p1 = Piece([3,3], "black")
    p = Piece([2,3], "black")
    print(ls == p)
