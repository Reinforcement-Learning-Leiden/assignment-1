import trueskill as ts
import assignment1_group9 as game
from hex_skeleton import HexBoard
import matplotlib.pyplot as plt

#TODO: Implement trueskill to rank the AI

if __name__ == '__main__':
    #while 1:
    
    # FOR PLOT ADDED
    to_plot_x = []
    to_plot_blue = []
    to_plot_red = []
    
    final_results = []
    # Create fresh ratings for both players
    blue = ts.Rating()
    red = ts.Rating()

    # FOR PLOT ADDED
    to_plot_x.append(0)
    to_plot_blue.append(blue.mu)
    to_plot_red.append(red.mu)

    redWins = 0
    blueWins = 0
    dictionary={1:'AB with random eval depth 3',2:'AB with Dijkstra eval depth 3',3:'AB with Dijkstra eval depth 4'}

    print(
        'Choose blue player! (type 1 for depth 3 with random eval, type 2 for depth 3 with dijkstra, type 3 for depth 4 with dijkstra)')
    bluePlayer = int(input("Blue Player: "))
    print(
        'Choose red player! (type 1 for depth 3 with random eval, type 2 for depth 3 with dijkstra, type 3 for depth 4 with dijkstra)')
    redPlayer = int(input("Red Player: "))

    boardSize=int(input('Choose the size of the board: '))

    for _ in range(2): # Play 12 games
        print("GAME Number:" , str(_))
        res = game.main(bluePlayer,redPlayer,boardSize) # Main game loop
        if res == "blue": # If blue won
            blueWins+=1
            blue, red = ts.rate_1vs1(blue, red) # first rating is winner, second is loser
        elif res == "red": # If red won
            redWins+=1
            red, blue = ts.rate_1vs1(red, blue)
        else: # If the game somehow resulted in a draw
            blue, red = ts.rate_1vs1(blue, red, drawn=True)
            
        # FOR PLOT ADDED
        to_plot_x.append(_)
        to_plot_blue.append(blue.mu)
        to_plot_red.append(red.mu)

    plt.xlabel("# of games")
    plt.ylabel("player rating")
    plt.plot(to_plot_x, to_plot_blue)
    plt.plot(to_plot_x, to_plot_red)
     #plt.savefig('hist_type%d_vs_type%d.png' % (bluePlayer, redPlayer))
    plt.show()

    plt.savefig('hist_%s_vs_%s.png' % (dictionary[bluePlayer] , dictionary[redPlayer]))
        #plt.close()
        
    final_results.append("BLUE'S RANK: " + str(blue.mu))
    final_results.append("RED'S RANK: " + str(red.mu))
    print('Total cutoffs made by AlphaBeta with random eval: ' + str(HexBoard.total_rCutoffs))
    print('Total cutoffs made by AlphaBeta with Dijkstra eval depth 3: ' + str(HexBoard.total_dCutoffs))
    print('Total cutoffs made by AlphaBeta with Dijkstra eval depth 4: ' + str(HexBoard.total_d4Cutoffs))
    print('Execution time of AB with random eval: '+ str(HexBoard.rTime) + ' seconds')
    print('Execution time of AB with Dijkstra eval depth 3: ' + str(HexBoard.dTime) + ' seconds')
    print('Execution time of AB with Dijkstra eval depth 4: ' + str(HexBoard.d4Time) + ' seconds')


    f=open("results.txt" , "w+")

    f.write('Blue Player: '+dictionary[bluePlayer]+' VS Red Player: '+ dictionary[redPlayer]+'\n')
    f.write('Total cutoffs made by AlphaBeta with random eval: ' + str(HexBoard.total_rCutoffs) + '\n')
    f.write('Total cutoffs made by AlphaBeta with Dijkstra eval depth 3: ' + str(HexBoard.total_dCutoffs)+ '\n')
    f.write('Total cutoffs made by AlphaBeta with Dijkstra eval depth 4: ' + str(HexBoard.total_d4Cutoffs) + '\n')
    f.write('Execution time of AB with random eval: '+ str(HexBoard.rTime) + ' seconds \n')
    f.write('Execution time of AB with Dijkstra eval depth 3: ' + str(HexBoard.dTime) + ' seconds \n')
    f.write('Execution time of AB with Dijkstra eval depth 4: ' + str(HexBoard.d4Time) + ' seconds \n')
    f.write('Times Blue Player won: '+ str(blueWins)+', times Red Player won: '+ str(redWins)+ '\n')
    f.write("BLUE'S RANK: " + str(blue.mu))
    f.write("RED'S RANK: " + str(red.mu))
    f.close()

    print(final_results)
