import numpy as np
import scipy as sp
from MarkovForSoc import *
"""
O = [   3,         2,           1,              0]
ODD: win Total  win little   Lose little   Lose Total

I = [   3,         1,           0]
RES:   Win        Dawn         Lose


O = [   2,         1,           0]
FOR: LL/LD/DL   DD/LW/WL      WW/WD/DW
"""
#I  = [0,0,-2,1,-2,-1,-2,-1,1,0,1]
#O  = [2,0,0,1, 1, 1, 2, 1,1,1,2]

# Baoding vs Zhejiang
# I1  = [-1,-1,-1,-1, 1,-2,-1,-1,-2, 0,-2]
# I2  = [-1, 1,-2, 0, 0,-2, 3, 2, 0,-2, 0]
# O1  = [0,1,2,2,2,1,1,2,2,2,1]
# O2  = [0,1,1,1,1,1,2,1,0,0,1]
# Op1 = [2]
# Op2 = [1]

# Arsnal
I  = [-1,-1,-1,-1, 1,-2,-1,-1,-2, 0,-2]
O  = [0,1,2,2,2,1,1,2,2,2,1]


def makeModel(Pi,Q,V,O,I,Op):
    model    = MarkovForSoc(1)
    model.Pi = Pi
    model.Q  = Q
    model.V  = V
    model.train(O,I)
    return model

def makeAverageRes(O1,O2,I,known_O1,known_O2):
    mode1_1    = MarkovForSoc(1)
    mode1_1.Pi = [0.3333,0.3333,0.3333]
    mode1_1.Q    = [3,1,0]
    mode1_2    = mode1_1
    mode1_1.V  = [2,1,0]
    mode1_2.V  = [3,2,1,0]
    mode1_1.train(O1,I)
    mode1_2.train(O2,I)
    res1 = mode1_1.predict(known_O1)
    res2 = mode1_2.predict(known_O2)
    #print (res1,res2)
    return (np.array(res1)+np.array(res2))/2


# if __name__ == "__main__":
#     model    = MarkovForSoc(1)
#     model.Pi = [0.2,0.2,0.2,0.2,0.2]
#     model.Q  = [2,1,0,-1,-2]
#     model.V  = [2,1,0]
#     model.train(O2,I2)
#     Gamma = model.predict(Op2)
#     print np.array(Gamma)