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
import spiderForMarket as fm
import AppOddschangePre


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
    PGO      = trans.ODD_to_O_29(Odds[0:len(Odds)]) #1*29
    FOR      = trans.PG_to_O_29(np.array(PGR_g)-np.array(PGR_l)) #1*29
    del PGR_g[0];del PGR_l[0];del HA[0];
    Mat      = trans.RFOH_to_StaticMat(PGR_g,PGR_l,PGO,HA,FOR)
    #print Mat
    for_now = trans.FOR_29(PGR_g[len(PGR_g)-1]-PGR_l[len(PGR_l)-1])
    #print for_now
    odd_now = trans.OD(lodd/wodd)
    #ha_now  = 
    #print odd_now
    #print for_now
    #return np.array(Mat[odd_now][for_now])
    rv      = (Mat[odd_now][for_now][ha_now],wodd)
    # if rv:
    #     pass
    # print '>>>>>>>>>>>>'
    # print '胜赔: ' + str(wodd)
    # print '进球期望: ' + str(rv.get_average_goal())
    # print '失球期望: ' + str(rv.get_average_lose())
    # print " --- "+ str(rv.get_pre_vec())  +" --- 置信度: " + str(rv.num_matches)
    return rv

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

def showMarket(match_id):
    (betfair_indexes,boss_wl,betfair_suggest) = fm.getBetfairsth(match_id)
    (asia_odds,asia_num)                      = fm.getAsialot(match_id)
    (bs_odds,bs_num)                          = fm.getBslot(match_id)
    (kelly_index,back_lot)                    = fm.getKelly(match_id)
    print '============== 指数分析 ================'
    print '必发指数: '+betfair_indexes[0]+' '+betfair_indexes[1]+' '+betfair_indexes[2]
    print '庄家盈亏: '+boss_wl[0]+' '+boss_wl[1]+' '+boss_wl[2]
    print '         '+betfair_suggest[0]
    print '         '+betfair_suggest[1]
    print '         '+betfair_suggest[2]
    print '============== 亚盘盘口 ================'
    print '-----初始盘口:'
    print '澳门    : '+asia_odds[2]+'  '+asia_num[1]+'  '+asia_odds[3]
    print 'Bet365  : '+asia_odds[6]+'  '+asia_num[3]+'  '+asia_odds[7]
    print '皇冠    : '+asia_odds[10]+'  '+asia_num[5]+'  '+asia_odds[11]
    print '金宝博  : '+asia_odds[14]+'  '+asia_num[7]+'  '+asia_odds[15]
    print '香港马会: '+asia_odds[18]+'  '+asia_num[9]+'  '+asia_odds[19]
    print '-----即时盘口:'
    print '澳门    : '+asia_odds[0]+'  '+asia_num[0]+'  '+asia_odds[1]
    print 'Bet365  : '+asia_odds[4]+'  '+asia_num[2]+'  '+asia_odds[5]
    print '皇冠    : '+asia_odds[8]+'  '+asia_num[4]+'  '+asia_odds[9]
    print '金宝博  : '+asia_odds[12]+'  '+asia_num[6]+'  '+asia_odds[13]
    print '香港马会: '+asia_odds[16]+'  '+asia_num[8]+'  '+asia_odds[17]
    print '============== 大小盘口 ================'
    print '-----初始盘口:'
    print '澳门    : '+bs_odds[2]+'  '+bs_num[1]+'  '+bs_odds[3]
    print 'Bet365  : '+bs_odds[6]+'  '+bs_num[3]+'  '+bs_odds[7]
    print '皇冠    : '+bs_odds[10]+'  '+bs_num[5]+'  '+bs_odds[11]
    print '金宝博  : '+bs_odds[14]+'  '+bs_num[7]+'  '+bs_odds[15]
    print '香港马会: '+bs_odds[18]+'  '+bs_num[9]+'  '+bs_odds[19]
    print '-----即时盘口:'
    print '澳门    : '+bs_odds[0]+'  '+bs_num[0]+'  '+bs_odds[1]
    print 'Bet365  : '+bs_odds[4]+'  '+bs_num[2]+'  '+bs_odds[5]
    print '皇冠    : '+bs_odds[8]+'  '+bs_num[4]+'  '+bs_odds[9]
    print '金宝博  : '+bs_odds[12]+'  '+bs_num[6]+'  '+bs_odds[13]
    print '香港马会: '+bs_odds[16]+'  '+bs_num[8]+'  '+bs_odds[17]
    print '============== 凯利指数 ================'
    print '初始: '+'返还率: '+back_lot[0]+' '+'凯利: '+kelly_index[0]+' '+kelly_index[1]+' '+kelly_index[2]
    print '即时: '+'返还率: '+back_lot[1]+' '+'凯利: '+kelly_index[3]+' '+kelly_index[4]+' '+kelly_index[5]


