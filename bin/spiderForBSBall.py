#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import spider
import re

__author__ = 'hanss401'

#http://live.500.com/2h1.php
def getHistoryMatches():
    pass

#http://zx.500.com/zc/
def getRandom9():
    #亚</a> <a href="http://odds.500.com/fenxi/ouzhi-554113.shtml"
    content = spider.url_get("http://zx.500.com/zc/","gb2312")
    url_r = re.compile(r'亚</a> <a href="http://odds.500.com/fenxi/ouzhi-(.*).shtml"')
    Match_URLs = url_r.findall(content)
    return Match_URLs

def getRandom9_test():
    return getRandom9()

#http://odds.500.com/ouzhi.php?cid=0&type=2
def getMainMatches():
    #<a href="/fenxi/shuju-702834.shtml" target="_blank" id="link147">数据</a>
    #<td align="center"><a href="/fenxi/shuju-631067.shtml" target="_blank">数据
    content = spider.url_get("http://odds.500.com/ouzhi.php?cid=0&type=2","gb2312")
    #url_r = re.compile(r'<td align="center"><a href="/fenxi/shuju-(.*).shtml"')
    url_r = re.compile(r'</td><td align="center"><a href="/fenxi/shuju-(.?*).shtml" target="_blank">数据</a><br /><a href=')
    Match_URLs = url_r.findall(content)
    return Match_URLs[0]

def get_Team_url(content):
    #<li><a class="hd_name" href="http://liansai.500.com/team/2440/" target="_blank">
    team_url_r = re.compile(r'<li><a class="hd_name" href="(.*)" target="_blank">')
    urls = team_url_r.findall(content)
    return(urls[0],urls[1])

#http://live.500.com/zqdc.php
def getAllMatches():
    #href="http://odds.500.com/fenxi/shuju-657875.shtml">析</a>
    content = spider.url_get("http://live.500.com/zqdc.php","gb2312")
    #content = spider.url_get("http://live.500.com/2h1.php","gb2312")
    url_r = re.compile(r'href="//odds.500.com/fenxi/shuju-(.*?).shtml"')
    Match_URLs = url_r.findall(content)
    return Match_URLs

#http://live.500.com/zqdc.php
def getEuroMatches():
    #href="http://odds.500.com/fenxi/shuju-657875.shtml">析</a>
    #content = spider.url_get("http://live.500.com/zqdc.php","gb2312")
    content = spider.url_get("http://live.500.com/2h1.php","gb2312")
    url_r = re.compile(r'href="//odds.500.com/fenxi/shuju-(.*?).shtml"')
    Match_URLs = url_r.findall(content)
    return Match_URLs


def getAllMatches_test():
    print getAllMatches()

def get_TeamHAHistory(content):
    #<td class="td_lteam"><a href="http://liansai.500.com/team/841/"  target="_blank">库普斯</a></td>
    #<td class="td_lteam"><a href="http://liansai.500.com/team/2326/" style="color:#a00000" target="_blank">玛丽港</a></td>
    HA_r = re.compile(r'<td class="td_lteam">(.*)</a></td>')
    HA_info = HA_r.findall(content)
    find_r = re.compile(r'style="(.*)"')
    HA_history = []
    for m in HA_info:
        #print m
        if(find_r.findall(m)):
          HA_history.append(1)
          continue
        HA_history.append(0) 
    return list(reversed(HA_history[0:30]))     


def get_TeamHAHistory_test():
    content = spider.url_get("http://liansai.500.com/team/2440/teamfixture/","gb2312")
    print get_TeamHAHistory(content)
    print len(get_TeamHAHistory(content))

def get_Suggest(content):
    #<td colspan="3" class="td_one td_no4">　　英特杜古最近表现难言理想，再加上此前6次面对马利汉姆只录得3和3负的劣绩，英特杜古此行定徒劳。</td>
    team_url_r = re.compile(r'<td colspan="3" class="td_one td_no4">(.*)</td>')
    urls = team_url_r.findall(content)
    if urls==[]:
        return 'nothing'
    return urls[0]

def get_Suggest_test():
    url = "http://odds.500.com/fenxi/shuju-642942.shtml"
    content = spider.url_get(url,"gb2312")
    print get_Suggest(content)

def get_now_Odds(content):
    #<td row="1" width="33.3%" id="avwinc2">1.59</td>
    #<td row="1"   id="avlostc2">5.13</td>
    # w_r = re.compile(r'<td row="1" width="33.3%" id="avwinc2">(.*)</td>')
    #l_r = re.compile(r'<td row="1"   id="avlostc2">(.*)</td>')
    w_r = re.compile(r'<td row="1" width="33.3%" id="avwinj2">(.*)</td>')
    l_r = re.compile(r'<td row="1"   id="avlostj2">(.*)</td>')
    wodd = float(w_r.findall(content)[0])
    lodd = float(l_r.findall(content)[0])
    return(wodd,lodd)

def get_now_all_odds(content):
    #<td row="1" width="33.3%" id="avwinj2">2.31</td>
    #<td row="1" width="33.3%" id="avdrawj2">3.28</td>
    #<td row="1"   id="avlostj2">2.87</td>
    w_r = re.compile(r'<td row="1" width="33.3%" id="avwinj2">(.*)</td>')
    d_r = re.compile(r'<td row="1" width="33.3%" id="avdrawj2">(.*)</td>')
    l_r = re.compile(r'<td row="1"   id="avlostj2">(.*)</td>')
    wodd = float(w_r.findall(content)[0])
    dodd = float(d_r.findall(content)[0])
    lodd = float(l_r.findall(content)[0])
    return(wodd,dodd,lodd)

