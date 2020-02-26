#### For now the file only contains the user input. To be expanded to the whole program

from hex_skeleton import HexBoard
import alphabeta as ab
import random

win_message = "******************************************\n\
*               YOU WIN                  *\n\
******************************************"

loss_message = "******************************************\n\
*              YOU LOSE                  *\n\
******************************************"

def human_input(size_of_board): # TOASK: is it efficient to pass board as arguement? better way to retrieve board size?
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

# For the moment the program generates random moves without considering alfabeta
def move_generator_random(size_of_board):
    x =  random.randint(0, size_of_board-1)
    y = random.randint(0, size_of_board-1)
    coordinates = (x, y)
    return coordinates

def main():
    print('the program plays Blue(LeftToRight) and the user plays Red(UpToButtom)')
    board = HexBoard(4)
    num_of_cells = board.get_board_size() * board.get_board_size()
    for nc in range(int(num_of_cells/2)):
        move_human = human_input(board.get_board_size())
        while not move_human in board.get_move_list():
            print('move is not legal, please choose another cell')
            move_human = human_input(board.get_board_size())
        board = ab._update_board(board, move_human ,False)
        board.print()
        if board.is_game_over(): # TODO: add condition for game over without no winning (board full)
            print(win_message)
            board.print()
            break
        move_program = ab.alphabeta_move(board, 3)
        board = ab._update_board(board, move_program, True)
        board.print()
        if board.is_game_over():  # TODO: add condition for game over without no winning (board full)
            print(loss_message)
            board.print()
            break


if __name__ == '__main__':
    #while 1:
    main()