def showOddsChangePre(match_id):
    (X_willian,y_willian) = (np.load('OddsChange0918-0926WillianHill.npy'),np.load('Res0918-0926.npy'))
    (X_bet365,y_bet365)   = (np.load('OddsChange0918-0926Bet365.npy'),np.load('Res0918-0926Bet365.npy'))
    x_will = fm.makeOddsOne(match_id,'威廉希尔')
    x_365  = fm.makeOddsOne(match_id,'Bet365')
    res_will = AppOddschangePre.findSimilarOdds(X_willian,y_willian,x_will)
    res_365  = AppOddschangePre.findSimilarOdds(X_bet365,y_bet365,x_365)
    print '============== 历史变赔 ================'
    if res_will!=[]:
        print '威廉希尔  : ' + str(res_will)
        print str(res_will.count(1)*1.0/len(res_will))+' '+str(res_will.count(0)*1.0/len(res_will))+' '+str(res_will.count(-1)*1.0/len(res_will))
    if res_365!=[]:
        print 'Bet365   : ' + str(res_365)
        print str(res_365.count(1)*1.0/len(res_365))+' '+str(res_365.count(0)*1.0/len(res_365))+' '+str(res_365.count(-1)*1.0/len(res_365))
    if res_365==[] and res_will==[]:
        print '无相似变赔'    
        

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
    if isStart(m_match.match_time):
       print '已经开赛'
       return 0
    m_match.display()
    match_url = 'http://odds.500.com/fenxi/shuju-'+ str(match_id) +'.shtml'
    content   = spider.url_get(match_url,"gb2312")
    WebSuggest = netdata.get_Suggest(content)
    (home_url,away_url) = netdata.get_Team_url(content)
    odd_url   = 'http://odds.500.com/fenxi/ouzhi-'+ str(match_id) +'.shtml'
    content   = spider.url_get(odd_url,"gb2312")
    (wodd,lodd) = netdata.get_now_Odds(content)
    (home_rv,home_rv_wodd)=getTeamMatDis(home_url,wodd,lodd,1)
    (away_rv,away_rv_wodd)=getTeamMatDis(away_url,lodd,wodd,0)
    print '==============================================='
    SelShow(home_rv,away_rv)
    show(home_rv,home_rv_wodd)
    show(away_rv,away_rv_wodd)
    print  '===============  澳门心水推荐  ================='
    print WebSuggest
    print '          '
    print '          '

def app(match_id):
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
    (home_rv,home_rv_wodd)=getTeamMatDis(home_url,wodd,lodd,1)
    (away_rv,away_rv_wodd)=getTeamMatDis(away_url,lodd,wodd,0)
    # if home_rv.num_matches==0 or away_rv.num_matches==0:
    #    print '          '
    #    print '          '
    #    return 0
    print '==============================================='
    SelShow(home_rv,away_rv)
    show(home_rv,home_rv_wodd)
    show(away_rv,away_rv_wodd)
    print  '===============  澳门心水推荐  ================='
    print WebSuggest
    showMarket(match_id)       
    showOddsChangePre(match_id)
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
    app(sys.argv[1])
    #test(sys.argv[1])
    #test(698120)
    #test_isStart(sys.argv[1])
    #showMarket(663190)