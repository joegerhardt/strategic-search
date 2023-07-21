
def game1(A, B):
    A_len, B_len = len(A.strategies), len(B.strategies)

    #set dictionary to keep track of all A vs B games
    strategy_wins = {opposition:(0,0) for opposition in [(A_strat, B_strat) for A_strat in A.strategies for B_strat in B.strategies]}
    
    #downsides to this are draws are forgetten in data so a player that wants to play a risk_free drawish strategy -
    #can't tell the difference between a 50/50/0 win/loss/draw strategy and a 0/0/100 win/loss/draw strategy

    strategy_wins[(A.strategies[0], B.strategies[0])] = (5, 3)
    strategy_wins[(A.strategies[0], B.strategies[1])] = (4, 4)
    strategy_wins[(A.strategies[1], B.strategies[0])] = (3, 6)
    strategy_wins[(A.strategies[1], B.strategies[1])] = (4, 1)

    for players, value in strategy_wins.items():
        players[0].opponent_node_games[players[1]] = sum(value)
        players[1].opponent_node_games[players[0]] = sum(value)

        players[0].opponent_node_vectors[players[1]] = (value[0] - value[1])/max(1, sum(value))
        players[1].opponent_node_vectors[players[0]] = -(value[0] - value[1])/max(1, sum(value))

    
    
