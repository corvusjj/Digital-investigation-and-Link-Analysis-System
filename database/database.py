import sqlite3
import json
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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                entity_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                category TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                label TEXT NOT NULL,
                properties TEXT,
                date_created TEXT NOT NULL,

                FOREIGN KEY (case_id)
                REFERENCES cases(case_id)
                ON DELETE CASCADE
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

    def get_case(self, case_id):
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
            WHERE case_id = ?
        """, (case_id,))

        row = cursor.fetchone()

        connection.close()

        if row is None:
            return None

        return Case(
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

    def update_case(self, case):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE cases
            SET
                case_name = ?,
                case_type = ?,
                description = ?,
                date_opened = ?,
                date_closed = ?,
                status = ?,
                investigator = ?
            WHERE case_id = ?
        """, (
            case.case_name,
            case.case_type,
            case.description,
            case.date_opened,
            case.date_closed,
            case.status,
            case.investigator,
            case.case_id
        ))

        connection.commit()
        connection.close()

    def delete_case(self, case_id):
        connection = self.connect()
        cursor = connection.cursor()
    
        cursor.execute("""
            DELETE FROM cases
            WHERE case_id = ?
        """, (case_id,))
    
        connection.commit()
        connection.close()

    def create_entity(self, entity, case_id, category):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO entities (
                entity_id,
                case_id,
                category,
                entity_type,
                label,
                properties,
                date_created
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            entity.entity_id,
            case_id,
            category,
            entity.type,
            entity.label,
            json.dumps(entity.properties),
            entity.date_created.isoformat()
        ))

        connection.commit()
        connection.close()

    def get_entities(self, case_id):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                entity_id,
                case_id,
                category,
                entity_type,
                label,
                properties,
                date_created
            FROM entities
            WHERE case_id = ?
            ORDER BY date_created DESC
        """, (case_id,))

        rows = cursor.fetchall()
        connection.close()

        entities = []

        for row in rows:
            entities.append({
                "entity_id": row[0],
                "case_id": row[1],
                "category": row[2],
                "entity_type": row[3],
                "label": row[4],
                "properties": json.loads(row[5]) if row[5] else {},
                "date_created": row[6]
            })

        return entities

    def get_entity(self, entity_id):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                entity_id,
                case_id,
                category,
                entity_type,
                label,
                properties,
                date_created
            FROM entities
            WHERE entity_id = ?
        """, (entity_id,))

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return None

        return {
            "entity_id": row[0],
            "case_id": row[1],
            "category": row[2],
            "entity_type": row[3],
            "label": row[4],
            "properties": json.loads(row[5]) if row[5] else {},
            "date_created": row[6]
        }

    def delete_entity(self, entity_id):
        connection = self.connect()
        cursor = connection.cursor()
    
        cursor.execute("""
            DELETE FROM entities
            WHERE entity_id = ?
        """, (entity_id,))
    
        connection.commit()
        connection.close()