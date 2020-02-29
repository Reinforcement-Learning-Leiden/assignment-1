import numpy as np
import ttalphabeta as tt
import trueskill as ts
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import alphabeta as ab
from transposition_table import TranspositionTable as TT

from hex_skeleton import HexBoard

BOARD_SIZE_TTID: int = 4
BLUE_SEC_TO_THINK: int = 5
RED_SEC_TO_THINK: int = 5
NUMBER_OF_GAMES: int = 12


def main():
    board = HexBoard(BOARD_SIZE_TTID)
    num_of_cells = board.get_board_size() * board.get_board_size()
    TT.cutoffs = 0
    HexBoard.d4Cutoffs = 0
    TT.retrievedStates=0
    for _ in range(int(num_of_cells/2)):

        move_blue = tt.iterative_deepening(
            board, is_max=True, max_seconds=BLUE_SEC_TO_THINK, depth_lim=10, show_AI=False)
        board.place((move_blue), board.BLUE)
        board.print()
        if board.is_game_over():
            print("==== BLUE WINS ====")
            #TT.total_cutoffs+=TT.cutoffs
            TT.total_retrievedStates+=TT.retrievedStates
            print(TT.retrievedStates)
            print(TT.total_retrievedStates)
            board.print()
            return "blue"
        move_red = ab.alphabeta_move(
            board,depth=4, is_max=False, show_AI=False)
        board=ab._update_board(board, move_red, is_max=False)
        board.print()
        if board.is_game_over():
            print("==== RED WINS ====")
            #HexBoard.total_d4Cutoffs+=HexBoard.d4Cutoffs
           # print(HexBoard.total_d4Cutoffs)
            board.print()
            return "red"


if __name__ == '__main__':
    to_plot_x = []
    to_plot_blue = []
    to_plot_red = []
    #plot_d4cutoffs = []
    #plot_cutoffs = []
    plot_retrieved=[]
    plot_total_retrieved=[]

    # Create fresh ratings for both players
    blue = ts.Rating()
    red = ts.Rating()

    to_plot_x.append(0)
    to_plot_blue.append(blue.mu)
    to_plot_red.append(red.mu)

    for match in range(NUMBER_OF_GAMES):  # Play 12 games
        res = main()  # Main game loop
        if res == "blue":  # If blue won
            blue, red = ts.rate_1vs1(blue, red)
        elif res == "red":  # If red won
            red, blue = ts.rate_1vs1(red, blue)
            blue, red = ts.rate_1vs1(blue, red, drawn=True)

        to_plot_x.append(match)
        to_plot_blue.append(blue.mu)
        to_plot_red.append(red.mu)

        #BAR
        #plot_d4cutoffs.append(HexBoard.d4Cutoffs)
        #plot_cutoffs.append(TT.cutoffs)
        plot_retrieved.append(TT.retrievedStates)
        plot_total_retrieved.append(TT.total_retrievedStates)

############################################################################
        # BAR
    n_groups = 12
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
    rects1 = plt.bar(index, plot_retrieved, bar_width,
                     alpha=opacity,
                     color='b',
                     label='Retrieved States')

    rects2 = plt.bar(index + bar_width, plot_total_retrieved, bar_width,
                     alpha=opacity,
                     color='g',
                     label='Total retrieved states')



    plt2.xlabel('Game number')
    plt2.ylabel('number of retrieved states')
    plt2.title('###')
    plt2.xticks(index + bar_width, range(12))
    plt2.legend()

    plt2.tight_layout()
    plt2.savefig('IDTT.png')
    plt2.show()
############################################################
    plt.plot(to_plot_x, to_plot_blue)
    plt.plot(to_plot_x, to_plot_red)
    plt.xlabel("# of games")
    plt.ylabel("player rating")
    plt.savefig(f"idtt_ai_vs_ai_{np.random.randint(100)}.png")
