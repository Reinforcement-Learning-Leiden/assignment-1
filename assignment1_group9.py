#### For now the file only contains the user input. To be expanded to the whole program

from hex_skeleton import HexBoard
import ttalphabeta as ttab
import alphabeta as ab
from transposition_table import TranspositionTable as TT
import random

#TODO: Add a heuristic start strategy to speed up the beginning of the game!!!!

win_message = "******************************************\n\
*               YOU WIN                  *\n\
******************************************"

loss_message = "******************************************\n\
*              YOU LOSE                  *\n\
******************************************"

redWins=0
blueWins=0

def human_input(size_of_board): # TOASK: is it efficient to pass board as arguement? better way to retrieve board size?
    # TODO: This is fine, but we can add a try/catch block to make sure the user can't crash the main loop
    input_user = input("Your Turn: ")
    if ',' in input_user:
        x, y = input_user.split(',')
    else:
        x, y = input_user.split()
    x = int(x)
    y = int(y)
    if x in range(size_of_board) and y in range(size_of_board) :
        coordinates = (x, y)
        return coordinates
    else :
        print ('coordinates (', x, ',', y, ') are not in range')
        return

def move_generator_random(size_of_board):
    """DEPRECATED"""
    #TODO: If you want to keep using the random move gen, we can update it to just use random.choice from board.get_move_list() then you don't need to add extra checks
    x =  random.randint(0, size_of_board-1)
    y = random.randint(0, size_of_board-1)
    coordinates = (x, y)
    return coordinates

#TODO: 
##########################################################
#        CODE BLOCK FOR HUMAN (RED) VS AI (BLUE)         #
##########################################################

# def main():
#     print('the program plays Blue(LeftToRight) and the user plays Red(UpToButtom)')
#     board = HexBoard(4)
#     num_of_cells = board.get_board_size() * board.get_board_size()
#     for nc in range(int(num_of_cells/2)):
#         move_human = human_input(board.get_board_size())
#         while not move_human in board.get_move_list():
#             print('move is not legal, please choose another cell')
#             move_human = human_input(board.get_board_size())
#         board = ab._update_board(board, move_human ,False)
#         board.print()
#         if board.is_game_over(): # TODO: add condition for game over without no winning (board full)
#             print(win_message)
#             board.print()
#             print('Cutoffs: '+str(HexBoard.cutoffs))
#             break
#         move_program = ab.alphabeta_move(board, depth=3, is_max=True)
#         board = ab._update_board(board, move_program, True)
#         board.print()
#         if board.is_game_over():  # TODO: add condition for game over without no winning (board full)
#             print(loss_message)
#             board.print()
#             print('Cutoffs: ' + str(HexBoard.cutoffs))
#             break

##########################################################
#               CODE BLOCK FOR AI VS AI                  #
##########################################################

def main(bluePlayer,redPlayer):

    board = HexBoard(4)
    num_of_cells = board.get_board_size() * board.get_board_size()
    HexBoard.dCutoffs=0
    HexBoard.d4Cutoffs=0
    HexBoard.rCutoffs=0
    TT.ttCutoffs=0
    for nc in range(int(num_of_cells/2)):

        ## Just a small heuristic for opening strategy, you can test this if you want. But then you have to comment the move_blue below out too
            if board.size % 2 != 0 and len(board.get_move_list()) == len(board.get_all_vertices()): # If it's the first move and the board is uneven
                move_blue = (board.size // 2, board.size // 2) # Always place the first move in the middle
            else:
                if bluePlayer == 1:
                    move_blue = ab.alphabeta_moveR(board, depth=3, is_max=True)
                elif bluePlayer == 2:
                    move_blue = ab.alphabeta_move(board, depth=3, is_max=True)
                    HexBoard.dCutoffs+=HexBoard.cutoffs
                    HexBoard.cutoffs=0
                elif bluePlayer == 3:
                    move_blue = ab.alphabeta_move(board, depth=4, is_max=True)
                    HexBoard.d4Cutoffs+=HexBoard.cutoffs
                    HexBoard.cutoffs = 0
                elif bluePlayer == 4:
                    move_blue = ttab.iterative_deepening(board, is_max=True, max_seconds=20)





        #move_blue = ab.alphabeta_move(board, depth=4, is_max=True)
        #move_blue = ab.alphabeta_move_Id(board, is_max=True, show_AI=True)
            board = ab._update_board(board, move_blue, is_max=True)
            board.print()
            if board.is_game_over(): # TODO: add condition for game over without no winning (board full)
                HexBoard.total_dCutoffs+=HexBoard.dCutoffs
                HexBoard.total_d4Cutoffs += HexBoard.d4Cutoffs
                HexBoard.total_rCutoffs += HexBoard.rCutoffs
                TT.total_ttCutoffs+=TT.ttCutoffs
                print("==== BLUE WINS ====")
                board.print()
                print('Cutoffs made by AlphaBeta with random eval: ' + str(HexBoard.rCutoffs))
                print('Cutoffs made by AlphaBeta with Dijkstra eval depth 3: ' + str(HexBoard.dCutoffs))
                print('Cutoffs made by AlphaBeta with Dijkstra eval depth 4: ' + str(HexBoard.d4Cutoffs))
                print('Cutoffs made by ID with TT ' + str(TT.ttCutoffs))
            # break
                return "blue"
            if redPlayer == 1:
                    move_red = ab.alphabeta_moveR(board, depth=3, is_max=True)
            elif redPlayer == 2:
                    move_red = ab.alphabeta_move(board, depth=3, is_max=True)
                    HexBoard.dCutoffs += HexBoard.cutoffs
                    HexBoard.cutoffs = 0
            elif redPlayer == 3:
                    move_red = ab.alphabeta_move(board, depth=4, is_max=True)
                    HexBoard.d4Cutoffs += HexBoard.cutoffs
                    HexBoard.cutoffs = 0
            elif redPlayer == 4:
                 move_red = ttab.iterative_deepening(board, is_max=True, max_seconds=20)


            #move_red = ab.alphabeta_move(board, depth=3, is_max=True)
            #move_red = ab.alphabeta_move_Id(board, is_max=True, show_AI=True)
            board = ab._update_board(board, move_red, is_max=False) # Using false here and true for the alphabeta is a bit confusing, but we need it to make moves for red here.
            board.print()
            if board.is_game_over():  # TODO: add condition for game over without no winning (board full)
                HexBoard.total_dCutoffs += HexBoard.dCutoffs
                HexBoard.total_rCutoffs += HexBoard.rCutoffs
                HexBoard.total_d4Cutoffs += HexBoard.d4Cutoffs
                TT.total_ttCutoffs += TT.ttCutoffs
                print("==== RED WINS ====")
                board.print()
                print('Cutoffs made by AlphaBeta with random eval: ' + str(HexBoard.rCutoffs))
                print('Cutoffs made by AlphaBeta with Dijkstra eval depth 3: ' + str(HexBoard.dCutoffs))
                print('Cutoffs made by AlphaBeta with Dijkstra eval depth 4: ' + str(HexBoard.d4Cutoffs))
                print('Cutoffs made by ID with TT ' + str(TT.ttCutoffs))
            # break
                return "red"


if __name__ == '__main__':
#     #while 1:
     main()





