# database_manager.py

import sqlite3

class DatabaseManager:
    """
    Manages database operations for storing and retrieving accomplishments.
    """
    def __init__(self, db_name="wecap.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        """Creates the accomplishments table if it does not exist."""
        query = """
        CREATE TABLE IF NOT EXISTS accomplishments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            accomplishment TEXT NOT NULL
        )
        """
        self.connection.execute(query)
        self.connection.commit()

    def add_accomplishment(self, date, accomplishment):
        """Inserts a new accomplishment into the database."""
        query = "INSERT INTO accomplishments (date, accomplishment) VALUES (?, ?)"
        self.connection.execute(query, (date, accomplishment))
        self.connection.commit()

    def get_accomplishments(self, start_date=None, end_date=None):
        """Retrieves accomplishments filtered by date range, if specified."""
        if start_date and end_date:
            query = "SELECT id, date, accomplishment FROM accomplishments WHERE date BETWEEN ? AND ? ORDER BY date DESC"
            return self.connection.execute(query, (start_date, end_date)).fetchall()
        else:
            query = "SELECT id, date, accomplishment FROM accomplishments ORDER BY date DESC"
            return self.connection.execute(query).fetchall()

    def delete_accomplishment(self, id):
        """Deletes the accomplishment with the matching id"""
        query = f"DELETE FROM accomplishments WHERE id = '{id}'"
        self.connection.execute(query)
        self.connection.commit()

