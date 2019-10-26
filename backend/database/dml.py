from backend.database.db import Database
from backend.database.schema import Cliente
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

    def insert_client(self, cliente: Cliente):
        self.conn.execute(
            "INSERT INTO Clientes (nome, cpf, telefone) VALUES (?, ?, ?)",
            (cliente.nome, cliente.cpf, cliente.telefone)
        )
        self.conn.commit()

    def delete_client(self, _id: int):
        self.conn.execute("DELETE FROM Clientes WHERE ID = ?", str(_id))
        self.conn.commit()
