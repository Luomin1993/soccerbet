import numpy as np
import sys

"""team match history info class"""

__author__ = 'hanss401'

import re
import datetime
import request

class TeamInfo(object):
	"""TeamInfo: Team's history info"""
	def __init__(self):
		self.TeamName     = ""
		self.TeamWebIndex = ""
		self.TeamID       = 0
		self.TeamValue    = float(0)
		self.GoalArr      = []
		self.LostArr      = []

	def display(self):
	    print "%s\t%s\t%s\t" % (self.TeamName,self.TeamID,self.TeamValue)



		