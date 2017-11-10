#include <string>
#include <boost/date_time.hpp>
#include <hiredis/hiredis.h>

//g++ -o testredis testredis.cpp -L/usr/local/lib -lhiredis

using namespace std;
using namespace boost;

int main(int argc, char const *argv[])
{
	/* code */
	shared_ptr<redis::client> cli;
	sting value;
	value = cli->get("user");
	cout<<value<<endl;
	return 0;
}