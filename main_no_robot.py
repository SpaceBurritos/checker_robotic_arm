            

from checkers_logic.game import Game
from checkers_logic.minimax import minimax
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
    
    #black_pieces = [[2,3], [5,6],[6,7], [7,0], [4,5], [3,2]]
    #red_pieces = [[1,2], [0,7], [6,1], [1,4]]
    
    
    black_pieces = []
    red_pieces = []
    for y in range(8):
        if y < 3:
            for x in range(8):
                if (y + x) % 2 != 0:
                    red_pieces.append([y,x])
        elif y > 4:
            for x in range(8):
                if (y + x) % 2 != 0:
                    black_pieces.append([y,x])
                   
    pieces = [black_pieces, red_pieces]
                
    game = Game(pieces)
    computer_color = game.turn
    
    print(game.board)



    while run:

        if game.winner():
            print(game.board.win)
            run = False

        elif game.turn == computer_color:

            evalu, move = minimax(game.board, 4, True, RED)
            print(move)
            new_board = move[0]
            piece = move[1]
            n_move = move[2][0]
            print(piece, n_move)
            print(n_move)
            print("eval: ", evalu)
            game.ai_move(piece, n_move)
            print(game.board)

        else:

            while not game.selected:
                print(game.board)
                print("Select a piece: ")
                for piece in game.board.valid_pieces:
                    print(piece)
                
                piece = list(map(int, input().split()))
                if piece in game.board.valid_pieces:
                    game.select(piece[0], piece[1]) 
            game.select(game.selected.y, game.selected.x)
            moves = game.valid_moves
            print("moves:", moves)
            print("selected", game.selected)
            while True:
                try:
                    game.draw_valid_moves()
                    print(game.board)
                    mv = int(input())
                    if mv <= len(moves):
                        break
                except ValueError:
                    print("Not a number")
                    
            game.move(moves[mv-1][0])
            print(game.board)
            game.change_turn()
        #print("turn changed ", game.turn)


if __name__ == "__main__":
    main()
