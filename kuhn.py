import random
import time

PASS, BET, num_actions = 0, 1, 2
nodeMap = {}

class Node:
    def __init__(self):
        self.info_set = ""
        self.strategy = [0,0]
        self.regret_sum = [0,0]
        self.strategy_sum = [0,0]



    def getStrategy(self, realization_weight):
        normalizing_sum = 0
        for a in range(num_actions):
            self.strategy[a] =  max(self.regret_sum[a],0)
            normalizing_sum += self.strategy[a]
        for a in range(num_actions):
            if normalizing_sum > 0:
                self.strategy[a] /= normalizing_sum
            else:
                self.strategy[a] = 1 / num_actions
            self.strategy_sum[a] += realization_weight * self.strategy[a]
        return self.strategy
    


    def getAverageStrategy(self):
        average_strategy = [0 for _ in range(num_actions)]
        normalizing_sum = 0
        for a in range(num_actions):
            normalizing_sum += self.strategy_sum[a]
        for a in range(num_actions):
            if normalizing_sum > 0:
                average_strategy[a] = self.strategy_sum[a] / normalizing_sum
            else:
                average_strategy[a] = 1 / num_actions
        return average_strategy
    


    def __str__(self) -> str:
        return self.info_set + ": " + str(self.getAverageStrategy())
    


def train(iterations):
    cards = [1, 2, 3]
    util = 0
    for i in range(iterations):
        shuffle(cards)
        util += cfr(cards, "", 1, 1)
    print("Average game value:", util/iterations)
    


def shuffle(cards):
    for c1 in range(len(cards)-1,0,-1):
        c2 = random.randint(0,c1)
        tmp = cards[c1]
        cards[c1] = cards[c2]
        cards[c2] = tmp



def cfr(cards, history, p0, p1):
    plays = len(history)
    player = plays % 2
    opponent = 1 - player

    if plays > 1:
        terminal_pass = history[plays - 1] == "p"
        double_bet = history[-2:] == "bb"
        is_player_card_higher = cards[player] > cards[opponent]
        if terminal_pass:
            if history == "pp":
                return 1 if is_player_card_higher else -1
            else:
                return 1
        elif double_bet:
            return 2 if is_player_card_higher else -2

    info_set = str(cards[player]) + ": " + history

    try:
        node = nodeMap[info_set]
    except KeyError:
        node = Node()
        node.info_set = info_set
        nodeMap[info_set] = node

    strategy = node.getStrategy(p0 if player == 0 else p1)
    util = [0 for _ in range(num_actions)]
    nodeUtil = 0
    for a in range(num_actions):
        nextHistory = history + ("p" if a == 0 else "b")
        if player == 0:
            util[a] = cfr(cards, nextHistory, p0 * strategy[a], p1)
        else:
            util[a] = cfr(cards, nextHistory, p0 * strategy[a], p1)
        nodeUtil += strategy[a] + util[a]

    for a in range(num_actions):
        regret = util[a] - nodeUtil
        node.regret_sum[a] += (p1 if player == 0 else p0) * regret

    return nodeUtil


iterations = 100000
train(iterations)
for node in nodeMap.values():
    print(node, node.regret_sum)




    



"""possibles = {"[1, 2, 3]":0,
             "[1, 3, 2]":0,
             "[2, 1, 3]":0,
             "[2, 3, 1]":0,
             "[3, 1, 2]":0,
             "[3, 2, 1]":0}

for i in range(1_000_000):
    cards = [1,2,3]
    shuffle(cards)
    possibles[str(cards)]+=1

print(possibles)"""
