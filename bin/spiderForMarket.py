#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import spider
import re
import sys

__author__ = 'hanss401'

#----------------------------------------------------
#http://odds.500.com/fenxi/touzhu-697026.shtml
def getBetfairsth(match_id):
    #anasys_url = 'http://odds.500.com/fenxi/touzhu-'+str(match_id)+'.shtml'
    betfair_indexes = getBetfair_test(match_id) #1*3
    boss_wl         = getBosswl_test(match_id)     #1*3
    betfair_suggest = getBetfairSug_test(match_id) #1*3 words
    return (betfair_indexes,boss_wl,betfair_suggest)

def getAnasys_test():
    match_id = 697026


def getBetfair_test(match_id):
    url     = 'http://odds.500.com/fenxi/touzhu-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    index_r = re.compile(r'<td>(.*)</td>')
    indexes = index_r.findall(content)
    index_w = indexes.index('盈亏指数')
    return [indexes[index_w+9],indexes[index_w+18],indexes[index_w+28]]

def getBetfairSug_test(match_id):
    url     = 'http://odds.500.com/fenxi/touzhu-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    index_r = re.compile(r'<td colspan="10">(.*)</td>')
    indexes = index_r.findall(content)
    #index_w = indexes.index('数据提点')
    return [indexes[0].replace('<em class="ying">','').replace('<em class="shu">','').replace('</em>',''),indexes[1].replace('<em class="ying">','').replace('<em class="shu">','').replace('</em>',''),indexes[2].replace('<em class="ying">','').replace('<em class="shu">','').replace('</em>','')]    
    #return indexes[0].replace('<em class="ying">','').replace('<em class="shu">','').replace('</em>','')

def getBosswl_test(match_id):
    url     = 'http://odds.500.com/fenxi/touzhu-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    index_r = re.compile(r'<td>(.*)</td>')
    indexes = index_r.findall(content)
    index_w = indexes.index('盈亏指数')
    return [indexes[index_w+10],indexes[index_w+19],indexes[index_w+29]]

#---------------------------------------------------
#http://odds.500.com/fenxi/yazhi-697026.shtml
def getAsialot(match_id):
    #asia_url   = 'http://odds.500.com/fenxi/yazhi-'+str(match_id)+'.shtml'
    asia_odds   = getAsiaOdds_test(match_id)   #1*20
    asia_num    = getAsiaLotnum_test(match_id) #1*10
    return (asia_odds,asia_num)

def getAsiaOdds_test(match_id):
    url     = 'http://odds.500.com/fenxi/yazhi-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    index_r = re.compile(r'class="ying">(.*)</td>|class="ping">(.*)</td>|class="shu">(.*)</td>|class="">(.*)</td>')
    indexes = notEm_Aodds(index_r.findall(content)[0:25])
    return indexes

def getAsiaLotnum_test(match_id):
	#<td row="1" ref="-0.250" class="">平手/半球</td>
	#row="1" ref="-0.250">平手/半球</td>
	#row="1" ref="1.250">受一球/球半<font color="blue"> 降</font></td>
	#ref="1.000" class="">受一球</td>
	#row="1" ref="0.000">平手<font color="red"> 升</font></td>
    url     = 'http://odds.500.com/fenxi/yazhi-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    #index_r = re.compile(r'0">(.*)</td>|0" class="">(.*)</td>')
    index_r = re.compile(r'row="1" (.*)0">(.*)</td>|<td row="1"(.*)0" class="">(.*)</td>')
    indexes = notEm_x(index_r.findall(content)[0:10])
    return indexes

#http://odds.500.com/fenxi/ouzhi-663188.shtml
def getOriAndNowOdds(match_id):
    #onclick="OZ.r(this)" style="cursor:pointer" > 2.50</td>
    url     = 'http://odds.500.com/fenxi/ouzhi-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    #index_r = re.compile(r'0">(.*)</td>|0" class="">(.*)</td>')
    index_r = re.compile(r'style="cursor:pointer" >(.*)</td>')
    #index_r = re.compile(r'style="cursor:pointer"(.*)</td>')
    indexes = index_r.findall(content)[0:6]
    return indexes
    #return float(np.array(indexes))

