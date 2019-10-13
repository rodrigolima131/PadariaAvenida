import sqlite3
from sqlite3 import Error
import os
import logging


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class Database:
    def __init__(self, path="database/app.db"):
        self.path = path
        if not self._db_exists():
            self._migrate()
            self._create_master_admin()
            logging.info("Database was successful created!!")

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

        conn.execute('''
            CREATE TABLE IF NOT EXISTS Produtos
             (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                produto TEXT NOT NULL,
                valor DOUBLE NOT NULL,
                unidade TEXT NOT NULL
             );
         ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS Estoque
             (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER,
                quantidade INTEGER,
                FOREIGN KEY (produto_id) REFERENCES Produtos(ID)
            );
        ''')

        conn.commit()
        conn.close()
        logging.info("  Tables created...")

    def _create_master_admin(self):
        conn = self.create_connection()

        # TODO get values from environment or input from the user
        conn.execute("""
            INSERT INTO Usuarios (username, password, role) VALUES ('padoca', 'admin123', 'master')
        """)

        conn.commit()
        conn.close()
        logging.info("  Master admin created...")


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

        produtos_values = [
            ('Coca-Cola 2l', 10.50, 'Unidade'),
            ('Pão Francês', 9.40, 'Kg')
        ]
        db.executemany("""
            INSERT INTO Produtos (produto, valor, unidade) VALUES (?, ?, ?)
        """, produtos_values)

        db.execute("""INSERT INTO Estoque (produto_id, quantidade) VALUES (1, 100)""")

        db.commit()
        db.close()
    except Exception as err:
        logging.critical(err, type(err))
