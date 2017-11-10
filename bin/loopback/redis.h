#ifndef _REDIS_H_  
#define _REDIS_H_  
  
#include <iostream>  
#include <string.h>  
#include <string>  
#include <stdio.h>  
  
#include <hiredis/hiredis.h>  
  
class Redis  
{  
public:  
  
    Redis(){}  
  
    ~Redis()  
    {  
        this->_connect = NULL;  
        this->_reply = NULL;               
    }  
  
    bool connect(std::string host, int port)  
    {  
        this->_connect = redisConnect(host.c_str(), port);  
        if(this->_connect != NULL && this->_connect->err)  
        {  
            printf("connect error: %s\n", this->_connect->errstr);  
            return 0;  
        }  
        return 1;  
    }  
  
    std::string get(std::string key)  
    {  
        this->_reply = (redisReply*)redisCommand(this->_connect, "GET %s", key.c_str());  
        std::string str = this->_reply->str;  
        freeReplyObject(this->_reply);  
        return str;  
    }  
  
    void set(std::string key, std::string value)  
    {  
        redisCommand(this->_connect, "SET %s %s", key.c_str(), value.c_str());  
    }

    void hset(std::string key,std::string field,std::string value)
    {
        redisCommand(this->_connect, "MSET %s:%s %s",key.c_str(),field.c_str(),value.c_str());
    }  

    std::string mget(std::string key,std::string field)
    {
        this->_reply = (redisReply*)redisCommand(this->_connect, "MGET %s:%s",key.c_str(),field.c_str());  
        //std::cout<<*(this->_reply->element[0]->str)<<std::endl;
        std::string str = this->_reply->element[0]->str;  
        //std::cout<<"OK"<<std::endl;
        freeReplyObject(this->_reply);  
        return str; 
    }

    std::string hget(std::string key,std::string field)
    {
        this->_reply = (redisReply*)redisCommand(this->_connect, "HGET %s %s",key.c_str(),field.c_str());  
        //std::cout<<*(this->_reply->element[0]->str)<<std::endl;
        //std::string str = this->_reply->element[0]->str;
        std::string str = this->_reply->str;  
        //std::cout<<"OK"<<std::endl;
        freeReplyObject(this->_reply);  
        return str; 
    }
  
private:  
  
    redisContext* _connect;  
    redisReply* _reply;  
                  
};  
  
#endif  //_REDIS_H_  