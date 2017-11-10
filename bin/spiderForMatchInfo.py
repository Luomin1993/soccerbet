#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import spider
import re
import portfoliomodel
import time
import sys
reload(sys)

__author__ = 'hanss401'

def get_MatchInfo(match_id):
	one_match = spider.get_match(match_id)
	return one_match

def get_MatchInfo_test():
	match_id = 647947
	print get_MatchInfo(match_id)

if __name__ == '__main__':
	get_MatchInfo_test()	