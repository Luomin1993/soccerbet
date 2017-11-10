#include "redis.h"
#include <iostream>
#include <sstream>
#include <vector>
#include <map>

using namespace std;

#define RIGHT  0
#define GOLOT  1
#define GOHALF 2
#define LOSE   3 


static string str[]={"web", "name", "hometeam", "awayteam", "time","homeodd","awayodd","homenum","awaynum","homepregoal","awaypregoal","homeprelose","awayprelose","biggoal","smagoal","hpl","hpd","hpw","apl","apd","apw","websuggest","mysuggest","homerealgoal","awayrealgoal"};  
vector<string> InitInfo(str, str+25);  

template <class Type>  
Type stringToNum(const string& str)
{  
    istringstream iss(str);  
    Type num;  
    iss >> num;  
    return num;      
}  

map<string,string> getInitMatchInfo()
{
	map<string,string> InitMatchInfo;
	for (vector<string>::iterator i = InitInfo.begin(); i != InitInfo.end(); ++i)
	{
		InitMatchInfo[*i] = 'no record';
	}
	return InitMatchInfo;
}

vector<map<string,string> > getMultiMatchInfo(vector<string> MatchIDVec)
{
	Redis *rd = new Redis();
	if(!rd->connect("127.0.0.1", 6379))  
    {  
        printf("connect error!\n");   
    }
	vector<map<string,string> > MultiMatchInfo;
	map<string,string> InitMatchInfo = getInitMatchInfo();
	for (vector<string>::iterator thisID = MatchIDVec.begin(); thisID != MatchIDVec.end(); ++thisID)
	{
		map<string,string> thisMatchInfo = InitMatchInfo;
		for (vector<string>::iterator thisField = InitInfo.begin(); thisField != InitInfo.end(); ++thisField)
		{
			thisMatchInfo[*thisField] = rd->hget(*thisID,*thisField);
		}
		MultiMatchInfo.push_back(thisMatchInfo);
	}
	delete rd;
	return MultiMatchInfo;
}

void test_getMultiMatchInfo(vector<string> MatchIDVec)
{
	//Input a one-dim MatchIDVec to test;
	vector<map<string,string> > MultiMatchInfo = getMultiMatchInfo(MatchIDVec);
	map<string,string>::iterator iter;
	for(iter = MultiMatchInfo[0].begin(); iter != MultiMatchInfo[0].end(); iter++)
        cout<<iter->first <<" : "<<iter->second<<endl;
}

//RIGHT,GOLOT,GOHALF,LOSE
vector<int> judgeBS(vector<string> MatchIDVec)
{
	vector<map<string,string> > MultiMatchInfo = getMultiMatchInfo(MatchIDVec);
	vector<int> judgeBSRes;
	for (vector<map<string,string> >::iterator thisMatchInfo = MultiMatchInfo.begin(); i != MultiMatchInfo.end(); ++i)
	{
		int BigGoal = stringToNum<int>(*thisMatchInfo["biggoal"]);
		int SmaGoal = stringToNum<int>(*thisMatchInfo["smagoal"]);
		int ReaGoal = stringToNum<int>(*thisMatchInfo["homerealgoal"]) + stringToNum<int>(*thisMatchInfo["awayrealgoal"]);
		if (BigGoal<ReaGoal && SmaGoal>ReaGoal)//Not Wrong! BigGoal is to predict the low limit of buying big ball;
		{
			judgeBSRes.push_back(RIGHT);
		}
		else if (BigGoal==ReaGoal || SmaGoal==ReaGoal )
		{
			judgeBSRes.push_back(GOLOT);
		}
		else if (BigGoal-ReaGoal==1 || ReaGoal-SmaGoal==1)
		{
			judgeBSRes.push_back(GOHALF);
		}
		else{judgeBSRes.push_back(LOSE);}
	}
	return judgeBSRes;
}

vector<int> judgeWL(vector<string> MatchIDVec)
{
	vector<map<string,string> > MultiMatchInfo = getMultiMatchInfo(MatchIDVec);
	vector<int> judgeWLRes;
	for (vector<map<string,string> >::iterator thisMatchInfo = MultiMatchInfo.begin(); i != MultiMatchInfo.end(); ++i)
	{
		int PreRes = stringToNum<int>(*thisMatchInfo["MySuggest"]);
		int ReaRes = stringToNum<int>(*thisMatchInfo["homerealgoal"]) - stringToNum<int>(*thisMatchInfo["awayrealgoal"]);
		if ((ReaRes>0 && PreRes==3) || (ReaRes<0 && PreRes==0))//Not Wrong! BigGoal is to predict the low limit of buying big ball;
		{
			judgeWLRes.push_back(RIGHT);
		}
		else if (ReaRes==0)
		{
			judgeWLRes.push_back(GOLOT);
		}
		else if ((ReaRes==-1 && PreRes==3) || (ReaRes==1 && PreRes==0))
		{
			judgeWLRes.push_back(GOHALF);
		}
		else{judgeWLRes.push_back(LOSE);}
	}
	return judgeWLRes;
}

void test_judgeWLAndBS(vector<string> MatchIDVec)
{
	vector<int> judgeBSRes = judgeBSRes(MatchIDVec);
	vector<int> judgeWLRes = judgeWLRes(MatchIDVec);
	cout<<judgeWLRes[0]<<endl;
	cout<<judgeBSRes[0]<<endl;
}

//--------------- TEST -----------------------------
int main(int argc, char const *argv[])
{
	/* code */
	vector<string> MatchIDVec;
	MatchIDVec.push_back("672981");
	test_getMultiMatchInfo(MatchIDVec);
	return 0;
}