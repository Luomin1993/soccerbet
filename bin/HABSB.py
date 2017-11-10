#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" soccer bet main function file """

__author__ = 'hanss401'

import spider
import portfoliomodel
import time
import sys
import os
import spiderForBSBall as sp

reload(sys)
sys.setdefaultencoding('utf8')

#m_match_ids = spider.crawl_match_list()
m_match_ids = sp.getAllMatches()

for m_match_id in m_match_ids:
    print m_match_id
    #m_match = spider.get_match(m_match_id)
    #m_match.display()
    os.system('python AppHABsSel.py ' + str(m_match_id) )
    time.sleep(2)
