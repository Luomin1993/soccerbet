#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
#import matplotlib.pyplot as plt
import spider
import portfoliomodel
import time
import sys
import os
import spiderForMarket as fm
import TestMarket as test
import datetime
from sklearn.datasets import make_multilabel_classification
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelBinarizer
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import CCA
import re
from progressbar import *

today = datetime.datetime.now()

def makeDataXY(days):
    #663195~663195
    match_ids = spider.crawl_match_list_by_date(str(today.year) + "-" + str(today.month) + "-" + str(today.day-days))
    DataX = []
    DataY = []
    for match_id in match_ids:
        info = fm.getOriAndNowOdds_Res(match_id)
        if info==0:continue
        #DataX.append(np.float64(np.array(info[0]))[0:3]-np.float64(np.array(info[0]))[3:6])
        DataX.append(np.dot((np.float64(np.array(info[0]))[0:3]-np.float64(np.array(info[0]))[3:6]),10)/np.float64(np.array(info[0]))[3:6])
        DataY.append(WDL(np.int32(np.array(info[1]))[0]-np.int32(np.array(info[1]))[1]))    
    return (DataX,DataY)

def makeDataXYtrain(day1,day2):
    #663195~663195
    #match_ids = spider.crawl_match_list_by_date(str(today.year) + "-" + str(today.month) + "-" + str(today.day-days))
    DataX = []
    DataY = []
    for day in range(day1,day2):
        match_ids = spider.crawl_match_list_by_date(str(today.year) + "-09-" + str(day))
        print '当天共'+str(len(match_ids))+'场比赛,正在下载...'
        pbar = ProgressBar().start();i=1;total=len(match_ids);
        for match_id in match_ids:
            info = fm.getAppointOddsAndRes(match_id,'Bet365')
            if info==0:continue
            pbar.update(int(100*(float(i)/total)))
            DataX.append(np.float64(np.array(info[0]))[0:3]-np.float64(np.array(info[0]))[3:6])
            #DataX.append(np.dot((np.float64(np.array(info[0]))[0:3]-np.float64(np.array(info[0]))[3:6]),10)/np.float64(np.array(info[0]))[3:6])
            DataY.append(WDL(np.int32(np.array(info[1]))[0]-np.int32(np.array(info[1]))[1]))    
            i+=1
        pbar.finish()    
    return (DataX,DataY)

#涵盖了初赔变赔的数据
#2017.10.18
#数据:X=[...,[match_id,Ps1,Ps2,Ps3,Pc1,Pc2,Pc3],...];Y=[...,[Gh,Ga],...];
def makeDataXYtrain_sc(day1,day2):
    #663195~663195
    #match_ids = spider.crawl_match_list_by_date(str(today.year) + "-" + str(today.month) + "-" + str(today.day-days))
    DataX = []
    DataY = []
    for day in range(day1,day2):
        match_ids = spider.crawl_match_list_by_date(str(today.year) + "-09-" + str(day))
        print '当天共'+str(len(match_ids))+'场比赛,正在下载...'
        pbar = ProgressBar().start();i=1;total=len(match_ids);
        for match_id in match_ids:
            info = fm.getAppointOddsAndRes(match_id,'Bet365')
            if info==0:continue
            pbar.update(int(100*(float(i)/total)))
            DataX.append([match_id]+info[0])
            #DataX.append(np.dot((np.float64(np.array(info[0]))[0:3]-np.float64(np.array(info[0]))[3:6]),10)/np.float64(np.array(info[0]))[3:6])
            DataY.append([np.int32(np.array(info[1])[0]),np.int32(np.array(info[1])[1])])    
            i+=1
        pbar.finish()    
    return (DataX,DataY)    

def makeDataXYtrain_forPsql(day1,day2,company):
    Lines = []
    for day in range(day1,day2):
        match_ids = spider.crawl_match_list_by_date(str(today.year) + "-09-" + str(day))
        print '当天共'+str(len(match_ids))+'场比赛,正在下载...'
        pbar = ProgressBar().start();i=1;total=len(match_ids);
        for match_id in match_ids:
            info = fm.getAppointOddsAndRes(match_id,company)
            if info==0:continue
            pbar.update(int(100*(float(i)/total)))
            #DataX.append([match_id]+info[0])
            #DataX.append(np.dot((np.float64(np.array(info[0]))[0:3]-np.float64(np.array(info[0]))[3:6]),10)/np.float64(np.array(info[0]))[3:6])
            #DataY.append([np.int32(np.array(info[1])[0]),np.int32(np.array(info[1])[1])])
            m_macth = spider.get_match(match_id)
            Lines.append(tuple([match_id]+info[0]+[info[1][0],info[1][1]]+[m_macth.host_team,m_macth.guest_team,m_macth.match_name,company,m_macth.match_time]))
            i+=1
        pbar.finish()    
    return Lines 

