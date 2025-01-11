from utils import database_connetion

class TrackOutput:
    def __init__(self):
        # Instantiate the db_conn class
        db_connection = database_connetion.db_conn()

        # Access the connection and cursor
        self.conn = db_connection.conn
        self.cur = db_connection.cur

    def save_results(self, input_command, output_file, timestamp):
        try:
            query = "INSERT INTO output_file_mapping(command, output_file, timestamp) VALUES(%s, %s, %s)"
            self.cur.execute(query, (input_command, output_file, timestamp))
            self.conn.commit()
            
            if self.cur.rowcount == 1:
                print("Data saved successfully.")
                return True
            else:
                print("Failed to save the data. No matching entry.")
                return False
        except Exception as e:
            print("Error during save_results:", e)
            self.conn.rollback()  # Rollback the transaction in case of failure
            return False
        finally:
            self.cur.close()
            self.conn.close()

