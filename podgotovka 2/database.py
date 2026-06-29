import psycopg2


class DbManager:
    def __init__(self):
        pass

    def connect(self):
        try:
            conn = psycopg2.connect(
                database="educore_db",
                user="postgres",
                port="5432",
                host="localhost",
                password="1234"
            )

            return conn
        except Exception as e:
            print(f"Не удалось подключиться к БД: {e}")

db_manager = DbManager()

