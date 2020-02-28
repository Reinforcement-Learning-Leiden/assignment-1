import trueskill as ts
import assignment1_group9 as game
from hex_skeleton import HexBoard
from transposition_table import TranspositionTable as TT

#TODO: Implement trueskill to rank the AI

if __name__ == '__main__':
    #while 1:
    final_results = []
    # Create fresh ratings for both players
    blue = ts.Rating()
    red = ts.Rating()

    redWins = 0
    blueWins = 0
    dictionary={1:'AB with random eval depth 3',2:'AB with Dijkstra eval depth 3',3:'AB with Dijkstra eval depth 4',4:',ID with TT'}

    print(
        'Choose blue player! (type 1 for depth 3 with random eval, type 2 for depth 3 with dijkstra, type 3 for depth 4 with dijkstra, type 4 for ID with TT)')
    bluePlayer = int(input("Blue Player: "))
    print(
        'Choose red player! (type 1 for depth 3 with random eval, type 2 for depth 3 with dijkstra, type 3 for depth 4 with dijkstra, type 4 for ID with TT)')
    redPlayer = int(input("Red Player: "))

    for _ in range(2): # Play 12 games
        res = game.main(bluePlayer,redPlayer) # Main game loop
        if res == "blue": # If blue won
            blueWins+=1
            blue, red = ts.rate_1vs1(blue, red) # first rating is winner, second is loser
        elif res == "red": # If red won
            redWins+=1
            red, blue = ts.rate_1vs1(red, blue)
        else: # If the game somehow resulted in a draw
            blue, red = ts.rate_1vs1(blue, red, drawn=True)
    final_results.append("BLUE'S RANK: " + str(blue.mu))
    final_results.append("RED'S RANK: " + str(red.mu))
    print('Total cutoffs made by AlphaBeta with random eval: ' + str(HexBoard.total_rCutoffs))
    print('Total cutoffs made by AlphaBeta with Dijkstra eval depth 3: ' + str(HexBoard.total_dCutoffs))
    print('Total cutoffs made by AlphaBeta with Dijkstra eval depth 4: ' + str(HexBoard.total_d4Cutoffs))
    print('Total cutoffs made by ID with TT: ' + str(TT.total_ttCutoffs))
    print('Execution time of AB with random eval: '+ str(HexBoard.rTime) + ' seconds')
    print('Execution time of AB with Dijkstra eval depth 3: ' + str(HexBoard.dTime) + ' seconds')
    print('Execution time of AB with Dijkstra eval depth 4: ' + str(HexBoard.d4Time) + ' seconds')
    print('Execution time of ID with TT: ' + str(TT.ttTime) + ' seconds')


    f=open("results.txt" , "w+")

    f.write('Blue Player: '+dictionary[bluePlayer]+' VS Red Player: '+ dictionary[redPlayer]+'\n')
    f.write('Total cutoffs made by AlphaBeta with random eval: ' + str(HexBoard.total_rCutoffs) + '\n')
    f.write('Total cutoffs made by AlphaBeta with Dijkstra eval depth 3: ' + str(HexBoard.total_dCutoffs)+ '\n')
    f.write('Total cutoffs made by AlphaBeta with Dijkstra eval depth 4: ' + str(HexBoard.total_d4Cutoffs) + '\n')
    f.write('Total cutoffs made by ID with TT: ' + str(TT.total_ttCutoffs))
    f.write('Execution time of AB with random eval: '+ str(HexBoard.rTime) + ' seconds \n')
    f.write('Execution time of AB with Dijkstra eval depth 3: ' + str(HexBoard.dTime) + ' seconds \n')
    f.write('Execution time of AB with Dijkstra eval depth 4: ' + str(HexBoard.d4Time) + ' seconds \n')
    f.write('Execution time of ID with TT: ' + str(TT.ttTime) + ' seconds')
    f.write('Times Blue Player won: '+ str(blueWins)+', times Red Player won: '+ str(redWins)+ '\n')
    f.write("BLUE'S RANK: " + str(blue.mu))
    f.write("RED'S RANK: " + str(red.mu))
    f.close()

    print(final_results)