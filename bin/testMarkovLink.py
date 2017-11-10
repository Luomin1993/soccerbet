import numpy as np
import spiderForTeamInfo as netdata
import TransDataForMK as trans
import MarkovDemo as mk
import sys
import spider
import pdb

def getRes(team_url,wodd,lodd):
	content  = spider.url_get(team_url+'teamfixture',"gb2312")
	Reses    = netdata.get_TeamMatchHistory(content)
	Odds     = netdata.get_TeamOddsHistory(content)
	O1       = trans.PG_to_O(Reses)
	O2       = trans.ODD_to_O(Odds)
	I        = trans.RS_to_I(Reses)
	known_O1 = [trans.FOR(Reses[len(Reses)-2],Reses[len(Reses)-1])]
	known_O2 = [trans.OD(lodd/wodd)]
	return mk.makeAverageRes(O1,O2,I,known_O1,known_O2)


if __name__ == '__main__':
	match_id  = sys.argv[1]
	match_url = 'http://odds.500.com/fenxi/shuju-'+ str(match_id) +'.shtml'
	content   = spider.url_get(match_url,"gb2312")
	(home_url,away_url) = netdata.get_Team_url(content)
	odd_url   = 'http://odds.500.com/fenxi/ouzhi-'+ str(match_id) +'.shtml'
	content   = spider.url_get(odd_url,"gb2312")
	(wodd,lodd) = netdata.get_now_Odds(content)
	res_home = getRes(home_url,wodd,lodd)
	res_away = getRes(away_url,lodd,wodd)
	#print (res_home,res_away)
	print res_home[0]
	print res_home[1]
	print res_home[2]
	print res_away[0]
	print res_away[1]
	print res_away[2]