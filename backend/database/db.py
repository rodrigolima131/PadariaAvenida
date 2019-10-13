import sqlite3
from sqlite3 import Error
import os
import logging


class Database:
    def __init__(self, path="database/app.db"):
        self.path = path
        if not self._db_exists():
            self._migrate()
            self._create_master_admin()
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

        conn.execute('''
            CREATE TABLE IF NOT EXISTS Clientes
             (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                telefone TEXT NOT NULL
             );
         ''')

        conn.commit()
        conn.close()

    def _create_master_admin(self):
        conn = self.create_connection()

        conn.execute("""
            INSERT INTO Usuarios (username, password, role) VALUES ('padoca', 'admin123', 'master')
        """)

        conn.commit()

        conn.close()


if __name__ == '__main__':
    try:
        db = Database("app.db").create_connection()
        user_values = [
            ('ADMIN', 'ADMIN', 'admin'),
            ('USER', 'USER', 'user')
        ]
        db.executemany("""
            INSERT INTO Usuarios (username, password, role) VALUES (?, ?, ?)
        """, user_values)

        db.execute("""INSERT INTO Clientes (nome, cpf, telefone) VALUES ('Nome', '123.456.789-00', '(11) 4444-0000')""")
        db.commit()
    except Exception as err:
        print(err, type(err))

