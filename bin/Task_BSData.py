#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import spider
import re
import sys
import spiderForMarket as sm
from progressbar import *
import datetime
today = datetime.datetime.now()

__author__ = 'hanss401'

def notArrow_odds(turArr):
    Arr=[]
    for tur in turArr:
        for m in tur:
            if m != '':
               Arr.append(m.replace('↑','').replace('↓',''))    
    return Arr    

def getAppointBSOddsAndRes(match_id,company):
    url     = 'http://odds.500.com/fenxi/daxiao-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    #print content
    #title="伟德"><span class="
    content_r = re.compile(r'title="'+company+r'"><span class="(.*)')
    real_content = content_r.findall(content.replace('\r','').replace('\n',''))
    #">3.5</td>
    odds_r   = re.compile(r'class="ying">(.*?)</td>|class="ping">(.*?)</td>|class="shu">(.*?)</td>|class="">(.*?)</td>')  #odds
    res_r    = re.compile(r'<strong>(.*):(.*)</strong>')            #goals
    pan_r    = re.compile(r'class="tb_tdul_pan ">(.*?)</td>|class="tb_tdul_pan ying">(.*?)</td>|class="tb_tdul_pan ping">(.*?)</td>') #pan
    #print real_content[0]
    if real_content==[]:
       return 0
    odds     = notArrow_odds(odds_r.findall(real_content[0])[0:4])
    #odds     = odds_r.findall(real_content[0])[0:4]
    pans     = notArrow_odds(pan_r.findall(real_content[0])[0:2])
    res      = res_r.findall(content)
    if len(res)<1:
       return 0
    if len(res[0])<2:
       return 0   
    return (odds,pans,[res[0][0],res[0][1]])

def getAppointBSOddsAndRes_notstart(match_id,company):
    url     = 'http://odds.500.com/fenxi/daxiao-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    #print content
    #title="伟德"><span class="
    content_r = re.compile(r'title="'+company+r'"><span class="(.*)')
    real_content = content_r.findall(content.replace('\r','').replace('\n',''))
    #">3.5</td>
    odds_r   = re.compile(r'class="ying">(.*?)</td>|class="ping">(.*?)</td>|class="shu">(.*?)</td>|class="">(.*?)</td>')  #odds
    res_r    = re.compile(r'<strong>(.*):(.*)</strong>')            #goals
    pan_r    = re.compile(r'class="tb_tdul_pan ">(.*?)</td>|class="tb_tdul_pan ying">(.*?)</td>|class="tb_tdul_pan ping">(.*?)</td>') #pan
    #print real_content[0]
    if real_content==[]:
       return 0
    odds     = notArrow_odds(odds_r.findall(real_content[0])[0:4])
    #odds     = odds_r.findall(real_content[0])[0:4]
    pans     = notArrow_odds(pan_r.findall(real_content[0])[0:2])
    res      = res_r.findall(content)
    return (odds,pans,[0,0])    

def reTurpleToList(ListTur,wantedInTurple):
    Arr = []
    for tur in ListTur:
        Arr.append(tur[wantedInTurple])
    return Arr    


def getAppointASOddsAndRes(match_id,company):
    url     = 'http://odds.500.com/fenxi/yazhi-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    #everything_r--------
    company_r    = re.compile(r'<p><a href="http://(.*)" title="(.*)"><span class="(.*)"')
    res_r        = re.compile(r'<strong>(.*):(.*)</strong>')            #goals
    odds_away_r  = re.compile(r'<td row="(.*)" width="(.*)" class="(.*)">(.*)</td>')
    odds_home_r  = re.compile(r'<td width="(.*)"row="(.*)" class="(.*)">(.*)</td>')
    pan_r  = re.compile(r'row="(.*)" ref="(.*?)">(.*?)<')
    #Get-----------------
    CompaniesArr = reTurpleToList(company_r.findall(content),1)
    if company not in CompaniesArr:
       return 0
    OddsHomeArr  = reTurpleToList(odds_home_r.findall(content),3)
    OddsAwayArr  = reTurpleToList(odds_away_r.findall(content),3)
    PansArr      = reTurpleToList(pan_r.findall(content),2)
    #Find----------------   
    indexOfCom   = CompaniesArr.index(company)
    res          = res_r.findall(content)
    #(['0.77', '1.05', '2.40', '0.30'], ['2.5', '3.5'], ['2', '1'])
    #['1.000', '0.890', '0.700', '1.250'], ['\xe5\xb9\xb3\xe6\x89\x8b/\xe5\x8d\x8a\xe7\x90\x83', '\xe5\x8f\x97\xe5\xb9\xb3\xe6\x89\x8b/\xe5\x8d\x8a\xe7\x90\x83'], ['2', '1']
    return ([OddsHomeArr[2*indexOfCom].replace('↑','').replace('↓',''),OddsAwayArr[2*indexOfCom].replace('↑','').replace('↓',''),OddsHomeArr[2*indexOfCom+1],OddsAwayArr[2*indexOfCom+1]],[PansArr[2*indexOfCom],PansArr[2*indexOfCom+1]],[res[0][0],res[0][1]])        

