#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" soccer bet main function file """

__author__ = 'ggstar'

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
    m_match = spider.get_match(m_match_id)
    m_match.display()
    os.system('python AppStatic.py ' + str(m_match_id) )
    time.sleep(4)
