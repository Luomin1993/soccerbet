import java.sql.*;

public class SelectTable {
    
    public static void main(String[] args){
        try{
            //调用Class.forName()方法加载驱动程序
            Class.forName("com.mysql.jdbc.Driver");
            System.out.println("成功加载MySQL驱动");
                
            String url="jdbc:mysql://master_o:3306/FootballNum";    //JDBC的URL    
            Connection conn;

            conn = DriverManager.getConnection(url,"root","1993");
            Statement stmt = conn.createStatement(); //创建Statement对象
            System.out.println("成功连接到数据库！");

            String sql = "select * from MatchPre";    //要执行的SQL
            ResultSet rs = stmt.executeQuery(sql);//创建数据对象
                System.out.println("ID"+"\t"+"WTP"+"\t"+"WLP"+"\t"+"DP"+"\t"+"LLP"+"\t"+"LTP");
                while (rs.next()){
                    System.out.print(rs.getInt(1) + "\t");
                    System.out.print(rs.getFloat(2) + "\t");
                    System.out.print(rs.getFloat(3) + "\t");
                    System.out.print(rs.getFloat(4) + "\t");
                    System.out.print(rs.getFloat(5) + "\t");
                    System.out.print(rs.getFloat(6) + "\t");
                    System.out.println();
                }
                rs.close();
                stmt.close();
                conn.close();
            }catch(Exception e)
            {
                e.printStackTrace();
            }
    }
}
