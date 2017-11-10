#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import spiderForBSBall as netdata
import TransDataForBS as trans
import MarkovDemo as mk
import sys
import spider
import pdb
import re
import datetime
import AppMark as mark

g_Treshold = 0.25
g_Treshold_goal = 0.5


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

def getTeamMatDis(team_url,wodd,lodd,ha_now):
    content  = spider.url_get(team_url+'/teamfixture',"gb2312")
    Reses    = netdata.get_TeamMatchHistory(content)  #1*30
    Odds     = netdata.get_TeamOddsHistory(content)   #1*30
    HA       = netdata.get_TeamHAHistory(content)     #1*30
    #PGR      = trans.PG_to_R(Reses[0:len(Reses)-1])
    (PGR_g,PGR_l) = netdata.get_TeamGoalHistory(content) #1*30
    #del PGR_g[0];del PGR_g[1];del PGR_l[0];del PGR_l[1];
    if len(PGR_g)<20:
       return -1
    PGO      = trans.ODD_to_O_29(Odds) #1*29
    FOR      = trans.PG_to_O_29(np.array(PGR_g)-np.array(PGR_l)) #1*29
    del PGR_g[0];del PGR_l[0];del HA[0];
    Mat      = trans.RFOH_to_StaticMat(PGR_g[0:len(PGR_g)-1],PGR_l[0:len(PGR_l)-1],PGO[0:len(PGO)-1],HA[0:len(HA)-1],FOR[0:len(FOR)-1])
    #print Mat
    for_now = FOR[-1]
    #print for_now
    odd_now = PGO[-1]
    #ha_now  = 
    #print odd_now
    #print for_now
    #return np.array(Mat[odd_now][for_now])
    rv      = Mat[odd_now][for_now][ha_now]
    # if rv:
    #     pass
    # print '>>>>>>>>>>>>'
    # print '胜赔: ' + str(wodd)
    # print '进球期望: ' + str(rv.get_average_goal())
    # print '失球期望: ' + str(rv.get_average_lose())
    # print " --- "+ str(rv.get_pre_vec())  +" --- 置信度: " + str(rv.num_matches)
    return (rv,wodd,int(PGR_g[-1]))

def show(rv,wodd):
    print '>>>>>>>>>>>>'
    print '胜赔: ' + str(wodd)
    print '进球期望: ' + str(rv.get_average_goal())
    print '失球期望: ' + str(rv.get_average_lose())
    print " --- "+ str(rv.get_pre_vec())  +" --- 置信度: " + str(rv.num_matches)

def show_nothing():
    print '不推荐投注!'

def show_BS(BigBall,SmaBall):
    print '大小球指示参考：'+' @大球界:'+str(BigBall)+'   @小球界:'+str(SmaBall)

def SelShow(home_rv,away_rv):
    print '>>>>>>>投注建议： '
    if (home_rv.num_matches==0 and away_rv.num_matches<3) or (home_rv.num_matches<3 and away_rv.num_matches==0):
       show_nothing()
       return
    if (home_rv.num_matches==0 and (not GoodVec(away_rv.get_pre_vec()))) or ((not GoodVec(home_rv.get_pre_vec())) and away_rv.num_matches==0):
       show_nothing()
       return
    # h_vec=home_rv.get_pre_vec()
    # a_vec=away_rv.get_pre_vec() 
    # print h_vec
    # print a_vec  
    # if(GoodVecs(home_rv.get_pre_vec(),away_rv.get_pre_vec())==3):
    #    print '>>>>>>>'
    #    print '     主队强势可追不败;'
    # if(GoodVecs(home_rv.get_pre_vec(),away_rv.get_pre_vec())==0):
    #    print '>>>>>>>'
    #    print '     客队强势可追不败;'   
    h=GoodVecs(home_rv.get_pre_vec(),away_rv.get_pre_vec())
    if h ==False :
       GoodVecs(home_rv.get_pre_vec(),away_rv.get_pre_vec())
    # print SureGoal(home_rv.get_average_goal(),away_rv.get_average_lose())
    # print home_rv.get_average_goal()
    # print away_rv.get_average_lose()
    if home_rv.num_matches!=0 and SureGoal(home_rv.get_average_goal(),away_rv.get_average_lose()):
        print '     主队波胆球数: '+ str(CalGoal((home_rv.get_average_goal()+away_rv.get_average_lose())/2)) +'球'   
    if away_rv.num_matches!=0 and SureGoal(away_rv.get_average_goal(),home_rv.get_average_lose()):
        print '     客队波胆球数: '+ str(CalGoal((away_rv.get_average_goal()+home_rv.get_average_lose())/2)) +'球'      
    BigBall = CalGoal(min(home_rv.get_average_goal(),away_rv.get_average_lose()))+CalGoal(min(away_rv.get_average_goal(),home_rv.get_average_lose()))   
    SmaBall = CalGoal(max(home_rv.get_average_goal(),away_rv.get_average_lose()))+CalGoal(max(away_rv.get_average_goal(),home_rv.get_average_lose()))   
    show_BS(BigBall,SmaBall)


