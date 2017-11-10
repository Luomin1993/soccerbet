import numpy as np
import scipy as sp
from MarkovForSoc import *
"""
O = [   3,         2,           1,              0]
ODD: win Total  win little   Lose little   Lose Total

O = [   2,         1,           0]
FOR: LL/LD/LW   DD/DL/WL      WW/WD/DW
"""
#I  = [0,0,-2,1,-2,-1,-2,-1,1,0,1]
#O  = [2,0,0,1, 1, 1, 2, 1,1,1,2]

# Levante vs Huesca
I1  = [ 1,-2, 0, 0, 1,-1, 2, 0, 2, 1]
I2  = [ 0, 1, 0, 0, 2,-2, 0,-2, 1, 0]
O1  = [ 3, 1, 3, 1, 3, 0, 1, 0, 3, 1]
O2  = [ 2, 1, 3, 1, 1, 0, 1, 1, 3, 3]
Op1 = [1]
Op2 = [2]

# Arsnal
# I  = [-1,-1,-1,-1, 1,-2,-1,-1,-2, 0,-2]
# O  = [0,1,2,2,2,1,1,2,2,2,1]


def makeModel(Pi,Q,V,O,I,Op):
    model    = MarkovForSoc(1)
    model.Pi = Pi
    model.Q  = Q
    model.V  = V
    model.train(O,I)
    return model


if __name__ == "__main__":
    model    = MarkovForSoc(1)
    model.Pi = [0.2,0.2,0.2,0.2,0.2]
    model.Q  = [2,1,0,-1,-2]
    model.V  = [3,2,1,0]
    model.train(O2,I2)
    Gamma = model.predict(Op2)
    print np.array(Gamma)
