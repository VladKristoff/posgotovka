import psycopg2

class DbManager:
    def __init__(self):
        pass
    def connect(self):
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="1234",
            database="UrokiDB",
            port="5432",
        )

        return conn

db_manager = DbManager()