def getAppointASOddsAndRes_notstart(match_id,company):
    url     = 'http://odds.500.com/fenxi/yazhi-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    #everything_r--------
    company_r    = re.compile(r'<p><a href="http://(.*)" title="(.*)"><span class="(.*)"')
    res_r        = re.compile(r'<strong>(.*):(.*)</strong>')            #goals
    odds_away_r  = re.compile(r'<td row="(.*)" width="(.*)" class="(.*)">(.*)</td>')
    odds_home_r  = re.compile(r'<td width="(.*)"row="(.*)" class="(.*)">(.*)</td>')
    pan_r  = re.compile(r'row="(.*)" ref="(.*?)">(.*?)<')
    #Get-----------------
    CompaniesArr = reTurpleToList(company_r.findall(content),1)
    if company not in CompaniesArr:
       return 0
    OddsHomeArr  = reTurpleToList(odds_home_r.findall(content),3)
    OddsAwayArr  = reTurpleToList(odds_away_r.findall(content),3)
    PansArr      = reTurpleToList(pan_r.findall(content),2)
    #Find----------------   
    indexOfCom   = CompaniesArr.index(company)
    res          = res_r.findall(content)
    #(['0.77', '1.05', '2.40', '0.30'], ['2.5', '3.5'], ['2', '1'])
    #['1.000', '0.890', '0.700', '1.250'], ['\xe5\xb9\xb3\xe6\x89\x8b/\xe5\x8d\x8a\xe7\x90\x83', '\xe5\x8f\x97\xe5\xb9\xb3\xe6\x89\x8b/\xe5\x8d\x8a\xe7\x90\x83'], ['2', '1']
    return ([OddsHomeArr[2*indexOfCom].replace('↑','').replace('↓',''),OddsAwayArr[2*indexOfCom].replace('↑','').replace('↓',''),OddsHomeArr[2*indexOfCom+1],OddsAwayArr[2*indexOfCom+1]],[PansArr[2*indexOfCom],PansArr[2*indexOfCom+1]],[0,0])        

def getOneWeddOdd(match_id):
    info = getAppointBSOddsAndRes_notstart(match_id,'伟德')
    if info==0:
       return 0
    return (np.float64(np.array((info[0]+info[2]))),info[1])

def getOneAomenOdd(match_id):
    info = getAppointASOddsAndRes_notstart(match_id,'澳门')
    if info==0:
       return 0
    return (np.float64(np.array((info[0]+info[2]))),info[1])

def getAppointASOddsAndRes_test():
    return getAppointASOddsAndRes('642942','伟德')

def getAppointBSOddsAndRes_test():
    return getAppointBSOddsAndRes('642942','伟德')

#------------- Every time one month ---------------
def AppSpiderWeddBSodds(month,lastday):
    Lines = []
    for day in range(1,min(10,lastday)):
    	match_ids = spider.crawl_match_list_by_date(str(today.year) + "-"+str(month)+"-0" + str(day))
        print '这一天是'+str(month)+'月'+str(day)+'日'
        print '当天共'+str(len(match_ids))+'场比赛,正在下载...'
        pbar = ProgressBar().start();i=1;total=len(match_ids);
        for match_id in match_ids:
            info = getAppointBSOddsAndRes(match_id,'伟德')
            if info==0:continue
            pbar.update(int(100*(float(i)/total)))
            Lines.append((np.float64(np.array((info[0]+info[2]))),info[1]))
            i+=1
        pbar.finish()
    if lastday<10:
        return Lines
    for day in range(10,lastday+1):
        match_ids = spider.crawl_match_list_by_date(str(today.year) + "-"+str(month)+"-" + str(day))
        print '这一天是'+str(month)+'月'+str(day)+'日'
        print '当天共'+str(len(match_ids))+'场比赛,正在下载...'
        pbar = ProgressBar().start();i=1;total=len(match_ids);
        for match_id in match_ids:
            info = getAppointBSOddsAndRes(match_id,'伟德')
            if info==0:continue
            pbar.update(int(100*(float(i)/total)))
            Lines.append((np.float64(np.array((info[0]+info[2]))),info[1]))
            i+=1
        pbar.finish()
    return Lines   

