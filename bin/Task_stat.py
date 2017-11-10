import numpy as np
import pickle as pk

def makeHisList():
	input = open('history_data.pkl','rb')
	data  = pk.load(input)
	data_list = []
	for meta in data:
		data_list.append([meta[0],meta[1],meta[2][0],meta[2][1],meta[2][2],meta[3][0],meta[3][1],meta[3][2],meta[4],meta[5],meta[6],meta[7],meta[8],meta[9]])
	return data_list

def statSth():
	data  = makeHisList()
	total = float(len(data))
	#[n for n in range(1,100) if n%3==0]
	#------ home win -------
	num_home_win     = len([n for n in data if n[4]>0.2 and n[4]<0.5  ])
	num_home_win_did = len([n for n in data if n[4]>0.2 and n[4]<0.5 and n[12]-n[13]>=0])
	print 'home win:  '+str(num_home_win)+'  '+str(num_home_win_did)+'  '+str(float(num_home_win_did)/num_home_win)

if __name__ == '__main__':
	statSth()	
