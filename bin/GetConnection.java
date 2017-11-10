import java.sql.*;
public class GetConnection {
	public static void main(String[] args) {
		try{
			Class.forName("com.mysql.jdbc.Driver");
			System.out.println("MySQL java successful");
		}catch (ClassNotFoundException e1) {
			System.out.println("MySQL java failed");
			e1.printStackTrace();
		}
		String url = "jdbc:mysql://master_o:3306/mysql";
		Connection conn;
		try{
			conn = DriverManager.getConnection(url,"root","1993");
			Statement stmt = conn.createStatement();
			System.out.println("DB Connection successful");
			stmt.close();
			conn.close();
		}catch(SQLException e){
			e.printStackTrace();
		}
	}
}