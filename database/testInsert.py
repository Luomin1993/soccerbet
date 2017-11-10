#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2 as ps

conn = ps.connect(database="oddsdata", user="postgres", password="123", host="127.0.0.1", port="5432")

print 'Open successful'
#cur = conn.cursor()

def insertIntoOddsdata(match_id,ps1,ps2,ps3,pf1,pf2,pf3,goal1,goal2,team1,team2,league,company,match_time,conn):
    Str = "INSERT INTO oddsdata_ex ( match_id,ps1,ps2,ps3,pf1,pf2,pf3,goal1,goal2,team1,team2,league,company,match_time) VALUES ("+match_id+","+ps1+","+ps2+","+ps3+","+pf1+","+pf2+","+pf3+","+goal1+","+goal2+",'"+team1+"','"+team2+"','"+league+"','"+company+"','"+match_time+"');"
    cur = conn.cursor()
    cur.execute(Str)
    conn.commit()
    conn.close()

insertIntoOddsdata('111001','2.11','2.12','3.11','2.12','2.01','4.11','1','2',('曼联').decode("UTF8").encode("UTF8"),'LIV','PremierLeague','wedd','2012-06-07 14:00:02.412827+08',conn)

