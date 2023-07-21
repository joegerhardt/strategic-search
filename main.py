import games
import random
import matplotlib.pyplot as plt
import numpy as np

#Every node is a distinct strategy
#This is a learning method for choosing the best strategy when the payoff matrix is unknown
#Later I will interperate nodes in dynamic games that are no longer distinct strategy and instead 'ideas'

true_probability_matrix_of_A_win = [[0.9, 0.4],
                                    [0.3, 0.8]]


class Player:
    def __init__(self, name):
        self.name = name
        self.strategies = []

    def __str__(self) -> str:
        return self.name



class Strategy:
    def __init__(self, id):
        self.id = id

        #every node vector could have a mean (true value) and uncertainty
        self.opponent_node_vectors = {}
        self.opponent_node_games = {}
        self.probability_to_play_according_to_opponent = 0

    def __str__(self) -> str:
        return str(self.id)



def print_choose_strategy(player, opponent):
    best_strategy = (None, -1000)
    for our_strategy in player.strategies:
        value = 0
        for opponent_strategy in opponent.strategies:
            value += our_strategy.opponent_node_vectors[opponent_strategy] * opponent_strategy.probability_to_play_according_to_opponent
        
        if value > best_strategy[1]:
            best_strategy = (our_strategy, value)
    print(player, best_strategy[0].id, best_strategy[0].probability_to_play_according_to_opponent, value)
    return best_strategy[0]


def choose_strategy(player, opponent):
    best_strategy = (None, -1000)
    for our_strategy in player.strategies:
        value = 0
        for opponent_strategy in opponent.strategies:
            value += our_strategy.opponent_node_vectors[opponent_strategy] * opponent_strategy.probability_to_play_according_to_opponent
        
        if value > best_strategy[1]:
            best_strategy = (our_strategy, value)
    return best_strategy[0]


def play(printer):

    #print()
    if(printer):
        A_strategy = print_choose_strategy(players['A'], players['B'])
        B_strategy = print_choose_strategy(players['B'], players['A'])
        print()
    else:
        #A_strategy = choose_strategy(players['A'], players['B'])
        if random.random() < 0.5:
            A_strategy = players['A'].strategies[0]
        else:
            A_strategy = players['A'].strategies[1]
        B_strategy = choose_strategy(players['B'], players['A'])

    A_picks.append(A_strategy.id)
    B_picks.append(B_strategy.id)

    
    #make players choose strategy

    

    #determine random outcome
    probability_A_wins = true_probability_matrix_of_A_win[A_strategy.id][B_strategy.id]

    #change value opponent probability based on your choice 

    if random.random() < probability_A_wins:
        #print('A wins')
        scores['A'] += 1
        A_strategy.opponent_node_vectors[B_strategy] = (A_strategy.opponent_node_vectors[B_strategy] * A_strategy.opponent_node_games[B_strategy] + 1) / (A_strategy.opponent_node_games[B_strategy] + 1)
        B_strategy.opponent_node_vectors[A_strategy] = (B_strategy.opponent_node_vectors[A_strategy] * B_strategy.opponent_node_games[A_strategy]) / (B_strategy.opponent_node_games[A_strategy] + 1)
        A_strategy.opponent_node_games[B_strategy] += 1
        B_strategy.opponent_node_games[A_strategy] += 1

        A_strategy.probability_to_play_according_to_opponent += 0.001
        players['A'].strategies[(A_strategy.id+1)%2].probability_to_play_according_to_opponent -= 0.001
        B_strategy.probability_to_play_according_to_opponent -= 0.001
        players['B'].strategies[(B_strategy.id+1)%2].probability_to_play_according_to_opponent += 0.001

    else:
        #print('B wins')
        scores['B'] += 1
        B_strategy.opponent_node_vectors[A_strategy] = (B_strategy.opponent_node_vectors[A_strategy] * B_strategy.opponent_node_games[A_strategy] + 1) / (B_strategy.opponent_node_games[A_strategy] + 1)
        B_strategy.opponent_node_vectors[B_strategy] = (A_strategy.opponent_node_vectors[B_strategy] * A_strategy.opponent_node_games[B_strategy]) / (A_strategy.opponent_node_games[B_strategy] + 1)
        A_strategy.opponent_node_games[B_strategy] += 1
        B_strategy.opponent_node_games[A_strategy] += 1

        B_strategy.probability_to_play_according_to_opponent += 0.001
        players['B'].strategies[(B_strategy.id+1)%2].probability_to_play_according_to_opponent -= 0.001
        A_strategy.probability_to_play_according_to_opponent -= 0.001
        players['A'].strategies[(A_strategy.id+1)%2].probability_to_play_according_to_opponent += 0.001

    #print()

        

    

    #adjust probability to play. Increase if they won with that strategy, decrease if they lost with that strategy



scores = {'A': 0, 'B': 0}

A_picks = []
B_picks = []

players = {'A': Player('A'), 'B': Player('B')}

players['A'].strategies.append(Strategy(0))
players['A'].strategies.append(Strategy(1))
players['B'].strategies.append(Strategy(0))
players['B'].strategies.append(Strategy(1))

games.game1(players['A'], players['B'])

for player in players.values():
    for strategy in player.strategies:
        strategy.probability_to_play_according_to_opponent = 0.5
        for opponent_strategy, value in strategy.opponent_node_vectors.items():
            print(player, strategy, opponent_strategy, value)




#must scale games
for i in range(1000000):
    if i % 100000 == 99:
        play(True)
    else:
        play(False)
print(scores)
x_values = [i for i in range(len(A_picks))]

#plt.plot(x_values, A_picks, B_picks)
#plt.show()

print('A picks:', 1-sum(A_picks)/len(A_picks), sum(A_picks)/len(A_picks))
print('B picks:', 1-sum(B_picks)/len(B_picks), sum(B_picks)/len(B_picks))

"""print('A')
for strategy in A_strategies:
    for opponent_strategy, value in strategy.opponent_node_vectors.items():
        print(value)

print('B')
for strategy in B_strategies:
    for opponent_strategy, value in strategy.opponent_node_vectors.items():
        print(value)"""
    



#scale is net winning/losing times / total number of iteratorions