#include "redis.h"
#include <iostream>
#include <sstream>
#include <vector>
#include <map>
#include <algorithm>

/*
Win/Lose/Dawn:       h3/h0/a3/a0;    No:99;
HomePreGoal:         ex:2;           No:99;
HomePreLose:         ex:1;           No:99;
AwayPreGoal:         ex:3;           No:99;
AwayPreLose:         ex:2;           No:99;
BigBall:             ex:3;           No:99;
SmaBall:             ex:1;           No:99;

*/


using namespace std;

#define RIGHT  0
#define GOLOT  1
#define GOHALF 2
#define LOSE   3
#define max(a, b)  (((a) > (b)) ? (a) : (b)) 
#define min(a, b)  (((a) < (b)) ? (a) : (b)) 

static string str[]={"web", "name", "hometeam", "awayteam", "time","homeodd","awayodd","homenum","awaynum","homepregoal","awaypregoal","homeprelose","awayprelose","biggoal","smagoal","hpl","hpd","hpw","apl","apd","apw","websuggest","mysuggest","homerealgoal","awayrealgoal"};  
vector<string> InitInfo(str, str+25);  

static string ids[]={"680435", "687526", "690074", "663914", "673311", "663589", "664279", "690072", "664805", "634206", "634204", "630823", "664282", "679013", "659270", "659273", "697040", "659269", "679019", "632260", "632256", "697042", "679016", "632263", "632261", "670530"};  
//static string ids[]={};  
vector<string> m_match_ids(ids, ids+26);  


template <class Type>  
Type stringToNum(const string& str)
{  
    istringstream iss(str);  
    Type num;  
    iss >> num;  
    return num;      
}  

template <class Type>
void printOneVec(vector<Type> Vec)
{
	for (typename vector<Type>::iterator i = Vec.begin(); i != Vec.end(); ++i)
	{
		cout<<*i<<endl;
	}
}

//positive:1;negtive:0;
//h3: home  is upBet and home win;
//a0: away  is upBet and away dawn or lose;
int WLDJudge(string WLDFlag,int homerealgoal,int awayrealgoal)
{
	if(WLDFlag.compare("h3")==0 && (homerealgoal-awayrealgoal)>0)
		return 1;
	if(WLDFlag.compare("h3")==0 && (homerealgoal-awayrealgoal)<=0)
		return 0;
	if(WLDFlag.compare("h0")==0 && (homerealgoal-awayrealgoal)>0)
		return 0;
	if(WLDFlag.compare("h0")==0 && (homerealgoal-awayrealgoal)<=0)
		return 1;
	if(WLDFlag.compare("a3")==0 && (homerealgoal-awayrealgoal)>=0)
		return 0;
	if(WLDFlag.compare("a3")==0 && (homerealgoal-awayrealgoal)<0)
		return 1;
	if(WLDFlag.compare("a0")==0 && (homerealgoal-awayrealgoal)>=0)
		return 1;
	if(WLDFlag.compare("a0")==0 && (homerealgoal-awayrealgoal)<0)
		return 0;
	return 99;
}

//positive:1;negtive:0;
int BSballJudge(int Bigball,int Smaball,int homerealgoal,int awayrealgoal)
{
	if((homerealgoal+awayrealgoal) <= Bigball && (homerealgoal+awayrealgoal) >= Smaball)
		return 1;
	return 0;
}

int BigBallJudge(int SmaBall,int homerealgoal,int awayrealgoal)
{
	if(SmaBall>=2 && (homerealgoal+awayrealgoal)>=SmaBall)
		return 1;
	if(SmaBall>=2 && (homerealgoal+awayrealgoal)<2)
		return 0;
	return 99;
}

//positive:1;negtive:0;
int GoalJudge(float homepregoal,float awayprelose,int homerealgoal)
{
	if(float(homerealgoal) <= max(homepregoal,awayprelose) && float(homerealgoal) >= min(homepregoal,awayprelose))
		return 1;
	return 0;
}

int BigGoalJudge(float littleGoal,int homerealgoal)
{
	//if( littleGoal>=1 && homerealgoal>=int(littleGoal))
	if( littleGoal>=1 && homerealgoal>=1)
		return 1;
	//if( littleGoal>=1 && homerealgoal<int(littleGoal))
	if( littleGoal>=1 && homerealgoal<1)	
		return 0;
	return 99;
}


