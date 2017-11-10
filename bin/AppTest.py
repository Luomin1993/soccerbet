#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" soccer bet main function file """

__author__ = 'hanss401'

import spider
import portfoliomodel
import time
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')

m_match_ids = spider.crawl_match_list()

for m_match_id in m_match_ids:
    print m_match_id
    #m_match = spider.get_match(m_match_id)
    #m_match.display()
    #for i in range(663188,663198):
    for i in range(687512,687522):
    	os.system('python TestHABsSel.py ' + str(i) )
    	time.sleep(1)
