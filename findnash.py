import nashpy as nash
import numpy as np

A = np.array([[9,4],[3,8]]) # A is the row player
B = np.array([[1,6],[7,2]]) # B is the column player

#9 * 0.4 + 4 * 0.6 = 6
#3 * 0.4 + 8 * 0.6 = 6
game1 = nash.Game(A,B)

print(game1)

equilibria = game1.support_enumeration()
for eq in equilibria:
    print(eq)