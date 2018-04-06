#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" use to get the likely matches """

__author__ = 'hanss401'

import re
import numpy
import spiderForMarket as sfm
import sys
import spider

def get_txt_from_cm(path):
    f = open(path);
    text = f.readlines();
    return text;

def get_path_list_cm():
	import os;
	res = [];
	for m in os.listdir('./shoot'):
		if '.cm' in m:
		   res.append('./shoot/'+m);
	return res;   


def write_txt_to_cm(path_list,path):
	r = [];
	for file in path_list:
		f = open(file);
		r+= [' ',' ']+f.readlines();
	with open(path,'w') as f:
	    for line in r:
	        f.write(line);


def test_write_to_txt_cm():
    path_list = ['./shoot/1111.cm','./shoot/1117.cm'];
    write_txt_to_cm(path_list,'./shoot/res.cm');


def Task_M2one():
	path_list = get_path_list_cm();
	write_txt_to_cm(path_list,'./shoot/res.cm');

def test_get_txt_from_cm():
    path = './shoot/1030.cm';
    txt  = get_txt_from_cm(path);
    #print txt[60:160];
    print txt.count('          \n');

#back to find a symbol and give it's index number;
def back_find(symbol,txt,index_now):
    while index_now >= 0:
        index_now -= 1;
        if txt[index_now] == symbol:
        #if fit(txt[index_now],symbol):    
            return index_now;
    return -1;#not found    

#forward to find a symbol and give it's index number;
def forward_find(symbol,txt,index_now):
    while index_now < len(txt):
        index_now += 1;
        if txt[index_now] == symbol:
        #if fit(txt[index_now],symbol):    
            return index_now;
    return -1;#not found    


def fit(text,patern):
    return re.match(patern,text);

def test_fit():
    txt = get_txt_from_cm('./shoot/1030.cm');
    for word in txt:
        #if fit(word,r'\d{3}?'):
        if fit(word,r' --- (.*) --- 置信度: (.*)'):
           print word    

#return a list which contains the matches' ID;
def find_same_dis(dis_strs,dict_dis_str):
    #dis_strs = ['--- [1,2,3] ','--- [1,2,3] '];
    #dict_dis_str = {..., '600200':['--- [1,2,3] ','--- [1,2,3] '] ,...};
    res = [];
    for key in dict_dis_str:
        if dict_dis_str[key]==dis_strs:
           res.append(key);
    return res       

# --- [ 1.  0.  0.] --- 置信度: 3
def make_dict_dis(txt):
    dict_dis_str = {};
    for i in range(len(txt)):
        if fit(txt[i],r'\d{6}'):
           #print txt[i];
           #move = 8 #to 27
           dis_strs = [];
           for move in range(8,28):
               if txt[i+move] == '          \n':
                 break;
               if fit(txt[i+move],r' --- (.*) --- 置信度: (.*)'):
                  #print txt[i+move];
                  dis_strs.append(txt[i+move].replace('\n',''));
           if len(dis_strs)>0:
              dict_dis_str[txt[i][0:6]] = dis_strs;
    return dict_dis_str;

def test_make_dict_dis():
    txt = get_txt_from_cm('./shoot/1030.cm');
    print make_dict_dis(txt);    


def give_same_match_res(dis_home,dis_away,path):                        
    txt            = get_txt_from_cm(path);
    same_match_ids = find_same_dis([dis_home,dis_away],make_dict_dis(txt));
    #print make_dict_dis(txt);
    if len(same_match_ids)>0:
       for match in same_match_ids:
           print_match_res(match);

def print_match_res(match_id):
    m_match = spider.get_match(match_id)
    match_url = 'http://odds.500.com/fenxi/shuju-'+ str(match_id) +'.shtml';
    res_r    = re.compile(r'<strong>(.*):(.*)</strong>');
    content   = spider.url_get(match_url,"gb2312");
    res       = res_r.findall(content);
    
    print m_match.match_name;
    print m_match.match_time;
    print m_match.host_team+' ' + res[0][0] +':'+ res[0][1] + ' ' + m_match.guest_team;
    print ' '


def app():
    pass


if __name__ == '__main__':
    #test_get_txt_from_cm();    
    #test_fit();
    #test_make_dict_dis();
    #test_write_to_txt_cm();
    #Task_M2one();

    dis_home = sys.argv[1];
    dis_away = sys.argv[2];
    txt_path = sys.argv[3];
    give_same_match_res(dis_home,dis_away,txt_path);


