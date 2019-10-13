import sqlite3
from sqlite3 import Error
import os
import logging


class Database:
    def __init__(self, path="database/app.db"):
        self.path = path
        if not self._db_exists():
            self._migrate()
            logging.info("Database created!!")

    def create_connection(self):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(os.path.join(os.getcwd(), self.path))
        except Error as e:
            logging.error(e)
        finally:
            return conn

    def _db_exists(self):
        return os.path.exists(os.path.join(os.getcwd(), self.path))

    def _migrate(self):
        conn = self.create_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios
             (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL 
             );
         ''')

        conn.commit()
        conn.close()


if __name__ == '__main__':
    db = Database("app.db").create_connection()
    values = [
        ('ADMIN', 'ADMIN', 'admin'),
        ('USER', 'USER', 'user')
    ]
    db.executemany("""
        INSERT INTO Usuarios (username, password, role) VALUES (?, ?, ?)
    """, values)
    db.commit()

