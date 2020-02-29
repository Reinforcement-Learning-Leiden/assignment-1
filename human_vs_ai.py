from hex_skeleton import HexBoard
import alphabeta as ab
import ttalphabeta as tt
import numpy as np
from ttalphabeta import BOARD_SIZE_TTID # Change board size in the ttalphabeta.py file

MAX_SECONDS_AI = 10
DEPTH_LIMIT_AI = np.inf
AB_DEPTH = 3

def main():
    TTID, AB, AB_RANDOM = choose_ai()
    print('the program plays Blue(LeftToRight) and the user plays Red(UpToButtom)')
    board = HexBoard(BOARD_SIZE_TTID)
    num_of_cells = board.get_board_size() * board.get_board_size()
    for nc in range(int(num_of_cells/2)):
        move_human = human_input(board.get_board_size())
        while not move_human in board.get_move_list():
            print('move is not legal, please choose another cell')
            move_human = human_input(board.get_board_size())
        board.place(move_human, board.RED)
        board.print()
        if board.is_game_over(): 
            print(win_message)
            board.print()
            # print('Cutoffs: '+str(HexBoard.cutoffs))
            break
        if TTID:
            move_program = tt.iterative_deepening(board, True, max_seconds=MAX_SECONDS_AI, depth_lim=DEPTH_LIMIT_AI, show_AI=False)
        if AB:
            move_program = ab.alphabeta(board, depth=AB_DEPTH, alpha=-np.inf, beta=np.inf, is_max=True)
        board.place(move_program, board.BLUE)
        board.print()
        if board.is_game_over(): 
            print(loss_message)
            board.print()
            print('Cutoffs: ' + str(HexBoard.cutoffs))
            break








def choose_ai():
    AB, TTID = False, False
    input_user = input("1) Basic Alpha-Beta\n2) TTID Alpha-Beta\nYour choice: ")
    if input_user == "1":
        AB = True
    elif input_user == "2":
        TTID = True
    else:
        print(f"\nThe input {input_user} is invalid, please enter 1 or 2")
        choose_ai()
    return AB, TTID

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

win_message = "******************************************\n\
*               YOU WIN                  *\n\
******************************************"

loss_message = "******************************************\n\
*              YOU LOSE                  *\n\
******************************************"

if __name__ == '__main__':
#     #while 1:
     main()