struct LoopBackRes
{
	vector<int> wdl_res;
	vector<int> bsball_res;
	vector<int> goal_res;
};


LoopBackRes LoopBack_alpha(vector<string> m_match_ids)
{
	Redis *rd = new Redis();
	if(!rd->connect("127.0.0.1", 6379))  
    {  
        printf("connect error!\n");   
    }
    LoopBackRes lbres;
    for (vector<string>::iterator thisID = m_match_ids.begin(); thisID != m_match_ids.end(); ++thisID)
	{
		string WLDFlag     = rd->hget(*thisID,"mysuggest");//cout<<WLDFlag<<endl;
		int SmaBall        = stringToNum<int>(rd->hget(*thisID,"biggoal"));//cout<<SmaBall<<endl;
		int BigBall        = stringToNum<int>(rd->hget(*thisID,"smagoal"));//cout<<BigBall<<endl;
		float homepregoal  = stringToNum<float>(rd->hget(*thisID,"homepregoal"));//cout<<homepregoal<<endl;
		float homeprelose  = stringToNum<float>(rd->hget(*thisID,"homeprelose"));//cout<<homeprelose<<endl;
		float awaypregoal  = stringToNum<float>(rd->hget(*thisID,"awaypregoal"));//cout<<awaypregoal<<endl;
		float awayprelose  = stringToNum<float>(rd->hget(*thisID,"awayprelose"));//cout<<awayprelose<<endl;
		int homerealgoal   = stringToNum<int>(rd->hget(*thisID,"homerealgoal"));//cout<<homerealgoal<<endl;
		int awayrealgoal   = stringToNum<int>(rd->hget(*thisID,"awayrealgoal"));//cout<<awayrealgoal<<endl;
		if (WLDFlag.compare("99") != 0)
			lbres.wdl_res.push_back(WLDJudge(WLDFlag,homerealgoal,awayrealgoal));
		//lbres.bsball_res.push_back(BSballJudge(BigBall,SmaBall,homerealgoal,awayrealgoal));
		lbres.bsball_res.push_back(BigBallJudge(SmaBall,homerealgoal,awayrealgoal));
		//lbres.goal_res.push_back(GoalJudge(homepregoal,awayprelose,homerealgoal));
		//lbres.goal_res.push_back(GoalJudge(awaypregoal,homeprelose,awayrealgoal));
		lbres.goal_res.push_back(BigGoalJudge(min(homepregoal,awayprelose),homerealgoal));
		lbres.goal_res.push_back(BigGoalJudge(min(awaypregoal,homeprelose),awayrealgoal));
	}
	return lbres;
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
/*vector<int> judgeBS(vector<string> MatchIDVec)
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
}*/

/*vector<int> judgeWL(vector<string> MatchIDVec)
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
*/

float Accuracy(vector<int> Vec)
{
	int right = count(Vec.begin(),Vec.end(),1);
	int wrong = count(Vec.begin(),Vec.end(),0);
	//return float(right)/Vec.size();
	cout<<"num: "<<(right+wrong)<<endl;
	return float(right)/(right+wrong);
}


//--------------- T -- E -- S -- T ---------------------
/*void test_judgeWLAndBS(vector<string> MatchIDVec)
{
	vector<int> judgeBSRes = judgeBSRes(MatchIDVec);
	vector<int> judgeWLRes = judgeWLRes(MatchIDVec);
	cout<<judgeWLRes[0]<<endl;
	cout<<judgeBSRes[0]<<endl;
}*/


void test_LoopBack_alpha()
{
	//vector<string> m_match_ids;
	//m_match_ids.push_back("672981");
	//m_match_ids.push_back("672981");
	LoopBackRes lbres = LoopBack_alpha(m_match_ids);
	//printOneVec<int>(lbres.wdl_res);
	//printOneVec<int>(lbres.bsball_res);
	//printOneVec<int>(lbres.goal_res);
	cout<<Accuracy(lbres.wdl_res)<<endl;
	cout<<Accuracy(lbres.bsball_res)<<endl;
	cout<<Accuracy(lbres.goal_res)<<endl;
}



int main(int argc, char const *argv[])
{
	/* code */
	//vector<string> MatchIDVec;
	//MatchIDVec.push_back("672981");
	//test_getMultiMatchInfo(MatchIDVec);
	test_LoopBack_alpha();
	return 0;
}