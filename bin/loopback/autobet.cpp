#pragma GCC diagnostic error "-std=c++11"  
#include "redis.h"
#include <iostream>
#include <sstream>
#include <vector>
#include <map>
#include <algorithm>
#include <string>
#include <typeinfo>
#include <cxxabi.h>
#include <fstream>
#include <sstream>

//g++ -g autobet.cpp -o autobet -L/usr/local/lib/ -lhiredis -std=c++11

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
vector<string> m_match_ids(ids, ids+26);  


const string GetClearName(const char* name)
{
    int status = -1;
    char* clearName = abi::__cxa_demangle(name, NULL, NULL, &status);
    const char* const demangledName = (status==0) ? clearName : name;
    string ret_val(demangledName);
    free(clearName);
    return ret_val;
}


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

//---------------------------------------------------------------Auto Bet---------------------------------

vector<string> read_videos_list(const string& filename) {
    vector<string> m_match_ids;
    ifstream file(filename.c_str(), ifstream::in);
    if (!file) {
        string error_message = "No valid input file was given, please check the given filename.";
        //CV_Error(Error::StsBadArg, error_message);
    }
    string line;
    while (getline(file, line)) {
        m_match_ids.push_back(line);
    }
    return m_match_ids;
}




struct AutoBetRes
{
	string match_name;
	string match_teams;
	string match_time;
	string wdl_res;
	string bsball_res;
	string goal_res;
};

AutoBetRes AutoBet_alpha(string match_id)
{
	Redis *rd = new Redis();
	if(!rd->connect("127.0.0.1", 6379))  
    {  
        printf("connect error!\n");   
    }
    AutoBetRes abr;
    string WLDFlag     = rd->hget(match_id,"mysuggest");//cout<<WLDFlag<<endl;
	int SmaBall        = stringToNum<int>(rd->hget(match_id,"biggoal"));//cout<<SmaBall<<endl;
	int BigBall        = stringToNum<int>(rd->hget(match_id,"smagoal"));//cout<<BigBall<<endl;
	float homepregoal  = stringToNum<float>(rd->hget(match_id,"homepregoal"));//cout<<homepregoal<<endl;
	float homeprelose  = stringToNum<float>(rd->hget(match_id,"homeprelose"));//cout<<homeprelose<<endl;
	float awaypregoal  = stringToNum<float>(rd->hget(match_id,"awaypregoal"));//cout<<awaypregoal<<endl;
	float awayprelose  = stringToNum<float>(rd->hget(match_id,"awayprelose"));//cout<<awayprelose<<endl;
	int homerealgoal   = stringToNum<int>(rd->hget(match_id,"homerealgoal"));//cout<<homerealgoal<<endl;
	int awayrealgoal   = stringToNum<int>(rd->hget(match_id,"awayrealgoal"));//cout<<awayrealgoal<<endl;
	//cout << GetClearName(typeid( rd->hget(match_id,"match_name") ).name()) << endl;
	//cout << rd->hget(match_id,"match_name") << endl;
	//abr.match_name = rd->hget(match_id,"match_name");
	abr.match_teams = rd->hget(match_id,"hometeam")+" VS "+rd->hget(match_id,"awayteam");
	//abr.match_time  = rd->hget(match_id,"match_time");
	if (WLDFlag.compare("99") == 0)
		abr.wdl_res="不推荐投注胜负";
	else
	{
		if (WLDFlag.compare("h3") == 0 && (min(homepregoal,awayprelose)-min(awaypregoal,homeprelose))>=1)
			abr.wdl_res="@"+rd->hget(match_id,"hometeam")+"  -0/0.5";
		if (WLDFlag.compare("h3") == 0 && (min(homepregoal,awayprelose)-min(awaypregoal,homeprelose))>=2)
			abr.wdl_res="@"+rd->hget(match_id,"hometeam")+"  -0.5";
		if (WLDFlag.compare("h0") == 0 && (min(homepregoal,awayprelose)-min(awaypregoal,homeprelose))<=-1)
			abr.wdl_res="@"+rd->hget(match_id,"awayteam")+"  +0.5";
		if (WLDFlag.compare("h0") == 0 && (min(homepregoal,awayprelose)-min(awaypregoal,homeprelose))<=-2)
			abr.wdl_res="@"+rd->hget(match_id,"awayteam")+"  +0/0.5";
		if (WLDFlag.compare("a3") == 0 && (min(awaypregoal,homeprelose)-min(homepregoal,awayprelose))>=1)
			abr.wdl_res="@"+rd->hget(match_id,"awayteam")+"  -0/0.5";
		if (WLDFlag.compare("a3") == 0 && (min(awaypregoal,homeprelose)-min(homepregoal,awayprelose))>=2)
			abr.wdl_res="@"+rd->hget(match_id,"awayteam")+"  -0.5";
		if (WLDFlag.compare("a0") == 0 && (min(awaypregoal,homeprelose)-min(homepregoal,awayprelose))<=-1)
			abr.wdl_res="@"+rd->hget(match_id,"hometeam")+"  +0.5";
		if (WLDFlag.compare("a0") == 0 && (min(awaypregoal,homeprelose)-min(homepregoal,awayprelose))<=-2)
			abr.wdl_res="@"+rd->hget(match_id,"hometeam")+"  +0/0.5";
	}
	if (SmaBall>=2)
	{
		abr.bsball_res="@大"+to_string(SmaBall)+"球";
	}
	if (int(min(homepregoal,awayprelose))>=1)
	{
		abr.goal_res="@"+rd->hget(match_id,"hometeam")+" 大"+to_string(int(min(homepregoal,awayprelose)))+"球";
	}
	if (int(min(awaypregoal,homeprelose))>=1)
	{
		abr.goal_res+="    @"+rd->hget(match_id,"awayteam")+" 大"+to_string(int(min(awaypregoal,homeprelose)))+"球";
	}
	return abr;
}

