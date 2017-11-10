#!/bin/bash
match_id=$1
python AppToRedisMark.py $match_id
if [ $?==0 ];then   
   ./loopback/autobet $match_id
elif [ $?==1 ];then
    exit   
fi
