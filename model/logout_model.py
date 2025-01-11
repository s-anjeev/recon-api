from utils import database_connetion
 
class LogoutModel:
    def __init__(self):
        # Instantiate the db_conn class
        db_connection = database_connetion.db_conn()
        # Access the connection and cursor
        self.conn = db_connection.conn
        self.cur = db_connection.cur

    def logout_model(self, user_id):
        try:
            query = "UPDATE Users SET status = 'inactive' WHERE user_id = %s"
            self.cur.execute(query, (user_id,))
            self.conn.commit()  # Commit the transaction
            if self.cur.rowcount == 1:
                print("Status updated successfully.")
                return True
            else:
                print("Failed to update the status. No matching user.")
                return False
        except Exception as e:
            print("Error during logout:", e)
            self.conn.rollback()  # Rollback the transaction in case of failure
            return False