bool VarLimit(float var1,float var2,float var3,float var4)
{
	if ((var1<0.5 && var4<0.5) || (var2<0.5 && var3<0.5))
		return true;
	return false;
}

AutoBetRes AutoBet_beta(string match_id)
{
	Redis *rd = new Redis();
	if(!rd->connect("127.0.0.1", 6379))  
    {  
        printf("connect error!\n");   
    }
    AutoBetRes abr;
    string WLDFlag     = rd->hget(match_id,"mysuggest");//cout<<WLDFlag<<endl;
	int SmaBall        = stringToNum<int>(rd->hget(match_id,"biggoal"));//cout<<SmaBall<<endl;
	int BigBall        = stringToNum<int>(rd->hget(match_id,"smagoal"));//cout<<BigBall<<endl;
	float homepregoal  = stringToNum<float>(rd->hget(match_id,"homepregoal"));//cout<<homepregoal<<endl;
	float homeprelose  = stringToNum<float>(rd->hget(match_id,"homeprelose"));//cout<<homeprelose<<endl;
	float awaypregoal  = stringToNum<float>(rd->hget(match_id,"awaypregoal"));//cout<<awaypregoal<<endl;
	float awayprelose  = stringToNum<float>(rd->hget(match_id,"awayprelose"));//cout<<awayprelose<<endl;
	float homepregoalvar = stringToNum<float>(rd->hget(match_id,"home_this_goals_var"));//cout<<homepregoalvar<<endl;
	float homeprelosevar = stringToNum<float>(rd->hget(match_id,"home_this_loses_var"));
	float awaypregoalvar = stringToNum<float>(rd->hget(match_id,"away_this_goals_var"));
	float awayprelosevar = stringToNum<float>(rd->hget(match_id,"away_this_loses_var"));
	//int homerealgoal   = stringToNum<int>(rd->hget(match_id,"homerealgoal"));//cout<<homerealgoal<<endl;
	//int awayrealgoal   = stringToNum<int>(rd->hget(match_id,"awayrealgoal"));//cout<<awayrealgoal<<endl;
	//cout << GetClearName(typeid( rd->hget(match_id,"match_name") ).name()) << endl;
	//cout << rd->hget(match_id,"match_name") << endl;
	//abr.match_name = rd->hget(match_id,"match_name");
	//cout<<"ok"<<endl;
	//abr.match_teams = rd->hget(match_id,"hometeam")+" VS "+rd->hget(match_id,"awayteam");
	//abr.match_time  = rd->hget(match_id,"match_time");
	if (WLDFlag.compare("99") == 0)
		abr.wdl_res="不推荐投注胜负";
	else
	{
		if (WLDFlag.compare("h3") == 0 && (min(homepregoal,awayprelose)-min(awaypregoal,homeprelose))>=1)
			abr.wdl_res="@"+rd->hget(match_id,"hometeam")+"  -0/0.5";
		if (WLDFlag.compare("h3") == 0 && (min(homepregoal,awayprelose)-min(awaypregoal,homeprelose))>=2)
			abr.wdl_res="@"+rd->hget(match_id,"hometeam")+"  -0.5";
		if (WLDFlag.compare("h0") == 0 && (min(homepregoal,awayprelose)-min(awaypregoal,homeprelose))<=-1)
			abr.wdl_res="@"+rd->hget(match_id,"awayteam")+"  +0.5";
		if (WLDFlag.compare("h0") == 0 && (min(homepregoal,awayprelose)-min(awaypregoal,homeprelose))<=-2)
			abr.wdl_res="@"+rd->hget(match_id,"awayteam")+"  +0/0.5";
		if (WLDFlag.compare("a3") == 0 && (min(awaypregoal,homeprelose)-min(homepregoal,awayprelose))>=1)
			abr.wdl_res="@"+rd->hget(match_id,"awayteam")+"  -0/0.5";
		if (WLDFlag.compare("a3") == 0 && (min(awaypregoal,homeprelose)-min(homepregoal,awayprelose))>=2)
			abr.wdl_res="@"+rd->hget(match_id,"awayteam")+"  -0.5";
		if (WLDFlag.compare("a0") == 0 && (min(awaypregoal,homeprelose)-min(homepregoal,awayprelose))<=-1)
			abr.wdl_res="@"+rd->hget(match_id,"hometeam")+"  +0.5";
		if (WLDFlag.compare("a0") == 0 && (min(awaypregoal,homeprelose)-min(homepregoal,awayprelose))<=-2)
			abr.wdl_res="@"+rd->hget(match_id,"hometeam")+"  +0/0.5";
	}
	if (SmaBall>=2 && VarLimit(homeprelosevar,homeprelosevar,awaypregoalvar,awayprelosevar))
	{
		abr.bsball_res="@大"+to_string(SmaBall)+"球";
	}
	if (int(min(homepregoal,awayprelose))>=1 && (homepregoalvar<0.5) && (awayprelosevar<0.5))
	{
		abr.goal_res="@"+rd->hget(match_id,"hometeam")+" 大"+to_string(int(min(homepregoal,awayprelose)))+"球";
	}
	if (int(min(awaypregoal,homeprelose))>=1 && (awaypregoalvar<0.5) && (homeprelosevar<0.5))
	{
		abr.goal_res+="  @"+rd->hget(match_id,"awayteam")+" 大"+to_string(int(min(awaypregoal,homeprelose)))+"球";
	}
	return abr;
}

