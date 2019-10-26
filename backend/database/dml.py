from backend.database.db import Database
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class DML:
    def __init__(self):
        self.conn = Database().create_connection()

    def destroy_me(self):
        try:
            self.conn.close()
        except Exception as err:
            logging.critical(err, type(err))

    def insert_client(self, nome: str, cpf: str, telefone: str = ""):
        self.conn.execute(
            "INSERT INTO Clientes (nome, cpf, telefone) VALUES (?, ?, ?)",
            (nome, cpf, telefone)
        )
        self.conn.commit()

    def delete_client(self, _id: int):
        self.conn.execute("DELETE FROM Clientes WHERE ID = ?", str(_id))
        self.conn.commit()