def get_now_Odds_test():
    content = spider.url_get("http://odds.500.com/fenxi/ouzhi-632108.shtml","gb2312")
    print get_now_Odds(content)

def get_Team_url_test():
    content = spider.url_get("http://odds.500.com/fenxi/shuju-632108.shtml","gb2312")
    print get_Team_url(content)

def get_TeamName(content):
    team_name_info_r = re.compile(r'<title>[\s\S]*?</title>')
    # for m in team_name_info_r.finditer(content):
    #     return m.group(1)
    #return ""
    return re.findall(r'\((.*)\)',re.findall(team_name_info_r,content)[0])    

def get_TeamName_test():
    content = spider.url_get("http://liansai.500.com/team/2440/","gb2312")
    #print content
    Name = get_TeamName(content)[0]
    print "%s" % (Name)

def Turarr2Numarr(Turarr):
    Numarr = []
    for m in Turarr:
        if m[0]=='':
           Numarr.append(float(m[1]))
        else:
           Numarr.append(float(m[0]))
    return Numarr       

def Strarr2Numarr(Strarr):
    Numarr = []
    for s in Strarr:
        Numarr.append(float(s))
    return Numarr    

def get_TeamGoalHistory(content):
    team_match_history_r = re.compile(r'nbsp;\((.*)\)')
    WDL_History_r = re.compile(r'">(.*?)</span></span></td>')
    #WG_History_r  = re.compile(r'>(\d+)</span>')
    D_goal_r      = re.compile(r'class="lgreen">(\d+)</span>:')
    W_goal_r      = re.compile(r'<span class="lred">(\d+)</span>')
    L_goal_r      = re.compile(r'</span>:(\d+)|(\d+):<span class')

    D_goal        = Strarr2Numarr(D_goal_r.findall(content))
    W_goal        = Strarr2Numarr(W_goal_r.findall(content))
    L_goal        = Turarr2Numarr(L_goal_r.findall(content))


    Goal_History  = []
    Lose_History  = []
    #print team_match_history_r.findall(content)
    index_wl = 0
    index_d  = 0
    for m in WDL_History_r.findall(content):
        #WDL_History.append(m)
        if re.compile(r'>(.*)').findall(m)[0] == '胜':
           Goal_History.append(W_goal[index_wl])
           Lose_History.append(L_goal[index_wl])
           index_wl +=1
        elif re.compile(r'>(.*)').findall(m)[0] == '负':
           Goal_History.append(L_goal[index_wl])
           Lose_History.append(W_goal[index_wl])
           index_wl +=1
        else:
           Goal_History.append(D_goal[index_d])
           Lose_History.append(D_goal[index_d])
           index_d  +=1       
    return (list(reversed(Goal_History)),list(reversed(Lose_History)))

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
    #     print re.compile(r'>(.*)').findall(m)[0]
    print History_Arr
    print len(History_Arr)

def get_TeamOddsHistory(content):
    #team_match_history_r = re.compile(r'nbsp;\((.*)\)')
    CONTEXT_r        = re.compile(r'<tbody class="jTrInterval his_table">(.*)<table class="ltable1" border="0" cellpadding="0" cellspacing="0">')
    Odds_History_r = re.compile(r'  >(.*)</span>')
    Odds_History   = Odds_History_r.findall(content)
    HA_history     = list(reversed(get_TeamHAHistory(content)))
    #print team_match_history_r.findall(content)
    move = 0
    Odds_num_History = []
    #print Odds_History
    move_HA = 0
    while(move <= len(Odds_History)-1):
        if Odds_History[move] != '':
            w = str(Odds_History[move])
            l = str(Odds_History[move+2])
            if HA_history[move_HA]==0:Odds_num_History.append(float(w)/float(l))
            else:Odds_num_History.append(float(l)/float(w))
        else :
            Odds_num_History.append(1.0)    
        move += 3      
        move_HA +=1
    return list(reversed(Odds_num_History))

def get_TeamOddsHistory_test():
    content = spider.url_get("http://liansai.500.com/team/2440/teamfixture/","gb2312")
    #print content
    History_Arr = get_TeamOddsHistory(content)
    print History_Arr
    print len(History_Arr)

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

def get_TeamGoalHistory_test():
    content = spider.url_get("http://liansai.500.com/team/2440/teamfixture/","gb2312")
    print get_TeamGoalHistory(content)
    print len(get_TeamGoalHistory(content)[0])
    print len(get_TeamGoalHistory(content)[1])    

if __name__ == '__main__':
    #get_Team_url_test()
    #get_now_Odds_test()
    #get_TeamName_test()
    #get_TeamMatchHistory_test()
    #get_TeamOddsHistory_test()
    #trans_History_to_GLArr_test()
    #get_TeamGoalHistory_test()    
    #get_Suggest_test()
    #get_TeamHAHistory_test()
    getAllMatches_test()
    #print getRandom9_test()
    #print getMainMatches()
