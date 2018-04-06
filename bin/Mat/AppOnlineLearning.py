#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" use to learn the data from matches , give judge """

__author__ = 'hanss401'

import re
import numpy
import sys
sys.path.append('../')
import spiderForMarket as sfm
import sys
import spider

def in_the_file(match_id,path):
    with open(path,'r') as foo:
        for line in foo.readlines():
            if match_id in line.replace('\n',''):
               return True;
    return False;    


def get_match_mat(path,match_id):
    f = open(path);
    text = f.readlines();
    if not in_the_file(match_id,path):
       return 0;
    start_pos = text.index(match_id+'\n');
    arr = []
    for line in text[start_pos+1:start_pos+10]:
        for num in line.replace('\n','').split(","):
            if num == '-': 
               arr.append(0);
               continue;
            arr.append(float(num));
    return arr;           

def test_get_match_mat():
    path = './Mat.csv';
    print get_match_mat(path,'719404');
    print len(get_match_mat(path,'719404'));



def get_match_res(match_id):
    m_match    = spider.get_match(match_id);
    match_url  = 'http://odds.500.com/fenxi/shuju-'+ str(match_id) +'.shtml';
    goal_res_r = re.compile(r'<strong>(.*):(.*)</strong>');
    content    = spider.url_get(match_url,"gb2312");
    goal_res   = goal_res_r.findall(content);
    if len(goal_res)==0:
       return 0;
    res        = [float(goal_res[0][0]),float(goal_res[0][1])];
    return res;

def test_get_match_res():
    print get_match_res('719404');

def write_2dArrs_into_csv(path,mat):
    import csv;
    csvfile = file(path,'a+');
    writer  = csv.writer(csvfile);
    for line in mat:
        writer.writerow(line);
    csvfile.close();

def make_train_data():
    f = open('./mat.csv');
    matchids = [];
    for line in f.readlines():
        if re.match(r'\d{6}',line):
           matchids.append(line.replace('\n',''));
    train_data_lines = [];
    for match_id in matchids:
    	match_res = get_match_res(match_id);
    	if match_res==0:
    	   continue;
        train_data_lines.append(get_match_mat('./mat.csv',match_id) + match_res);
    write_2dArrs_into_csv('goal_data.csv',train_data_lines);


def test_make_train_data():
    make_train_data();

def online_learning(new_x,old_model_path):
    pass;

def offline_learning(X,y,model):
    pass;    



if __name__ == '__main__':
    #test_get_match_mat();    
    #test_get_match_res();
    test_make_train_data();
