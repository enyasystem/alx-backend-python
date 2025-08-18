import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / 'users.db'

class ExecuteQuery:
    def __init__(self, query, params=None, db_path=DB_PATH):
        self.query = query
        self.params = params or []
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(str(self.db_path))
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc, tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

if __name__ == '__main__':
    query = 'SELECT * FROM users WHERE age > ?'
    with ExecuteQuery(query, [25]) as results:
        for row in results:
            print(row)