def saveOddsData():
    pass

def makeDataOne(match_id):
    info = fm.getAppointOddsAndRes(match_id,'威廉希尔')
    if info==0:return 0
    DataX=np.float64(np.array(info[0]))[0:3]-np.float64(np.array(info[0]))[3:6]
    #DataX=(np.dot((np.float64(np.array(info[0]))[0:3]-np.float64(np.array(info[0]))[3:6]),10)/np.float64(np.array(info[0]))[3:6])
    #DataY=WDL(np.int32(np.array(info[1]))[0]-np.int32(np.array(info[1]))[1])
    return DataX

def makeOddsOne_sf_356(match_id):
    info = fm.getAppointOdds(match_id,'Bet365')
    if info==0:return 0
    DataX=np.float64(np.array(info))[0:6]
    return DataX

def makeOddsOne(match_id):
    info = fm.getAppointOdds(match_id,'Bet365')
    if info==0:return 0
    DataX=np.float64(np.array(info))[0:3]-np.float64(np.array(info))[3:6]
    #DataX=(np.dot((np.float64(np.array(info[0]))[0:3]-np.float64(np.array(info[0]))[3:6]),10)/np.float64(np.array(info[0]))[3:6])
    #DataY=WDL(np.int32(np.array(info[1]))[0]-np.int32(np.array(info[1]))[1])
    return DataX

def WDL(num):
    if num==0:
       return 0
    return num/abs(num)   

def SVMclassifer():
    #(DataX,DataY) = makeDataXY(2)
    clf = SVC()
    #(C=1.0, cache_size=200, class_weight=None, coef0=0.0,decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',max_iter=-1, probability=False, random_state=None, shrinking=True,tol=0.001, verbose=False)
    (X,y)=makeDataXY(2)
    print 'Data Num: '+str(len(y))
    clf.fit(X,y)
    (X,y)=makeDataXY(3)
    print 'Data Num: '+str(len(y))
    clf.fit(X,y)
    return clf

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
    indexes = index_r.findall(real_content[0])[0:6]
    #print indexes
    #res     = res_r.findall(content)
    # if len(res)<1:
    #    return 0
    # if len(res[0])<2:
    #    return 0   
    if len(indexes)<1:
       return 0   
    DataX=np.float64(np.array(indexes))[0:3]-np.float64(np.array(indexes))[3:6]   
    return DataX
    


#test_X[:,1][:,None]
def statUpChangeWL(X,y,i,up_odd):
    x = np.array(X)[:,i][:,None]
    Indexes = np.where(x>=up_odd)[0]
    #print Indexes
    y_meet = y[Indexes]
    print y_meet
    # for index in Indexes:
    #     y_meet.append(y[index])
    length = len(y_meet)
    return [float(len(np.where(y_meet==1)))/length,float(len(np.where(y_meet==0)))/length,float(len(np.where(y_meet==-1)))/length]

def findSimilarOdds(X,y,x):
    if type(x)==int:
    	return []
    res=[]
    for i in range(len(X)):
        if abs(X[i][0]-x[0])<0.1 and abs(X[i][1]-x[1])<0.1 and abs(X[i][2]-x[2])<0.1:
           res.append(y[i])
           #print X[i]
    return res    

#from AppOddschangePre import *
#(X,y)=makeDataXYtrain(20,21)
#model.fit(X,y);py=model.predict(tX);m=py==ty;float(m.tolist().count(True))/len(ty)
def RFclassifer():
    from sklearn.ensemble import RandomForestRegressor
    regr = RandomForestRegressor(max_depth=2, random_state=0)
    (X,y)=makeDataXY(3)
    regr.fit(X, y)
    return regr    

def testClassifer(clf):
    (test_X,test_Y) = makeDataXY(1)
    #from sklearn.model_selection import cross_val_score
    from sklearn import cross_validation, metrics
    #scores = cross_val_score(clf, test_X, test_Y, cv=2)
    scores = metrics.roc_auc_score(test_Y, clf.predict(test_X[0:-1]))
    return scores

#def multiPre

if __name__ == '__main__':
    clf = SVMclassifer()
    print testClassifer(clf)
