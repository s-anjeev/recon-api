import pymysql
# from config.config import db_config

# from config import config
db_config = {
    "host": "localhost",
    "username": "root",
    "password": "root",
    "database": "recon_api_database",
    "port": 3306
}

class db_conn:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self):
        """Establish a database connection."""
        try:
            self.conn = pymysql.connect(
                host=db_config["host"],
                user=db_config["username"],
                password=db_config["password"],
                database=db_config["database"],
                port=db_config["port"]
            )
            self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
            print("Connection established successfully")
        except pymysql.MySQLError as err:
            print(f"Error: {err}")
            self.conn = None
            self.cur = None

    def close(self):
        """Close the database connection."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Connection closed")


# db_obj = db_conn()