#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import spider
import re

__author__ = 'hanss401'

def get_Team_url(content):
	#<li><a class="hd_name" href="http://liansai.500.com/team/2440/" target="_blank">
	team_url_r = re.compile(r'<li><a class="hd_name" href="(.*)" target="_blank">')
	urls = team_url_r.findall(content)
	return(urls[0],urls[1])

def get_now_Odds(content):
	#<td row="1" width="33.3%" id="avwinc2">1.59</td>
	#<td row="1"   id="avlostc2">5.13</td>
	w_r = re.compile(r'<td row="1" width="33.3%" id="avwinc2">(.*)</td>')
	l_r = re.compile(r'<td row="1"   id="avlostc2">(.*)</td>')
	wodd = float(w_r.findall(content)[0])
	lodd = float(l_r.findall(content)[0])
	return(wodd,lodd)

def get_now_Odds_test():
	content = spider.url_get("http://odds.500.com/fenxi/ouzhi-632108.shtml","gb2312")
	print get_now_Odds(content)

def get_Team_url_test():
	content = spider.url_get("http://odds.500.com/fenxi/shuju-632108.shtml","gb2312")
	print get_Team_url(content)

def get_TeamName(content):
	team_name_info_r = re.compile(r'<title>[\s\S]*?</title>')
	# for m in team_name_info_r.finditer(content):
	# 	return m.group(1)
	#return ""
	return re.findall(r'\((.*)\)',re.findall(team_name_info_r,content)[0])	

def get_TeamName_test():
	content = spider.url_get("http://liansai.500.com/team/2440/","gb2312")
	#print content
	Name = get_TeamName(content)[0]
	print "%s" % (Name)

def get_TeamMatchHistory(content):
	team_match_history_r = re.compile(r'nbsp;\((.*)\)')
	WDL_History_r = re.compile(r'">(.*?)</span></span></td>')
	WG_History_r  = re.compile(r'>(\d+)</span>')
	#History_Arr  = []
	WDL_History   = []
	WG_History    = []
	LG_History    = []
	#print team_match_history_r.findall(content)
	for m in WDL_History_r.findall(content):
		#WDL_History.append(m)
		if re.compile(r'>(.*)').findall(m)[0] == '胜':
		   WDL_History.append(3)
		elif re.compile(r'>(.*)').findall(m)[0] == '平':
		   WDL_History.append(1)
		else:
		   WDL_History.append(0)      
	return list(reversed(WDL_History))

def get_TeamMatchHistory_test():
    """
    <span class="lblue">负</span>
    0:<span class="lred">1</span>
    <span class="lred">2</span>:1
    """
    content = spider.url_get("http://liansai.500.com/team/2440/teamfixture/","gb2312")
    #print str(content)
    History_Arr = get_TeamMatchHistory(content)
    # for m in History_Arr:
    # 	print re.compile(r'>(.*)').findall(m)[0]
    print History_Arr
    #return History_Arr

def get_TeamOddsHistory(content):
	#team_match_history_r = re.compile(r'nbsp;\((.*)\)')
	CONTEXT_r        = re.compile(r'<tbody class="jTrInterval his_table">(.*)<table class="ltable1" border="0" cellpadding="0" cellspacing="0">')
	Odds_History_r = re.compile(r'  >(.*)</span>')
	Odds_History   = Odds_History_r.findall(content)
	#print team_match_history_r.findall(content)
	move = 0
	Odds_num_History = []
	#print Odds_History
	while(move <= len(Odds_History)-1):
		if Odds_History[move] != '':
		    w = str(Odds_History[move])
		    l = str(Odds_History[move+2])
		    Odds_num_History.append(float(l)/float(w))
		else :
		    Odds_num_History.append(1.0)    
		move += 3      
	return Odds_num_History

def get_TeamOddsHistory_test():
    content = spider.url_get("http://liansai.500.com/team/2440/teamfixture/","gb2312")
    #print content
    History_Arr = get_TeamOddsHistory(content)
    print list(reversed(History_Arr))

def trans_History_to_GLArr(History_Arr):
	GoalArr = []
	LostArr = []
	for Str in History_Arr:
		res = re.compile(r'\d+').findall(Str)
		GoalArr.append(int(res[0]))
		LostArr.append(int(res[1]))
	return (GoalArr,LostArr)	

def trans_History_to_GLArr_test():
	History_Arr = get_TeamMatchHistory_test()
	print trans_History_to_GLArr(History_Arr)

if __name__ == '__main__':
	get_Team_url_test()
	#get_now_Odds_test()
	#get_TeamName_test()
	#get_TeamMatchHistory_test()
	#get_TeamOddsHistory_test()
	#trans_History_to_GLArr_test()	