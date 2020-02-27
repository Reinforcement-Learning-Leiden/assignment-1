import trueskill as ts
import assignment1_group9 as game

#TODO: Implement trueskill to rank the AI

if __name__ == '__main__':
    #while 1:
    final_results = []
    # Create fresh ratings for both players
    blue = ts.Rating()
    red = ts.Rating()

    for _ in range(12): # Play 12 games
        res = game.main() # Main game loop
        if res == "blue": # If blue won
            blue, red = ts.rate_1vs1(blue, red) # first rating is winner, second is loser
        elif res == "red": # If red won
            red, blue = ts.rate_1vs1(red, blue)
        else: # If the game somehow resulted in a draw
            blue, red = ts.rate_1vs1(blue, red, drawn=True)
    final_results.append("BLUE'S RANK: " + str(blue.mu))
    final_results.append("RED'S RANK: " + str(red.mu))
    
    print(final_results)