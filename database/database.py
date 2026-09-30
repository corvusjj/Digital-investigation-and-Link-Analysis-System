import sqlite3
from models.case import Case

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

    def create_case(self, case):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO cases (
                case_id,
                case_name,
                case_type,
                description,
                date_opened,
                date_closed,
                status,
                investigator,
                date_created
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            case.case_id,
            case.case_name,
            case.case_type,
            case.description,
            case.date_opened,
            case.date_closed,
            case.status,
            case.investigator,
            case.date_created
        ))

        connection.commit()
        connection.close()

    def get_cases(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                case_id,
                case_name,
                case_type,
                description,
                date_opened,
                date_closed,
                status,
                investigator,
                date_created
            FROM cases
            ORDER BY date_created DESC
        """)

        rows = cursor.fetchall()

        connection.close()

        cases = []

        for row in rows:
            case = Case(
                case_id=row[0],
                case_name=row[1],
                case_type=row[2],
                description=row[3],
                date_opened=row[4],
                date_closed=row[5],
                status=row[6],
                investigator=row[7],
                date_created=row[8]
            )

            cases.append(case)

        return cases
