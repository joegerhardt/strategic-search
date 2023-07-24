import random

rock, paper, scissors, num_actions = 0, 1, 2, 3
regret_sum = [0 for _ in range(num_actions)]
strategy = [0 for _ in range(num_actions)]
strategy_sum = [0 for _ in range(num_actions)]
opp_strategy = [0.4, 0.3, 0.3]
score = 0

def getStrategy():
    normalizing_sum = 0
    for a in range(num_actions):
        strategy[a] =  max(regret_sum[a],0)
        normalizing_sum += strategy[a]
    for a in range(num_actions):
        if normalizing_sum > 0:
            strategy[a] /= normalizing_sum
        else:
            strategy[a] = 1 / num_actions
        strategy_sum[a] += strategy[a]
    return strategy


def getAction(strategy):
    r = random.random()
    cd = 0
    for a in range(num_actions):
        cd += strategy[a]
        if r < cd:
            return a
    

def train(iterations):
    action_utility = [0 for _ in range(num_actions)]
    score = 0
    for i in range(iterations):
        strategy = getStrategy()
        my_action = getAction(strategy)
        opp_action = getAction(opp_strategy)

        if (my_action - 1)%3 == opp_action:
            score += 1
        elif (my_action + 1)%3 == opp_action:
            score -= 1

        action_utility[opp_action] = 0
        action_utility[(opp_action+1)%3] = 1
        action_utility[(opp_action-1)%3] = -1

        for a in range(num_actions):
            regret_sum[a] += action_utility[a] - action_utility[my_action]

        
def getAverageStrategy():
    average_strategy = [0 for _ in range(num_actions)]
    normalizing_sum = 0
    for a in range(num_actions):
        normalizing_sum += strategy_sum[a]
    for a in range(num_actions):
        if normalizing_sum > 0:
            average_strategy[a] = strategy_sum[a] / normalizing_sum
        else:
            average_strategy[a] = 1 / num_actions
    return average_strategy

train(10)
print(getAverageStrategy())