void printAutoBetRes(const AutoBetRes& abr)
{
	cout<<"🔌💻 自动投注 📶"<<endl;
	cout<<"==========================="<<endl;
	//cout<<abr.match_name<<endl;
	//cout<<abr.match_time<<endl;
	//cout<<abr.match_teams<<endl;
	cout<<abr.wdl_res<<endl;
	cout<<abr.bsball_res<<endl;
	cout<<abr.goal_res<<endl;
	cout<<"==========================="<<endl;
	//cout<<" "<<endl;
	//cout<<" "<<endl;
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
	if( littleGoal>=1 && homerealgoal>=littleGoal)
		return 1;
	if( littleGoal>=1 && homerealgoal<littleGoal)
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


float Accuracy(vector<int> Vec)
{
	int right = count(Vec.begin(),Vec.end(),1);
	int wrong = count(Vec.begin(),Vec.end(),0);
	//return float(right)/Vec.size();
	return float(right)/(right+wrong);
}


//--------------- T -- E -- S -- T ---------------------
void test_AutoBet_alpha()
{
	for (vector<string>::iterator i = m_match_ids.begin(); i != m_match_ids.end(); ++i)
	{
		cout<<*i<<endl;
		string match_id = *i;
		AutoBetRes abr = AutoBet_alpha(match_id);
		printAutoBetRes(abr);
	}
}

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

void app_AutoBet_beta(string match_id)
{
    AutoBetRes abr = AutoBet_beta(match_id);
	printAutoBetRes(abr);
}


int main(int argc, char const *argv[])
{
	/* code */
	//vector<string> MatchIDVec;
	//MatchIDVec.push_back("672981");
	//test_getMultiMatchInfo(MatchIDVec);
	//test_LoopBack_alpha();
	string match_id = argv[1];
	app_AutoBet_beta(match_id);
	//test_AutoBet_alpha();
	return 0;
}
