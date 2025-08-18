import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / 'users.db'

class DatabaseConnection:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(str(self.db_path))
        self.cursor = self.conn.cursor()
        return self.cursor

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
    with DatabaseConnection() as cursor:
        try:
            cursor.execute('SELECT * FROM users')
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print('Error querying users:', e)
