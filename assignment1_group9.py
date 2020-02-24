#### For now the file only contains the user input. To be expanded to the whole program

from hex_skeleton import HexBoard

def human_input(board): # TOASK: is it efficient to pass board as arguement? better way to retrieve board size?
    input_user = input("Your Turn: ")
    if ',' in input_user:
        x, y = input_user.split(',')
    else:
        x, y = input_user.split()
    x = int(x)
    y = int(y)
    if x in range(board.get_board_size()) and y in range(board.get_board_size()) :
        coordinates = (x, y)
        return coordinates
    else :
        print ('coordinates (', x, ',', y, ') are not in range')
        return

def main():
    board = HexBoard(3)
    human_input(board)

if __name__ == '__main__':
    #while 1:
    main()



