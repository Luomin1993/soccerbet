#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import numpy as np
import spiderForBSBall as netdata
import TransDataForBS as trans
import MarkovDemo as mk
import sys
import spider
import pdb
import re
import BScalculate as BSc
import datetime
today = datetime.datetime.now()

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

# def getTeamMatDis(team_url,wodd,lodd):
#     content  = spider.url_get(team_url+'/teamfixture',"gb2312")
#     Reses    = netdata.get_TeamMatchHistory(content)
#     Odds     = netdata.get_TeamOddsHistory(content)
#     #PGR      = trans.PG_to_R(Reses[0:len(Reses)-1])
#     (PGR_g,PGR_l) = netdata.get_TeamGoalHistory(content)
#     #del PGR_g[0];del PGR_g[1];del PGR_l[0];del PGR_l[1];
#     if len(PGR_g)<20:
#        return -1
#     PGO      = trans.ODD_to_O(Odds[0:len(Odds)])
#     FOR      = trans.PG_to_O(np.array(PGR_g)-np.array(PGR_l))
#     del PGR_g[0];del PGR_g[1];del PGR_l[0];del PGR_l[1];
#     Mat      = trans.RFO_to_StaticMat(PGR_g,PGR_l,PGO,FOR)
#     #print Mat
#     for_now = trans.FOR(PGR_g[len(PGR_g)-2]-PGR_l[len(PGR_l)-2],PGR_g[len(PGR_g)-1]-PGR_l[len(PGR_l)-1])
#     odd_now = trans.OD(lodd/wodd)
#     #print odd_now
#     #print for_now
#     #return np.array(Mat[odd_now][for_now])
#     rv      = (Mat[odd_now][for_now],wodd)
#     # if rv:
#     #     pass
#     # print '>>>>>>>>>>>>'
#     # print '胜赔: ' + str(wodd)
#     # print '进球期望: ' + str(rv.get_average_goal())
#     # print '失球期望: ' + str(rv.get_average_lose())
#     # print " --- "+ str(rv.get_pre_vec())  +" --- 置信度: " + str(rv.num_matches)
#     return rv

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
    #print '>>>>>>>>>>>>'
    print '胜赔: ' + str(wodd)
    print '进球期望: ' + str(rv.get_average_goal())
    print '失球期望: ' + str(rv.get_average_lose())
    print " --- "+ str(rv.get_pre_vec())  +" --- 置信度: " + str(rv.num_matches)

def show_nothing():
    print '不推荐投注!'

def show_BS(BigBall,SmaBall):
    print '大小球指示参考：'+' @大球界:'+str(BigBall)+'   @小球界:'+str(SmaBall)

def SelShow(home_rv,away_rv):
    # #print '>>>>>>>投注建议： '
    # if (home_rv.num_matches==0 and away_rv.num_matches<3) or (home_rv.num_matches<3 and away_rv.num_matches==0):
    #    show_nothing()
    #    return
    # if (home_rv.num_matches==0 and (not GoodVec(away_rv.get_pre_vec()))) or ((not GoodVec(home_rv.get_pre_vec())) and away_rv.num_matches==0):
    #    show_nothing()
    #    return
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
    #MySuggest=GoodVecs(home_rv.get_pre_vec(),away_rv.get_pre_vec())
    #if h ==False :
    #   GoodVecs(home_rv.get_pre_vec(),away_rv.get_pre_vec())
    # print SureGoal(home_rv.get_average_goal(),away_rv.get_average_lose())
    # print home_rv.get_average_goal()
    # print away_rv.get_average_lose()
    # if home_rv.num_matches!=0 and SureGoal(home_rv.get_average_goal(),away_rv.get_average_lose()):
    #     print '     主队波胆球数: '+ str(CalGoal((home_rv.get_average_goal()+away_rv.get_average_lose())/2)) +'球'   
    # if away_rv.num_matches!=0 and SureGoal(away_rv.get_average_goal(),home_rv.get_average_lose()):
    #     print '     客队波胆球数: '+ str(CalGoal((away_rv.get_average_goal()+home_rv.get_average_lose())/2)) +'球'      
    BigBall = CalGoal(min(home_rv.get_average_goal(),away_rv.get_average_lose()))+CalGoal(min(away_rv.get_average_goal(),home_rv.get_average_lose()))   
    SmaBall = CalGoal(max(home_rv.get_average_goal(),away_rv.get_average_lose()))+CalGoal(max(away_rv.get_average_goal(),home_rv.get_average_lose()))   
    #return (BigBall,SmaBall,MySuggest)
    return (BigBall,SmaBall,MySuggest)


def GoodVec(vec):
    if vec[0]<0.2 or vec[2]<0.2:
       return True
    return False 

def GoodVecs(vec1,vec2):
    if (vec1[0]<=g_Treshold and vec2[2]<=g_Treshold):
       #print '>>>>>>>'
       #print '     主队强势可追不败;'
       return 3
    if (vec1[2]<=g_Treshold and vec2[0]<=g_Treshold):
       print '>>>>>>>'
       #print '     客队强势可追不败;'
       return 0   
    return 99   

#w_Treshold
def GiveSuggest(homeodd,awayodd,vec1,vec2):
    w_Treshold=0.5
    l_Treshold=0.26
    if homeodd<awayodd:
       if vec1[2]>w_Treshold and vec2[0]>w_Treshold:
          return 'h3'
       if vec1[2]<l_Treshold and vec2[0]<l_Treshold:
          return 'h0'
    if homeodd>awayodd:
       if vec2[2]>w_Treshold and vec1[0]>w_Treshold:
          return 'a3'
       if vec2[2]<l_Treshold and vec1[0]<l_Treshold:
          return 'a0'
    return '99'      

