import numpy as np
import scipy as sp

class MarkovForSoc(object):
    """docstring for MarkovForSoc"""
    Q  = []
    V  = []
    A  = []
    B  = []
    O  = []
    I  = []
    Pi = []
    def __init__(self, arg):
        super(MarkovForSoc, self).__init__()
        self.arg = arg

    def train(self,O,I):
        #self.O = O
        #self.I = I
        #N = len(V)
        self.A = np.zeros((len(self.Q),len(self.Q)))
        for i in range(0,len(self.Q)):
            for j in range(0,len(self.Q)):
                self.A[i][j] = self.ProbA(O,i,j)
        self.B = np.zeros((len(self.Q),len(self.V)))
        for j in range(0,len(self.Q)):
            for k in range(0,len(self.V)):
                self.B[j][k] = self.ProbB(O,I,k,j)

    def ProbA(self,O,i,j):
        numj = 0
        numi = 0
        for t in range(0,len(O)-1):
            if O[t] == self.Q[i]:
               numi += 1
               if O[t+1] == self.Q[j]:
                  numj += 1
        if numi == 0:
        	return 0
        return float(numj)/float(numi)       

    def ProbB(self,O,I,k,j):
        numk = 0
        numj = 0
        for t in range(0,len(O)):
            if I[t] == self.Q[j]:
               numj += 1
               if O[t] == self.V[k]:
                  numk += 1
        if numj == 0:
            return 0          
        return float(numk)/float(numj)

    def calAlpha(self,Pi,B,O,A):
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

    def calBeta(self,Pi,B,O,A):
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
                #at this for ending,SigmaThis is Beta[t-1][i]    
                SigmaABBeta.append(SigmaThis)
            #at this for ending,SigmaABBeta is Beta[t-1]    
            #print SigmaABBeta
            t = t-1
        return Beta    

    def calGamma(self,t,i,Pi,B,O,A):
        Alpha = self.calAlpha(Pi,B,O,A)
        Beta  = self.calBeta(Pi,B,O,A)
        SigmaAlphaBeta = 0
        for j in range(0,len(Pi)):
            SigmaAlphaBeta += Alpha[t][j]*Beta[t][j]
            #print Alpha[t][j]
            #print Beta[t][j]
        #print SigmaAlphaBeta    
        return Alpha[t][i]*Beta[t][i]/SigmaAlphaBeta               


    def predict(self,Op):
        Gamma = []
        for i in range(0,len(self.Q)):
            gamma_i = self.calGamma(0,i,self.Pi,self.B,Op,self.A)
            if gamma_i >0:
                Gamma.append(gamma_i)
                continue
            Gamma.append(1.0/3)
        return Gamma    
        