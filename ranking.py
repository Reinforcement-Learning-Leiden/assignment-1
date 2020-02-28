import trueskill as ts
import assignment1_group9 as game
from hex_skeleton import HexBoard

#TODO: Implement trueskill to rank the AI

if __name__ == '__main__':
    #while 1:
    final_results = []
    # Create fresh ratings for both players
    blue = ts.Rating()
    red = ts.Rating()


    print(
        'Choose blue player! (type 1 for depth 3 with random eval, type 2 for depth 3 with dijkstra, type 3 for depth 4 with dijkstra')
    bluePlayer = int(input("Blue Player: "))
    print(
        'Choose red player! (type 1 for depth 3 with random eval, type 2 for depth 3 with dijkstra, type 3 for depth 4 with dijkstra')
    redPlayer = int(input("Red Player: "))

    for _ in range(3): # Play 12 games
        res = game.main(bluePlayer,redPlayer) # Main game loop
        if res == "blue": # If blue won
            blue, red = ts.rate_1vs1(blue, red) # first rating is winner, second is loser
        elif res == "red": # If red won
            red, blue = ts.rate_1vs1(red, blue)
        else: # If the game somehow resulted in a draw
            blue, red = ts.rate_1vs1(blue, red, drawn=True)
    final_results.append("BLUE'S RANK: " + str(blue.mu))
    final_results.append("RED'S RANK: " + str(red.mu))
    print('Total cutoffs made by AlphaBeta with random eval: ' + str(HexBoard.total_rCutoffs))
    print('Total cutoffs made by AlphaBeta with Dijkstra eval: ' + str(HexBoard.total_dCutoffs))
    
    print(final_results)