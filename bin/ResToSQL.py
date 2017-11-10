#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb

def open_db(IP,USER,DB_PASSWD,DB_NAME):
	db = MySQLdb.connect(IP,USER,DB_PASSWD,DB_NAME)
	return db

def delete_db_form(db,DB_FORM_NAME):
	cursor = db.cursor()
	cursor.execute("DROP TABLE IF EXISTS " + DB_FORM_NAME)

def insert_db_form(db,SQL_INSERT_COMMAND):
	cursor = db.cursor()
	try:
	    cursor.execute(SQL_INSERT_COMMAND)
	    db.commit()
	except:
	    db.rollback()        
    
