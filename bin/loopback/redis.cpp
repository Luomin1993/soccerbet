#include "redis.h"  
#include <iostream>
#include <sstream>

using namespace std;

template <class Type>  
Type stringToNum(const string& str)
{  
    istringstream iss(str);  
    Type num;  
    iss >> num;  
    return num;      
}  


int main()  
{  
    Redis *r = new Redis();  
    if(!r->connect("127.0.0.1", 6379))  
    {  
        printf("connect error!\n");  
        return 0;  
    }  
    r->hset("698185","odd","1.38");  
    //printf("Get the odd is %s\n", r->get("name").c_str());  
    //cout<<"OK"<<endl;
    cout<<"Get the odd is "<<stringToNum<float>(r->mget("698185","odd"))<<endl;
    cout<<"Feng xiao is "<<r->hget("user","eric")<<endl;
    delete r;  
    return 0;  
}  