def getOriAndNowOdds_Res(match_id):
    #onclick="OZ.r(this)" style="cursor:pointer" > 2.50</td>
    #<strong>0:0</strong>
    url     = 'http://odds.500.com/fenxi/ouzhi-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    #index_r = re.compile(r'0">(.*)</td>|0" class="">(.*)</td>')
    index_r = re.compile(r'style="cursor:pointer" >(.*)</td>')
    res_r   = re.compile(r'<strong>(.*):(.*)</strong>')
    #index_r = re.compile(r'style="cursor:pointer"(.*)</td>')
    indexes = index_r.findall(content)[0:6]
    res     = res_r.findall(content)
    if len(res)<1:
       return 0
    if len(res[0])<2:
       return 0   
    return (indexes,[res[0][0],res[0][1]])

#Company_Dic = {'WillianHill':}
#http://odds.500.com/fenxi/touzhu-697025.shtml
def getAppointOddsAndRes(match_id,company):
    url     = 'http://odds.500.com/fenxi/ouzhi-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    #index_r = re.compile(r'0">(.*)</td>|0" class="">(.*)</td>')
    content_r = re.compile(company+r'<span class="gray">(.*)')
    #content_r = re.compile(r'(.*)'+company)
    real_content = content_r.findall(content.replace('\r','').replace('\n',''))
    #print real_content
    index_r   = re.compile(r'style="cursor:pointer" >(.*?)</td>\t')
    #index_r   = re.compile(r'style="cursor:pointer" >(.*)</td>\t              <td row="1" width="33.3%"  klfc="0.12"   onclick="OZ.r(this)" style="cursor:pointer" >(.*)</td>\t              <td row="1"   klfc="14.41" \t\t\t   onclick="OZ.r(this)" style="cursor:pointer" >(.*)</td>\t            </tr>\t            <tr>\t              <td row="1" width="33.3%"  klfc="1.12" class="" onclick="OZ.r(this)" style="cursor:pointer" >(.*)</td>\t              <td row="1" width="33.3%"  klfc="3.38" class="bg-a" onclick="OZ.r(this)" style="cursor:pointer" >(.*)</td>\t              <td row="1" klfc="36.28"                class="bg-b" onclick="OZ.r(this)" style="cursor:pointer" >(.*)</td>')
    res_r     = re.compile(r'<strong>(.*):(.*)</strong>')
    indexes = index_r.findall(real_content[0])[0:6]
    #print indexes
    res     = res_r.findall(content)
    if len(res)<1:
       return 0
    if len(res[0])<2:
       return 0   
    return (indexes,[res[0][0],res[0][1]])

def getAppointOdds(match_id,company):
    url     = 'http://odds.500.com/fenxi/ouzhi-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    #index_r = re.compile(r'0">(.*)</td>|0" class="">(.*)</td>')
    content_r = re.compile(company+r'<span class="gray">(.*)')
    #content_r = re.compile(r'(.*)'+company)
    real_content = content_r.findall(content.replace('\r','').replace('\n',''))
    #print real_content
    index_r   = re.compile(r'style="cursor:pointer" >(.*?)</td>\t')
    #index_r   = re.compile(r'style="cursor:pointer" >(.*)</td>\t              <td row="1" width="33.3%"  klfc="0.12"   onclick="OZ.r(this)" style="cursor:pointer" >(.*)</td>\t              <td row="1"   klfc="14.41" \t\t\t   onclick="OZ.r(this)" style="cursor:pointer" >(.*)</td>\t            </tr>\t            <tr>\t              <td row="1" width="33.3%"  klfc="1.12" class="" onclick="OZ.r(this)" style="cursor:pointer" >(.*)</td>\t              <td row="1" width="33.3%"  klfc="3.38" class="bg-a" onclick="OZ.r(this)" style="cursor:pointer" >(.*)</td>\t              <td row="1" klfc="36.28"                class="bg-b" onclick="OZ.r(this)" style="cursor:pointer" >(.*)</td>')
    #res_r     = re.compile(r'<strong>(.*):(.*)</strong>')
    if real_content==[]:
    	return 0
    indexes = index_r.findall(real_content[0])[0:6]
    #print indexes
    #res     = res_r.findall(content)
    # if len(res)<1:
    #    return 0
    # if len(res[0])<2:
    #    return 0   
    if len(indexes)<1:
       return 0   
    return indexes

def makeOddsOne(match_id,company):
    info = getAppointOdds(match_id,company)
    if info==0:return 0
    DataX=np.float64(np.array(info))[0:3]-np.float64(np.array(info))[3:6]
    #DataX=(np.dot((np.float64(np.array(info[0]))[0:3]-np.float64(np.array(info[0]))[3:6]),10)/np.float64(np.array(info[0]))[3:6])
    #DataY=WDL(np.int32(np.array(info[1]))[0]-np.int32(np.array(info[1]))[1])
    return DataX

