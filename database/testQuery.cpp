#include <iostream>
#include <pqxx/pqxx>
#include <pqxx/connection>
#include <pqxx/transaction>
#include <pqxx/result>
#include <string>

using namespace pqxx;

void Process_MatchID(pqxx::result R)
{
   for (pqxx::result::size_type i = 0; i != R.size(); ++i)
        //Process(R[i]["match_id"]);
        std::cout << R[i]["match_id"].as<int>() << std::endl;  
}


int main(int argc, char **argv) {
   pqxx::connection *conn = new pqxx::connection("host=localhost dbname=oddsdata port=5432 user=postgres password=123");

   std::cout << "Creating Transaction...\n";
   pqxx::work trans(*conn, "MyTest");
   pqxx::result res;
   std::string query_s("SELECT * FROM oddsdata_ex");
   std::cout << "Executing Query '" << query_s.c_str() << "'\n";
   try {
    res = trans.exec(query_s.c_str(), "test");
    Process_MatchID(res);
    trans.commit();
   } catch ( std::runtime_error &r) {
    std::cout << r.what() << "\n";
   } catch (const std::exception &e) {
    std::cout << e.what() << "\n";
   } catch (...) {
    std::cout << "unknown exception\n";
   }

 if (conn != NULL) { delete conn; conn = NULL; }
 return 0;
}
