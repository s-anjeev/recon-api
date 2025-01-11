from utils import database_connetion

class LoginModel:
    def __init__(self):
         # Instantiate the db_conn class
        db_connection = database_connetion.db_conn()

        # Access the connection and cursor
        self.conn = db_connection.conn
        self.cur = db_connection.cur
        

    def user_login(self,email, password_hash):
        query = "SELECT role,user_id,email FROM Users where email = %s and password_hash = %s"
        self.cur.execute(query, (email,password_hash))

        result = self.cur.fetchone()  # Fetch the first result
        return result
    
    def user_status(self,user_id):
        query = "UPDATE Users SET status = 'active' WHERE user_id = %s"
        self.cur.execute(query,(user_id))
        self.conn.commit()  # Commit the transaction to save changes
