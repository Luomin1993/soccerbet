#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""try using the apis of soccerbet"""

__author__ = 'hanss401'

import spider
import portfoliomodel
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')

m_match_ids = spider.crawl_match_list()

print len(m_match_ids)
match_id = m_match_ids[0]
print match_id

one_match = spider.get_match(match_id)

print len(one_match.item_arr)
for i in range(0,len(one_match.item_arr)):
	#print one_match.item_arr[i].l_odds
        print one_match.item_arr[i].cl_odds

print one_match.host_team
print one_match.match_name
print one_match.match_time

