#!/usr/bin/python

import psycopg2

conn = psycopg2.connect(database="oddsdata",user="postgres",password="123",host="127.0.0.1",port="5432")

print "success" 
