#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pickle as pk
import random
import spiderForWedd as sw
import sys

def show(Infos):
    num_25  = 0 
    num_15  = 0
    num_10  = 0
    num_t   = float(len(Infos))
    history = []
    for info in Infos:
        if info[0][4]+info[0][5]>2.5:
           num_25+=1
           history.append('>2.5 ')
           continue
        if info[0][4]+info[0][5]>1.5:
           num_15+=1
           history.append('>1.5 ')
        if info[0][4]+info[0][5]<2:
           num_10+=1
           history.append('0-1 ')
    print  ' 场数:      '+str(num_t)       
    print  ' 大于2.5球:  '+str(num_25/num_t)
    print  ' 大于1.5球:  '+str(num_15/num_t)
    print  ' 小于1.5球:  '+str(num_10/num_t)
    print  history

def giveJudge(Infos):
    num_25 = 0 
    num_15 = 0
    num_10 = 0
    num_t  = float(len(Infos))
    for info in Infos:
        if info[0][4]+info[0][5]>2.5:
           num_25+=1
        if info[0][4]+info[0][5]>1.5:
           num_15+=1
        if info[0][4]+info[0][5]<2:
           num_10+=1
    if num_25/num_t > 0.8 and num_t-num_25<4:
        return 2.5
    if num_15/num_t > 0.8 and num_t-num_25<4:
        return 1.5
    if num_10/num_t > 0.8 and num_t-num_25<4:
        return 1
    return 0    

def giveSimilarInfos(pre_info,Datas):
    Infos = []
    for info in Datas:
        if abs(pre_info[0][0]-info[0][0])<0.03 and abs(pre_info[0][1]-info[0][1])<0.03 and abs(pre_info[0][2]-info[0][2])<0.02 and abs(pre_info[0][3]-info[0][3])<0.02 and pre_info[1][0]==info[1][0] and pre_info[1][1]==info[1][1]:
           Infos.append(info)
    return Infos       

def AppUseWedd(match_id):
    pre_info = sw.getAppointBSOddsAndRes_notstart(match_id,'伟德')
    if pre_info==0:
       return 0
    pre_info = (np.float64(np.array((pre_info[0]+pre_info[2]))),pre_info[1])
    Datas    = np.concatenate((np.load('Data_BS/WeddBS-1.npy'),np.load('Data_BS/WeddBS-2.npy'),np.load('Data_BS/WeddBS-3.npy'),np.load('Data_BS/WeddBS-4.npy'),np.load('Data_BS/WeddBS-5.npy'),np.load('Data_BS/WeddBS-6.npy'),np.load('Data_BS/WeddBS-7.npy'),np.load('Data_BS/WeddBS-8.npy'),np.load('Data_BS/WeddBS-9.npy'),np.load('Data_BS/WeddBS-10.npy'),np.load('Data_BS/WeddBS-11.npy'),np.load('Data_BS/WeddBS-12.npy'),np.load('Data_BS/WeddBS-1_18.npy'),np.load('Data_BS/WeddBS-2_18.npy') ))
    Infos    = giveSimilarInfos(pre_info,Datas)
    if len(Infos)==0:
       return 0
    show(Infos)

def AppUseWedd_s(match_id):
    pre_info = sw.getAppointBSOddsAndRes_notstart(match_id,'伟德')
    if pre_info==0:
       return 0
    pre_info = (np.float64(np.array((pre_info[0]+pre_info[2]))),pre_info[1])
    Datas    = np.concatenate((np.load('Data_BS/WeddBS-1.npy'),np.load('Data_BS/WeddBS-2.npy'),np.load('Data_BS/WeddBS-3.npy'),np.load('Data_BS/WeddBS-4.npy'),np.load('Data_BS/WeddBS-5.npy'),np.load('Data_BS/WeddBS-6.npy'),np.load('Data_BS/WeddBS-7.npy'),np.load('Data_BS/WeddBS-8.npy'),np.load('Data_BS/WeddBS-9.npy'),np.load('Data_BS/WeddBS-10.npy'),np.load('Data_BS/WeddBS-11.npy') ))
    Infos    = giveSimilarInfos_s(pre_info,Datas)
    if len(Infos)==0:
       return 0
    show(Infos)

def giveSimilarInfos_s(pre_info,Datas):
    Infos = []
    for info in Datas:
        if pre_info[0][2]==info[0][2] and pre_info[0][3]==info[0][3] and pre_info[1][1]==info[1][1]:
           Infos.append(info)
    return Infos       


def isRight(pre_info,Datas):
    #Datas = np.concatenate((np.load('WeddBS-1.npy'),np.load('WeddBS-2.npy'),np.load('WeddBS-3.npy'),np.load('WeddBS-4.npy')))
    Infos = giveSimilarInfos(pre_info,Datas)
    if len(Infos)==0:
       return 99       
    bs = giveJudge(Infos)
    if bs==0:
       return 99
    if bs==1 and pre_info[0][4]+pre_info[0][5]<2.5:
       return '10_1'
    if bs==1 and pre_info[0][4]+pre_info[0][5]>=3:
       return '10_0'
    if bs==1.5 and pre_info[0][4]+pre_info[0][5]>1.5:
       return '15_1'
    if bs==1.5 and pre_info[0][4]+pre_info[0][5]<1.5:
       return '15_0'
    if bs==2.5 and pre_info[0][4]+pre_info[0][5]>2.5:
       return '25_1'
    if bs==2.5 and pre_info[0][4]+pre_info[0][5]<2.5:
       return '25_0'
    return 99   

def stat():
    Datas    = np.concatenate((np.load('WeddBS-1.npy'),np.load('WeddBS-2.npy'),np.load('WeddBS-3.npy'),np.load('WeddBS-4.npy'),np.load('WeddBS-5.npy'),np.load('WeddBS-6.npy'),np.load('WeddBS-7.npy'),np.load('WeddBS-8.npy'),np.load('WeddBS-9.npy') ))
    PreInfos = np.load('WeddBS-10.npy')      
    Res      = []
    for pre_info in PreInfos:
        Res.append(isRight(pre_info,Datas))
    #print 'Right: '+ str(Res.count(1)) +'  '+ str(Res.count(0)) +'  '+ str(Res.count(1)/float(Res.count(1)+Res.count(0)))  
    print 'Right: '+ str(Res.count('10_1')) +'  '+ str(Res.count('10_0')) +'  '+ str(Res.count('10_1')/float(Res.count('10_1')+Res.count('10_0')))
    print 'Right: '+ str(Res.count('25_1')) +'  '+ str(Res.count('25_0')) +'  '+ str(Res.count('25_1')/float(Res.count('25_1')+Res.count('25_0')))
    print 'Right: '+ str(Res.count('15_1')) +'  '+ str(Res.count('15_0')) +'  '+ str(Res.count('15_1')/float(Res.count('15_1')+Res.count('15_0')))  


if __name__ == '__main__':
    #stat()
    AppUseWedd(sys.argv[1])
