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
I1  = [-1,-1,-1,-1, 1,-2,-1,-1,-2, 0,-2]
I2  = [-1, 1,-2, 0, 0,-2, 3, 2, 0,-2, 0]
O1  = [0,1,2,2,2,1,1,2,2,2,1]
O2  = [0,1,1,1,1,1,2,1,0,0,1]
Op1 = [2]
Op2 = [1]

if __name__ == "__main__":
   model = MarkovForSoc(1)
   model.Pi = [0.2,0.2,0.2,0.2,0.2]
   model.Q  = [2,1,0,-1,-2]
   model.V  = [2,1,0]
   model.train(O2,I2)
   Gamma = model.predict(Op2)
   print np.array(Gamma)
