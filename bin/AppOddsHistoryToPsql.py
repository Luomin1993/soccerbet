#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2 as ps
import AppOddschangePre as oc
import pickle
import numpy as np

def insertIntoOddsdata(table_name,match_id,ps1,ps2,ps3,pf1,pf2,pf3,goal1,goal2,team1,team2,league,company,match_time,cur):
    Str = "INSERT INTO "+table_name+" ( match_id,ps1,ps2,ps3,pf1,pf2,pf3,goal1,goal2,team1,team2,league,company,match_time) VALUES ("+match_id+","+ps1+","+ps2+","+ps3+","+pf1+","+pf2+","+pf3+","+goal1+","+goal2+",'"+team1+"','"+team2+"','"+league+"','"+company+"','"+match_time+"');"
    cur.execute(Str)


def app_save():
    conn = ps.connect(database="oddsdata", user="postgres", password="123", host="127.0.0.1", port="5432")
    print 'Open successful'
    cur = conn.cursor()
    companies    = ['Bet365','澳门','威廉希尔','伟德','Bwin']
    companies_en = ['oddsdata_bet365','oddsdata_maqu','oddsdata_wh','oddsdata_wedd','oddsdata_bwin']
    days         = [(15,17),(17,19),(19,21),(21,26),(27,30)]
    for i in range(len(companies)):
        for day_circle in days:
            (day1,day2) = day_circle
            Lines = oc.makeDataXYtrain_forPsql(day1,day2,companies[i])
            filename = 'oddsdata/'+companies_en[i]+str(day1)+'-'+str(day2)+'.pkl'
            output = open(filename, 'wb')
            pickle.dump(Lines, output)
            output.close()
            # for line in Lines:
            #     (match_id,ps1,ps2,ps3,pf1,pf2,pf3,goal1,goal2,team1,team2,league,company,match_time)=line
            #     insertIntoOddsdata(companies_en[i],match_id,ps1,ps2,ps3,pf1,pf2,pf3,goal1,goal2,team1,team2,league,company,match_time,cur)
            print 'finished:'+companies[i]+' '+str(day1)+'->'+str(day2)    
    return 0

def app_toSql():
        conn = ps.connect(database="oddsdata", user="postgres", password="123", host="127.0.0.1", port="5432")
        print 'Open successful'
        cur = conn.cursor()
        #cur.execute('\encoding GBK')
        companies    = ['Bet365']
        companies_en = ['oddsdata_bet365']
        days         = [(15,17),(17,19),(19,21),(21,26),(27,30)]
        for i in range(len(companies)):
                for day_circle in days:
                        (day1,day2) = day_circle
                        #Lines = oc.makeDataXYtrain_forPsql(day1,day2,companies[i])
                        filename = 'oddsdata/'+companies_en[i]+str(day1)+'-'+str(day2)+'.pkl'
                        pkl_file = open(filename, 'rb')
                        Lines = pickle.load(pkl_file)
                        for line in Lines:
                            (match_id,ps1,ps2,ps3,pf1,pf2,pf3,goal1,goal2,team1,team2,league,company,match_time)=line
                            insertIntoOddsdata(companies_en[i],match_id,ps1,ps2,ps3,pf1,pf2,pf3,goal1,goal2,team1.decode("UTF-8").encode("UTF-8"),team2.decode("UTF-8").encode("UTF-8"),league.decode("UTF-8").encode("UTF-8"),company.decode("UTF-8").encode("UTF-8"),match_time[12:],cur)
                            conn.commit()
                        print 'to sql finished:'+companies[i]+' '+str(day1)+'->'+str(day2)
        conn.close()
        return 0


def test():
    conn = ps.connect(database="oddsdata", user="postgres", password="123", host="127.0.0.1", port="5432")
    print 'Open successful'
    cur = conn.cursor()
    companies    = ['Bet365','澳门','威廉希尔','伟德','Bwin']
    companies_en = ['oddsdata_bet365','oddsdata_maqu','oddsdata_wh','oddsdata_wedd','oddsdata_bwin']
    days         = [(15,20),(21,26),(27,30)]
    for i in range(len(companies)):
        for day_circle in days:
            (day1,day2) = day_circle
            Lines = oc.makeDataXYtrain_forPsql(day1,day2,companies[i])
            for line in Lines:
                print line
                #insertIntoOddsdata(companies_en[i],match_id,ps1,ps2,ps3,pf1,pf2,pf3,goal1,goal2,team1,team2,league,company,match_time,cur)    
            print 'finished:'+companies[i]+' '+str(day1)+'->'+str(day2)    
    return 0

def combine():
    companies    = ['Bet365']
    companies_en = ['oddsdata_bet365']
    days         = [(15,17),(17,19),(19,21),(21,26),(27,30)]
    Lines = []
    for i in range(len(companies)):
        for day_circle in days:
            (day1,day2) = day_circle
            filename = 'oddsdata/'+companies_en[i]+str(day1)+'-'+str(day2)+'.pkl'
            pkl_file = open(filename, 'rb')
            lines_ = pickle.load(pkl_file)
            Lines += lines_
    Num_Lines = []
    for line in Lines:
        Num_Lines.append([float(line[1]),float(line[2]),float(line[3]),float(line[4]),float(line[5]),float(line[6]),float(line[7]),float(line[8])])
    np.save("odds_365.npy",np.array(Num_Lines))                    
    return 0

def searchSimilar(match_id):
    X = oc.makeOddsOne_sf_356(match_id)
    Xs = np.load("odds_365.npy")
    for X_ in Xs:
        if similar(X,X_):
           print str(X_[6]) +' : '+ str(X_[7])+'    '+res(X_[6],X_[7]) 
    print '=========================='       

def similar(X,X_):
    if abs(X[0]-X_[0])<0.3 and abs(X[1]-X_[1])<0.3 and abs(X[2]-X_[2])<0.3 and abs(X[3]-X_[3])<0.2 and abs(X[4]-X_[4])<0.2 and abs(X[5]-X_[5])<0.2:
       return True
    return False   

def res(goal1,goal2):
    if goal1>goal2:
       return '胜'
    if goal1==goal2:
       return '平'
    return '负'        


if __name__ == '__main__':
    #app_toSql()
    #combine()
    searchSimilar('642942')