def SureGoal(goal1,goal2):
    if abs(goal2 - goal1)<g_Treshold_goal:
       return True
    return False   

def CalGoal(goal):
    return int(goal+0.3)

def test(match_id):
    #match_id  = sys.argv[1]
    m_match = spider.get_match(match_id)
    m_match.display()
    match_url = 'http://odds.500.com/fenxi/shuju-'+ str(match_id) +'.shtml'
    content   = spider.url_get(match_url,"gb2312")
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
    print '          '
    print '          '

def toRedis(match_id,pool):
    m_match = spider.get_match(match_id)
    match_url = 'http://odds.500.com/fenxi/shuju-'+ str(match_id) +'.shtml'
    content   = spider.url_get(match_url,"gb2312")
    WebSuggest = netdata.get_Suggest(content)
    (home_url,away_url) = netdata.get_Team_url(content)
    odd_url   = 'http://odds.500.com/fenxi/ouzhi-'+ str(match_id) +'.shtml'
    content   = spider.url_get(odd_url,"gb2312")
    (wodd,lodd) = netdata.get_now_Odds(content)
    #(home_rv,home_rv_wodd)=getTeamMatDis(home_url,wodd,lodd)
    #(away_rv,away_rv_wodd)=getTeamMatDis(away_url,lodd,wodd)
    (home_rv,home_rv_wodd,home_goal)=getTeamMatDis(home_url,wodd,lodd,1)
    (away_rv,away_rv_wodd,away_goal)=getTeamMatDis(away_url,lodd,wodd,0)
    #print '==============================================='
    #(BigBall,SmaBall,MySuggest)=SelShow(home_rv,away_rv)
    #show(home_rv,home_rv_wodd)
    #show(away_rv,away_rv_wodd)
    home_vec = home_rv.get_pre_vec()
    away_vec = away_rv.get_pre_vec()
    if home_rv.num_matches<2 or away_rv.num_matches<2:
       return 0
    MySuggest = GiveSuggest(wodd,lodd,home_vec,away_vec) 
    (BigBall,SmaBall)=BSc.CalGoal(home_rv.get_average_goal(),home_rv.get_average_lose(),away_rv.get_average_goal(),away_rv.get_average_lose())  
    match_dict = {"web":m_match.match_link, 
                  "name":m_match.match_name, 
                  "hometeam":m_match.host_team, 
                  "awayteam":m_match.guest_team, 
                  "time":m_match.match_time,
                  "homeodd":str(wodd),
                  "awayodd":str(lodd),
                  "homenum":str(home_rv.num_matches),
                  "awaynum":str(away_rv.num_matches),
                  "homepregoal":str(home_rv.get_average_goal()),
                  "awaypregoal":str(away_rv.get_average_goal()),
                  "homeprelose":str(home_rv.get_average_lose()),
                  "awayprelose":str(away_rv.get_average_lose()),
                  "biggoal":str(BigBall),
                  "smagoal":str(SmaBall),
                  "hpl":str(home_vec[0]),
                  "hpd":str(home_vec[1]),
                  "hpw":str(home_vec[2]),
                  "apl":str(away_vec[0]),
                  "apd":str(away_vec[1]),
                  "apw":str(away_vec[2]),
                  "websuggest":WebSuggest,
                  "mysuggest":MySuggest,
                  "homerealgoal":str(home_goal),
                  "awayrealgoal":str(away_goal)}  
    #pool = redis.ConnectionPool(host='127.0.0.1',port=6379)
    #pool = redis.ConnectionPool(host='115.28.138.54',port=6379)
    rd   = redis.StrictRedis(connection_pool=pool)
    rd.hmset(match_id,match_dict)            
    print 'id writed: '+match_id
    return 'writed'    

def notOver(content):
    #<p class="odds_hd_bf"><strong>2:1</strong></p>
    #<p class="odds_hd_bf"><strong>VS</strong></p>
    over_url_r = re.compile(r'<p class="odds_hd_bf"><strong>(.*)</strong></p>')
    urls = over_url_r.findall(content)
    if urls[0]=="VS":
       return True
    return False   

def WritePre(match_id):
    match_url = 'http://odds.500.com/fenxi/shuju-'+ str(match_id) +'.shtml'
    content   = spider.url_get(match_url,"gb2312")
    if notOver(content):
       toRedis(match_id)

#def WriteRes()
def useOnePool(m_match_ids):
    #pool = redis.ConnectionPool(host='115.28.138.54',port=6379)
    pool = redis.ConnectionPool(host='127.0.0.1',port=6379)
    for match_id in m_match_ids:
        toRedis(match_id,pool)

def TestMultiMatches(how_many_days_ago):
    #pool = redis.ConnectionPool(host='115.28.138.54',port=6379)
    pool = redis.ConnectionPool(host='127.0.0.1',port=6379)
    m_match_ids = spider.crawl_match_list_by_date(str(today.year) + "-" + str(today.month) + "-" + str(today.day-how_many_days_ago))
    print len(m_match_ids)
    match_ids_writed = []
    for match_id in m_match_ids:
        if toRedis(match_id,pool)!=0:
           match_ids_writed.append(match_id)
    return match_ids_writed       


if __name__ == '__main__':
    #WritePre(sys.argv[1])
    #test(698120)
    #m_match_ids = ['663190','663189','663191','663194']
    print TestMultiMatches(2)