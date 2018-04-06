# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 14:02:19 2017

@author: Hanss401
"""


import numpy as np

def make_random_mat():
    mat = [];
    for i in range(300):
        #mat.append(list(np.random.beta(1,10,3) ).append(float(i%3)));
        y = [0.0,0.0,0.0];
        y[i%3] = 1.0;
        mat.append(list(np.random.beta(10,100,3) ) + y );
    #np.savetxt("train_data.txt", np.array(mat), fmt="%d", delimiter=",")    
    #np.savetxt('train_data.txt',np.array(mat),fmt='%.18e',delimiter=',');

    import csv
    csvfile = file('train_data.txt','a+')
    writer  = csv.writer(csvfile)
    for i in range(len(mat)):
    	#line = mat[i]+[float(i%3)];
    	# if i<10:
    	#    print line;
        #writer.writerow(line);
        writer.writerow(mat[i])
    csvfile.close() 

if __name__ == '__main__':
    make_random_mat();
