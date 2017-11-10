import numpy as np
import spiderForTeamInfo as netdata
import TransDataForMK as trans
import MarkovDemo as mk
import sys
import spider
import pdb

def getTeamMatTest(team_url):
	content  = spider.url_get(team_url+'/teamfixture',"gb2312")
	Reses    = netdata.get_TeamMatchHistory(content)
	Odds     = netdata.get_TeamOddsHistory(content)
	if len(Reses)<20:
	   return -1
	PGR      = trans.PG_to_R(Reses[0:len(Reses)-2])
	PGO      = trans.ODD_to_O(Odds[0:len(Odds)-2])
	FOR      = trans.PG_to_O(Reses[0:len(Reses)-2])
	Mat      = trans.RFO_to_StaticMat(PGR,PGO,FOR)
	for_test = trans.FOR(Reses[len(Reses)-3],Reses[len(Reses)-2])
	odd_test = trans.OD(Odds[len(Reses)-1])
	res_test = trans.RS(Reses[len(Reses)-1])
	if Mat[odd_test][for_test].sum() == 0:
	   return -1 # stat lose;No data;
	elif Mat[odd_test][for_test][res_test]/Mat[odd_test][for_test].sum() >= 0.5:   
	   return 1  # positive instance;
	else:
	   return 0  # negative instance; 

def getTeamMatDis(team_url):
	content  = spider.url_get(team_url+'/teamfixture',"gb2312")
	Reses    = netdata.get_TeamMatchHistory(content)
	Odds     = netdata.get_TeamOddsHistory(content)
	if len(Reses)<20:
	   return -1
	PGR      = trans.PG_to_R(Reses[0:len(Reses)-2])
	PGO      = trans.ODD_to_O(Odds[0:len(Odds)-2])
	FOR      = trans.PG_to_O(Reses[0:len(Reses)-2])
	Mat      = trans.RFO_to_StaticMat(PGR,PGO,FOR)
	for_test = trans.FOR(Reses[len(Reses)-3],Reses[len(Reses)-2])
	odd_test = trans.OD(Odds[len(Reses)-1])
	res_test = trans.RS(Reses[len(Reses)-1])
	# print Reses
	# print Odds
	# print PGR
	# print PGO
	# print FOR
	# print (for_test,odd_test,res_test)
	print str(Mat[odd_test][for_test]) + ("  +++  ") + str(res_test) 


if __name__ == '__main__':
	#http://liansai.500.com/team/5230/teamfixture/
	#print getTeamMatDis("http://liansai.500.com/team/5230/")
	pos = 0
	neg = 0
	for i in range(5230,5331):
		url = "http://liansai.500.com/team/"+ str(i)
		res = getTeamMatTest(url)
		#print res
		if res == 1:
		   pos += 1
		if res == 0:
		   neg += 1
	print pos
	print neg
	print float(pos)/(pos+neg)      