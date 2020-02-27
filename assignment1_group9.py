#### For now the file only contains the user input. To be expanded to the whole program

from hex_skeleton import HexBoard
import alphabeta as ab
import random

#TODO: Add a heuristic start strategy to speed up the beginning of the game!!!!

win_message = "******************************************\n\
*               YOU WIN                  *\n\
******************************************"

loss_message = "******************************************\n\
*              YOU LOSE                  *\n\
******************************************"

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
#             break
#         move_program = ab.alphabeta_move(board, 3, is_max=True)
#         board = ab._update_board(board, move_program, True)
#         board.print()
#         if board.is_game_over():  # TODO: add condition for game over without no winning (board full)
#             print(loss_message)
#             board.print()
#             break

##########################################################
#               CODE BLOCK FOR AI VS AI                  #
##########################################################

def main():
    board = HexBoard(3)
    num_of_cells = board.get_board_size() * board.get_board_size()
    for nc in range(int(num_of_cells/2)):
        ## Just a small heuristic for opening strategy, you can test this if you want. But then you have to comment the move_blue below out too
        # if board.size % 2 != 0 and len(board.get_move_list()) == len(board.get_all_vertices()): # If it's the first move and the board is uneven
        #     move_blue = (board.size // 2, board.size // 2) # Always place the first move in the middle
        # else:
            # move_blue = ab.alphabeta_move(board, depth=2, is_max=True)
        
        move_blue = ab.alphabeta_move(board, depth=2, is_max=True)
        #move_blue = ab.alphabeta_move_Id(board, is_max=True)
        board = ab._update_board(board, move_blue, is_max=True)
        board.print()
        if board.is_game_over(): # TODO: add condition for game over without no winning (board full)
            print("==== BLUE WINS ====")
            board.print()
            break
        move_red = ab.alphabeta_move(board, depth=2, is_max=True)
        #move_red = ab.alphabeta_move_Id(board, is_max=True)
        board = ab._update_board(board, move_red, is_max=False) # Using false here and true for the alphabeta is a bit confusing, but we need it to make moves for red here.
        board.print()
        if board.is_game_over():  # TODO: add condition for game over without no winning (board full)
            print("==== RED WINS ====")
            board.print()
            break


if __name__ == '__main__':
    #while 1:
    main()