def AppSpiderAomenASodds(day1,day2):
    Lines = []
    for day in range(day1,day2):
        match_ids = spider.crawl_match_list_by_date(str(today.year) + "-11-0" + str(day))
        print '当天共'+str(len(match_ids))+'场比赛,正在下载...'
        pbar = ProgressBar().start();i=1;total=len(match_ids);
        for match_id in match_ids:
            info = getAppointASOddsAndRes(match_id,'澳门')
            if info==0:continue
            pbar.update(int(100*(float(i)/total)))
            Lines.append((np.float64(np.array((info[0]+info[2]))),info[1]))
            i+=1
        pbar.finish()
    return Lines       

def AppMakeAomenData(day1,day2):
    Lines = AppSpiderAomenASodds(day1,day2)
    np.save('AomenAS'+str(day1)+'-'+str(day2),Lines)

def AppUseAomenOdds(match_id):
    thisInfo = getOneAomenOdd(match_id)
    if thisInfo ==0:return 0
    #Infos    = np.load('AomenAS10-29.npy')
    Infos    = np.concatenate((np.load('AomenAS10-29.npy'),np.load('AomenAS1-5.npy')))
    for info in Infos:
        if abs(thisInfo[0][0]-info[0][0])<0.05 and abs(thisInfo[0][1]-info[0][1])<0.05 and abs(thisInfo[0][2]-info[0][2])<0.1 and abs(thisInfo[0][3]-info[0][3])<0.1 and thisInfo[1][0]==info[1][0] and thisInfo[1][1]==info[1][1]:
           print str(info[0][4])+':'+str(info[0][5]) +' --- '+ judgeASRes(info[0][4],info[0][5])

def judgeASRes(goal1,goal2):
    if goal1>goal2:
       return 'Win'
    if goal1==goal2:
       return 'Don'
    return 'Los'      


def AppSpiderWeddBSodds_test():
    Lines = AppSpiderWeddBSodds(12,13)
    for line in Lines:
    	print line

def AppMakeWeddData(month,lastday):
	Lines = AppSpiderWeddBSodds(month,lastday)
	np.save('Data_BS/WeddBS'+'-'+str(month),Lines)

def AppUseWeddOdds(match_id):
    thisInfo = getOneWeddOdd(match_id)
    if thisInfo ==0:return 0
    #Infos    = np.load('WeddBS10-20.npy')
    Infos    = np.concatenate((np.load('WeddBS10-28.npy'),np.load('WeddBS1-5.npy')))
    for info in Infos:
    	if abs(thisInfo[0][0]-info[0][0])<0.05 and abs(thisInfo[0][1]-info[0][1])<0.05 and abs(thisInfo[0][2]-info[0][2])<0.1 and abs(thisInfo[0][3]-info[0][3])<0.1 and thisInfo[1][0]==info[1][0] and thisInfo[1][1]==info[1][1]:
    	   print str(info[0][4])+':'+str(info[0][5]) +' --- '+ judgeBSRes(info[0][4],info[0][5])

def judgeBSRes(goal1,goal2):
	if goal1+goal2>2.5 and goal1+goal2>1.5:
	   return '大2.5 大1.5'
	if goal1+goal2<2.5 and goal1+goal2>1.5:   
	   return '      大1.5'
	return '小'   

if __name__ == '__main__':
    #print getAppointBSOddsAndRes_test()    
    #print getAppointASOddsAndRes_test()
    #AppSpiderWeddBSodds_test()
    #AppMakeAomenData(1,5)
    AppMakeWeddData(11,9)
    #AppMakeWeddData_thisMonth(11,9)
    #AppUseWeddOdds(sys.argv[1])
    #AppUseAomenOdds(sys.argv[1])
