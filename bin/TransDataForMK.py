#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np

def PG_to_I(PG):
    I = []
    for i in range(2,len(PG)):
        if PG[i] > 2:
           I.append(2)
        elif PG[i] < -2:
           I.append(-2)
        else:
           I.append(PG[i])
    return I

def PG_to_R(PG):
    R = []
    for i in range(2,len(PG)):
        if PG[i] > 0:
           R.append(2)
        elif PG[i] < 0:
           R.append(0)
        else:
           R.append(1)
    return R

#PGR: Transfered Results:[0,1,3]
#PGO: Transfered Odds:[0,1,2,3]
#FOR: Transfered For:[0,1,2]
def RFO_to_StaticMat(PGR,PGO,FOR):
    Mat = np.zeros((4,3,3))
    # print PGR
    # print PGO
    # print FOR
    for i in range(0,len(PGR)):
    	#stat = [win_num,de_num,loss_num,total_num]
    	#stat = [0,0,0]
    	# if PGR[i]==2 :
    	#    Mat[PGO[i]][FOR[i]][2] += 1
    	# if PGR[i]==1 :
    	#    Mat[PGO[i]][FOR[i]][1] += 1
    	# if PGR[i]==0 :
    	#    Mat[PGO[i]][FOR[i]][0] += 1
    	Mat[PGO[i]][FOR[i]][PGR[i]] += 1
    return Mat	          


def RS_to_I(Res):
    del(Res[0])
    del(Res[0])
    return Res

def IF_ZERO(n):
    if n == 0:
       return 0
    else:
       return -n/n  

def FOR(n1,n2):
    if (n1<=0 and n2<=0) and (n1 != n2):
        return 2
    if (n1==0 and n2==0) or (n1<0 and n2>0) or (n1>0 and n2<0):
        return 1
    else:
        return 0        

def RS(res):
	if res>0:
	   return 2
	if res<0:
	   return 0
	else:
	   return 1      	

def OD(odd):
    if odd > 2:
        return 3
    elif odd < 0.5:
        return 0
    elif odd>=1 and odd<=2:
        return 2
    else:
        return 1             

def Res_310_to_210(Reses):
	Res = []
	for res in Reses:
		if res == 3:
		   Res.append(2)
		elif res == 1:
		   Res.append(1)
		elif res == 0:
		   Res.append(0)

def Res_310_to_210_cut2(Reses):
	del Reses[0]
	del Reses[0]
	Res = []
	for res in Reses:
		if res == 3:
		   Res.append(2)
		elif res == 1:
		   Res.append(1)
		elif res == 0:
		   Res.append(0)


def FOR_2(n1,n2):
    if ((n1<=0 and n2<=0) and (n1 != n2)) or (n1>0 and n2<0):
        return 1
    else:
        return 0        

def OD_2(odd):
    if odd>1:
        return 1
    else:
        return 0             


def PG_to_O(PG):
    O = []
    for i in range(2,len(PG)):
        O.append( FOR(PG[i-2],PG[i-1]) )
    return O                     

def ODD_to_O(ODD):
    O = []
    for i in range(2,len(ODD)):
        O.append( OD(ODD[i]) )
    return O    

def PG_to_I_test():
    PG = [-1,4,-3,-1,3,0,2,0,1,3,-2]
    print PG_to_I(PG)    

def PG_to_O_test():
    PG = [-1,4,-3,-1,3,0,2,0,1,3,-2]
    print PG_to_O(PG)    

def ODD_to_O_test():
    ODD = [2.676470588235294, 1.04296875, 1.6990291262135921, 1.5446009389671362, 2.8682634730538923, 2.6959064327485383, 0.7586206896551725, 1.4761904761904763, 1.0, 1.0671936758893281, 2.2307692307692304, 1.8040201005025125, 4.880281690140845, 0.8644688644688644, 2.0210526315789474, 2.204301075268817, 1.7386934673366834, 4.14569536423841, 0.77, 3.9600000000000004, 1.2198275862068966, 5.727941176470588, 1.483568075117371, 3.2611464968152863, 4.590277777777779, 0.8586956521739132, 2.5764705882352943, 3.067484662576687, 1.8102564102564103, 1.6911764705882353]
    print ODD_to_O(ODD)

def PG_to_R_test():
    PG = [-1,4,-3,-1,3,0,2,0,1,3,-2]
    print PG_to_R(PG)

def RFO_to_StaticMat_test():
    PG  = [-1,4,-3,-1,3,0,2,0,1,3,-2]
    ODD = [2.8682634730538923, 2.6959064327485383, 0.7586206896551725, 1.4761904761904763, 1.0, 1.0671936758893281, 2.2307692307692304, 1.8040201005025125, 4.880281690140845, 0.8644688644688644, 2.02105263157] 
    PGO = ODD_to_O(ODD)
    PGR = PG_to_R(PG)
    FOR = PG_to_O(PG)
    print RFO_to_StaticMat(PGR,PGO,FOR) 

if __name__ == '__main__':
    #PG_to_I_test()
    #PG_to_O_test()
    #ODD_to_O_test()
    #PG_to_R_test()
    RFO_to_StaticMat_test()