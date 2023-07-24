import random

PASS, BET, num_actions = 0, 1, 2

class Node:
    def __init__(self):
        self.strategy = []
        self.regret_sum = []

    def getStrategy(self):
        normalizing_sum = 0
        for a in range(num_actions):
            self.strategy[a] =  max(self.regret_sum[a],0)
            normalizing_sum += self.strategy[a]
        for a in range(num_actions):
            if normalizing_sum > 0:
                self.strategy[a] /= normalizing_sum
            else:
                self.strategy[a] = 1 / num_actions
            self.strategy_sum[a] += self.strategy[a]
        return self.trategy