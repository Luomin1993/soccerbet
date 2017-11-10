#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import spiderForBSBall as netdata
import TransDataForBS as trans
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
	#PGR      = trans.PG_to_R(Reses[0:len(Reses)-1])
	(PGR_g,PGR_l) = netdata.get_TeamGoalHistory(content)
    #del PGR_g[0];del PGR_g[1];del PGR_l[0];del PGR_l[1];
	if len(PGR_g)<20:
	   return -1
	PGO      = trans.ODD_to_O(Odds[0:len(Odds)])
	FOR      = trans.PG_to_O(np.array(PGR_g)-np.array(PGR_l))
	del PGR_g[0];del PGR_g[1];del PGR_l[0];del PGR_l[1];
	Mat      = trans.RFO_to_StaticMat(PGR_g,PGR_l,PGO,FOR)
	#print Mat
	for_now = trans.FOR(PGR_g[len(PGR_g)-2]-PGR_l[len(PGR_l)-2],PGR_g[len(PGR_g)-1]-PGR_l[len(PGR_l)-1])
	odd_now = trans.OD(lodd/wodd)
	print odd_now
	print for_now
	#return np.array(Mat[odd_now][for_now])
	rv      = Mat[odd_now][for_now]
	print '>>>>>>>>>>>>'
	print '胜赔: ' + str(wodd)
	print '进球期望: ' + str(rv.get_average_goal())
	print '失球期望: ' + str(rv.get_average_lose())
	print " --- "+ str(rv.get_pre_vec())  +" --- 置信度: " + str(rv.num_matches)

if __name__ == '__main__':
	#http://liansai.500.com/team/5230/teamfixture/
	#print getTeamMatDis("http://liansai.500.com/team/5230/")
	match_id  = sys.argv[1]
	m_match = spider.get_match(match_id)
	m_match.display()
	match_url = 'http://odds.500.com/fenxi/shuju-'+ str(match_id) +'.shtml'
	content   = spider.url_get(match_url,"gb2312")
	(home_url,away_url) = netdata.get_Team_url(content)
	odd_url   = 'http://odds.500.com/fenxi/ouzhi-'+ str(match_id) +'.shtml'
	content   = spider.url_get(odd_url,"gb2312")
	(wodd,lodd) = netdata.get_now_Odds(content)
	getTeamMatDis(home_url,wodd,lodd)
	getTeamMatDis(away_url,lodd,wodd)
	print '==============================================='
	print ' '
	print ' '
