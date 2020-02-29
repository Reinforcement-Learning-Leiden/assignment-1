# Reinforcement Learning 2020 Assignment 1
## Group 9
### Julius Cathalina, Faezeh Amou, Georgios Tzimitras

## If you're not sure you have all the right packages, remember to run
### pip install -r requirements.txt

# Important files:
### ranking.py
- Contains the scripts and experiments for all the non-transposition table alphabeta search implementations
- Contains parameters that you can modify to adjust e.g. the AI search depth

### idtt_ranking.py
- Contains the scripts and experiments for the transposition table / iterative deepening alphabeta search
- Use 'ttalphabeta.py' if you want to change the board size (TTID_BOARD_SIZE), this is done to perserve consistency between the zobrist table and the board across files.
- You can use the parameters to set the time limit, depth search limit of the AI.

### human_vs_ai.py
- Lets you play against either the TTID variant or the normal alphabeta variant
- Option 1 is against the normal, Option 2 is against TTID
