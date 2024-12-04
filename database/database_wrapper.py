import sqlite3

class DatabaseWrapper:
    def __init__(self, db_url = "database/app_data.db"):
        self.conn = sqlite3.connect(db_url)
        self.conn.row_factory = sqlite3.Row  # Allows dictionary-style access
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise e

    def fetch_one(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise e

    def fetch_all(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise e

    def close(self):
        self.conn.close()