def notEm(turArr):
    Arr=[]
    for tur in turArr:
        for m in tur:
            if m != '':
               Arr.append(m)    
    return Arr           

def notEm_Aodds(turArr):
    Arr=[]
    for tur in turArr:
        for m in tur:
            if m != '' and not(('手' in m) or ('球' in m)):
               Arr.append(m)    
    return Arr           


def notEm_x(turArr):
    Arr = []
    for tur in turArr:
        for m in tur:
            if m != '' and not('ref' in m):
               Arr.append(m.replace('<font color="red">','').replace('<font color="blue">','').replace('</font>',''))    
    return Arr           

#---------------------------------------------------
#http://odds.500.com/fenxi/daxiao-697026.shtml
def getBslot(match_id):
    #bs_url     = 'http://odds.500.com/fenxi/daxiao-'+str(match_id)+'.shtml'
    bs_odds    = getBsodds_test(match_id)   #1*20
    bs_num     = getBsLotnum_test(match_id) #1*10
    return (bs_odds,bs_num)

def getBsodds_test(match_id):    
    url     = 'http://odds.500.com/fenxi/daxiao-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    index_r = re.compile(r'class="ying">(.*)</td>|class="ping">(.*)</td>|class="shu">(.*)</td>|class="">(.*)</td>')
    indexes = notEm_Aodds(index_r.findall(content)[0:20])
    return indexes


def getBsLotnum_test(match_id):
	#class="tb_tdul_pan ying">
	#class="tb_tdul_pan ">
    url     = 'http://odds.500.com/fenxi/daxiao-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    #index_r = re.compile(r'0">(.*)</td>|0" class="">(.*)</td>')
    index_r = re.compile(r'class="tb_tdul_pan ">(.*)</td>|class="tb_tdul_pan ying">(.*)</td>|class="tb_tdul_pan ping">(.*)</td>')
    indexes = notEm(index_r.findall(content)[0:10])
    return indexes

#-------------------------------------------------
#http://odds.500.com/fenxi/ouzhi-697026.shtml
def getKelly(match_id):
    #kelly_url  = 'http://odds.500.com/fenxi/ouzhi-'+str(match_id)+'.shtml'    
    kelly_index = getKellyindex_test(match_id) #1*6
    back_lot    = getBacklot_test(match_id)    #1*2
    return (kelly_index,back_lot)

def getKellyindex_test(match_id):
	#<td row="1" class="" width="33.3%" >0.91</td>
    #<td row="1" class="">0.94</td>
    url     = 'http://odds.500.com/fenxi/ouzhi-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    index_r = re.compile(r'<td row="1" class="" width="33.3%" >(.*)</td>|<td row="1" class="">(.*)</td>|<td row="1" width="33.3%"  class=" ying">(.*)</td>|<td row="1" width="33.3%"  class=" ping">(.*)</td>|<td row="1"  class=" ping">(.*)</td>|<td row="1"  class=" ying">(.*)</td>')
    #print index_r.findall(content)[0:6]
    indexes = notEm(index_r.findall(content)[0:6])
    return indexes

def getBacklot_test(match_id):
    #<td row="1">88.53%</td>
    url     = 'http://odds.500.com/fenxi/ouzhi-'+str(match_id)+'.shtml'
    content = spider.url_get(url,"gb2312")
    index_r = re.compile(r'<td row="1">(.*)%</td>')
    indexes = index_r.findall(content)[0:2]
    return indexes

def printArr(Arr):
	for m in Arr:
		print m

if __name__ == '__main__':
    #print getBetfair_test(sys.argv[1])
    #print getBetfairSug_test(sys.argv[1])
    #print getBosswl_test(sys.argv[1])
    #printArr(getAsiaOdds_test(sys.argv[1]))
    #printArr(getAsiaLotnum_test(sys.argv[1]))
    #printArr(getBsodds_test(sys.argv[1]))
    #printArr(getBsLotnum_test(sys.argv[1]))
    #printArr(getKellyindex_test(sys.argv[1]))
    #printArr(getBacklot_test(sys.argv[1]))
    #printArr(getOriAndNowOdds(sys.argv[1]))
    #print getOriAndNowOdds_Res(sys.argv[1])
    print getAppointOddsAndRes(sys.argv[1],'威廉希尔')