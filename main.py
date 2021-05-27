from checkers_logic.game import Game
from checkers_logic.minimax import minimax
from robot_movement.inverse_kinematics import IK
from digital_board.digital_board import DigitalBoard

RED = "red"
BLACK = "black"

def check_positions(x, y, valid_positions):
    for vp in valid_positions:
        if [int(y), int(x)] == [vp.y, vp.x]:
            return True
    print("Piece not available")
    print("Possible positions are: ")
    for p in valid_positions:
        print(p)
    return False


def main():
    run = True
    pieces = []
    red = []
    black = []
    for y in range(3):
        for x in range(8):
            if (x + y) % 2 != 0:
                black.append([y, x])
            if (7 - y + x) % 2 != 0:
                red.append([7 - y, x])
    pieces.append(black)
    pieces.append(red)
    game = Game(pieces)
    dofbot = IK()

    while run:

        if game.winner():
            print(game.winner())
            run = False

        if game.turn == RED:
            evalu, move = minimax(game.board, 5, True, game)
            new_board = move[0]
            piece = move[1]
            n_move = move[2]
            print("eval: ", evalu)
            game.ai_move(new_board)
            dofbot.movePiece([piece.y, piece.x], n_move)
            print(game.board)

        else:
            print(game.turn, "turn (y x)")

            print(game.board)
            print("Possible positions: ")

            for p in game.board.valid_pieces:
                print(p)

            while True:
                y, x = input().split()
                if check_positions(x, y, game.board.valid_pieces):
                    break
            game.select(int(y), int(x))

            game.draw_valid_moves(game.selected)
            print(game.board)
            print("Select the desired move: ")
            x = input()

            game.move(game.valid_moves[int(x) - 1][0])

            game.change_turn()
        print("turn changed ", game.turn)


if __name__ == "__main__":
    main()
