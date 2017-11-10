#!/usr/bin/env python
# -*- coding: utf-8 -*-


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

def getTeamMatDis(team_url,wodd,lodd):
	content  = spider.url_get(team_url+'/teamfixture',"gb2312")
	Reses    = netdata.get_TeamMatchHistory(content)
	Odds     = netdata.get_TeamOddsHistory(content)
	if len(Reses)<20:
	   return -1
	PGR      = trans.PG_to_R(Reses[0:len(Reses)-1])
	PGO      = trans.ODD_to_O(Odds[0:len(Odds)-1])
	FOR      = trans.PG_to_O(Reses[0:len(Reses)-1])
	Mat      = trans.RFO_to_StaticMat(PGR,PGO,FOR)
	#print Mat
	for_now = trans.FOR(Reses[len(Reses)-2],Reses[len(Reses)-1])
	odd_now = trans.OD(lodd/wodd)
	#print odd_now
	return np.array(Mat[odd_now][for_now])


if __name__ == '__main__':
	#http://liansai.500.com/team/5230/teamfixture/
	#print getTeamMatDis("http://liansai.500.com/team/5230/")
	match_id  = sys.argv[1]
	match_url = 'http://odds.500.com/fenxi/shuju-'+ str(match_id) +'.shtml'
	content   = spider.url_get(match_url,"gb2312")
	(home_url,away_url) = netdata.get_Team_url(content)
	odd_url   = 'http://odds.500.com/fenxi/ouzhi-'+ str(match_id) +'.shtml'
	content   = spider.url_get(odd_url,"gb2312")
	(wodd,lodd) = netdata.get_now_Odds(content)
	res_home = getTeamMatDis(home_url,wodd,lodd)
	res_away = getTeamMatDis(away_url,lodd,wodd)
	if sum(res_home)!=0:
		p_home   = res_home/sum(res_home)
	else:
	    p_home   = np.array([0,0,0])	
	if sum(res_away)!=0:
		p_away   = res_away/sum(res_away)
	else:
	    p_away   = np.array([0,0,0])	
	#p_away   = res_away/sum(res_away)
	print "Home:  --- "+ str(p_home)  +" 置信度: " + str(sum(res_home))
	#print np.array(res_home)/sum(res_home)
	print "Away:  --- "+ str(p_away)  +" 置信度: " + str(sum(res_away))
	#print np.array(res_away)/sum(res_away)