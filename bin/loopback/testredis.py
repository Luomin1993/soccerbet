#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis

pool = redis.ConnectionPool(host='127.0.0.1',port=6379)
rd   = redis.StrictRedis(connection_pool=pool)

#rd.hset("eric","name")
dic={"eric":"阿用","tom":"bad"}
rd.hmset("user",dic)
print rd.hget("user","eric")
#pool.release(rd)
print rd.dbsize()