def GoodVec(vec):
    if vec[0]<0.2 or vec[2]<0.2:
       return True
    return False 

def GoodVecs(vec1,vec2):
    if (vec1[0]<=g_Treshold and vec2[2]<=g_Treshold):
       print '>>>>>>>'
       print '     主队强势可追不败;'
       return 3
    if (vec1[2]<=g_Treshold and vec2[0]<=g_Treshold):
       print '>>>>>>>'
       print '     客队强势可追不败;'
       return 0   
    return False   

def SureGoal(goal1,goal2):
    if abs(goal2 - goal1)<g_Treshold_goal:
       return True
    return False   

def CalGoal(goal):
    return int(goal+0.3)

def test(match_id):
    #match_id  = sys.argv[1]
    m_match = spider.get_match(match_id)
    # if isStart(m_match.match_time):
    #    print '已经开赛'
    #    return 0
    m_match.display()
    match_url = 'http://odds.500.com/fenxi/shuju-'+ str(match_id) +'.shtml'
    content   = spider.url_get(match_url,"gb2312")
    WebSuggest = netdata.get_Suggest(content)
    (home_url,away_url) = netdata.get_Team_url(content)
    odd_url   = 'http://odds.500.com/fenxi/ouzhi-'+ str(match_id) +'.shtml'
    content   = spider.url_get(odd_url,"gb2312")
    (wodd,lodd) = netdata.get_now_Odds(content)
    (home_rv,home_rv_wodd,home_goal)=getTeamMatDis(home_url,wodd,lodd,1)
    (away_rv,away_rv_wodd,away_goal)=getTeamMatDis(away_url,lodd,wodd,0)
    print '==============================================='
    SelShow(home_rv,away_rv)
    show(home_rv,home_rv_wodd)
    show(away_rv,away_rv_wodd)
    print  '===============  澳门心水推荐  ================='
    print WebSuggest
    if home_rv.num_matches==0 or away_rv.num_matches==0:
       print '          '
       print '          '
       print '++++++++++++++++         REAL             ++++++++++++++++'
       print m_match.host_team+' '+str(home_goal)+':'+str(away_goal)+' '+m_match.guest_team
       print '          '
       print '          '
       return 0
    mark.showMarket(match_id)
    print '          '
    print '++++++++++++++++         REAL             ++++++++++++++++'
    print m_match.host_team+' '+str(home_goal)+':'+str(away_goal)+' '+m_match.guest_team
    print '          '
    print '          '



def isStart(match_time):
    #time = re.match(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})', match_time)
    #print match_time
    time = re.match(r'比赛时间(.*)-(.*)-(.*) (.*):(.*)', match_time)
    #print time.groups()
    #(m_year,m_month,m_day,m_hour,m_minute) = (time.groups()[0],time.groups()[1],time.groups()[2],time.groups()[3],time.groups()[4])
    now = datetime.datetime.now()
    now_time = re.match(r'(.*)-(.*)-(.*) (.*):(.*):(.*)',str(now))
    #print now_time.groups()
    #(now_year,now_month,now_day,now_hour,now_minute) = (now_time.groups()[0],now_time.groups()[1],now_time.groups()[2],now_time.groups()[3],now_time.groups()[4])
    # if int(m_year) >= int(now_year):
    #    if int(m_month) >= int(now_month):
    #       if int(m_day) >= int(now_day):
    #          if int(m_hour) >= int(now_hour):
    #             if int(m_minute) >= int(now_minute):
    #                return False
    # return True
    return compareTime(time.groups(),now_time.groups(),0) 

def compareTime(m_time,n_time,i):
    if m_time > n_time:
       return False
    if m_time < n_time:
       return True
    if i == len(m_time)-1:
       return True
    else:
       return compareTime(m_time,n_time,i+1)         

def test_isStart(match_id):
    #content = spider.url_get('http://odds.500.com/fenxi/shuju-642942.shtml',"gb2312")
    m_match = spider.get_match(match_id)
    print isStart(m_match.match_time)

if __name__ == '__main__':
    #app(sys.argv[1])
    test(sys.argv[1])
    #test(698120)
    #test_isStart(sys.argv[1])
