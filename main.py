

from checkers_logic.game import Game
from checkers_logic.minimax import minimax
from robot_movement.inverse_kinematics import IK
from digital_board.digital_board import DigitalBoard
from digital_board.camera import Camera
from boardFinder.main import detect
from checkers_logic.board import Board
import cv2

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
    dofbot = IK()
    dofbot.set_initial_pose()
    cam = Camera()
    print("Please take all the pieces off the board, then press enter")
    _ = input()
    pic = cam.take_picture()
    #cam.exit()

    #reference_img = detect(pic)
    reference_img = cv2.imread("boardFinder/output.jpg")


    db = DigitalBoard(reference_img)
    #cam.set_cam()
    
    print("Please set up the board, then press enter")
    _ = input()

    pic_pieces = cam.take_picture()
    #cv2.imshow("pic_pieces", pic_pieces)
    #cv2.waitKey(0)
    pieces = db.digitalize_board(pic_pieces)
    game = Game(pieces)

    print(game.board)

    while run:

        if game.winner():
            print(game.winner())
            run = False
            cam.exit()
            return

        if game.is_computer_turn():

            evalu, move = minimax(game.board, 4, True, game.computer_color)
            new_board = move[0]
            piece = move[1]
            n_move = move[2][0]
            print("eval: ", evalu)
            if piece.can_jump:
                dofbot.jumpPiece([piece.y, piece.x], n_move)
            else:
                dofbot.movePiece([piece.y, piece.x], n_move)
            game.ai_move(piece, n_move)

        else:
            while True:         
                print("Press enter to continue: ")
                x = input()

                player_move = cam.take_picture()
                
                pieces = db.digitalize_board(player_move)
                board = Board(pieces, game.computer_color) 

                if game.set_player_move(board):
                    print("piece", piece)
                    game.select(piece.y, piece.x)
                    break
                print("Please play a valid move")
                print(game.board)

if __name__ == "__main__":
    main()
