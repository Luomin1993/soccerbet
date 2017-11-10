import numpy as np
import scipy as sp

def calAlpha(Pi,B,O,A):
    Alpha = []
    for t in range(0,len(O)):
        line = []
        for i in range(0,len(Pi)):
            if t == 0:
               line.append(Pi[i]*B[i][O[t]])
               continue
            line.append(SigmaAlphaA[i]*B[i][O[t]])
        Alpha.append(line)
        SigmaAlphaA = []
        for i in range(0,len(Pi)):
            SigmaThis = 0
            for j in range(0,len(Pi)):
                SigmaThis = SigmaThis + Alpha[t][j]*A[j][i]
            SigmaAlphaA.append(SigmaThis)
    return np.array(Alpha)

def calBeta(Pi,B,O,A):
    Beta = np.zeros((len(O),len(Pi)))
    #Beta = np.zeros(len(O))
    #for t in range(len(O),0):
    t = len(O)-1
    while(t >= 0):
        line = []
        for i in range(0,len(Pi)):
            if t == len(O)-1:
               line.append(1)
            else:
               line.append(SigmaABBeta[i])
        Beta[t] = line
        SigmaABBeta = []
        for i in range(0,len(Pi)):
            SigmaThis = 0
            for j in range(0,len(Pi)):
                SigmaThis = SigmaThis + A[i][j]*B[i][O[t]]*Beta[t][j]
            SigmaABBeta.append(SigmaThis)
        print SigmaABBeta
        t = t-1
    return Beta

def calGamma(t,i,Pi,B,O,A):
    Alpha = calAlpha(Pi,B,O,A)
    Beta  = calBeta(Pi,B,O,A)
    SigmaAlphaBeta = 0
    for j in range(0,len(Pi)):
        SigmaAlphaBeta += Alpha[t][j]*Beta[t][j]
    return Alpha[t][i]*Beta[t][i]/SigmaAlphaBeta

def test_calBeta():
    Pi = [0.2,0.3,0.5]
    A  = [[0.5,0.1,0.4],[0.3,0.5,0.2],[0.2,0.2,0.6]]
    B  = [[0.5,0.5],[0.4,0.6],[0.7,0.3]]
    O  = [0,1,0,0,1,0,1,1]
    Beta = calBeta(Pi,B,O,A)
    print Beta

def test_calAlpha():
    Pi = [0.2,0.3,0.5]
    A  = [[0.5,0.1,0.4],[0.3,0.5,0.2],[0.2,0.2,0.6]]
    B  = [[0.5,0.5],[0.4,0.6],[0.7,0.3]]
    O  = [0,1,0,0,1,0,1,1]
    Alpha = calAlpha(Pi,B,O,A)
    print Alpha

def test_calGamma():
    t = 3
    Pi = [0.2,0.3,0.5]
    A  = [[0.5,0.1,0.4],[0.3,0.5,0.2],[0.2,0.2,0.6]]
    B  = [[0.5,0.5],[0.4,0.6],[0.7,0.3]]
    O  = [0,1,0,0,1,0,1,1]
    Gamma = []
    for i in range(0,3):
       Gamma.append(calGamma(t,i,Pi,B,O,A))
    print np.array(Gamma)


if __name__ == "__main__":
    test_calBeta()
    test_calAlpha()
    test_calGamma()
