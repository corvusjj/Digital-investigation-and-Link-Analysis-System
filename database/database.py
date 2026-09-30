import sqlite3

class Database:
    def __init__(self, database_path="investigation.db"):
        self.database_path = database_path

    def connect(self):
        return sqlite3.connect(self.database_path)

    def initialize(self):
        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                case_name TEXT NOT NULL,
                case_type TEXT,
                description TEXT,
                date_opened TEXT,
                date_closed TEXT,
                status TEXT,
                investigator TEXT,
                date_created TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()