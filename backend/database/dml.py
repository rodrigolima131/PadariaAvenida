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
        try:
            self.conn.execute(
                "INSERT INTO Clientes (nome, cpf, telefone) VALUES (?, ?, ?)",
                (cliente.nome, cliente.cpf, cliente.telefone)
            )
            self.conn.commit()
        except Exception as err:
            logging.critical(type(err), err)

    def delete_client(self, _id: int):
        try:
            self.conn.execute("DELETE FROM Clientes WHERE ID = ?", str(_id))
            self.conn.commit()
        except Exception as err:
            logging.critical(type(err), err)

    def edit_client(self, set_query, where):
        query = f"UPDATE Clientes SET {set_query} WHERE {where}"
        try:
            self.conn.execute(query)
            self.conn.commit()
        except Exception as err:
            logging.critical(type(err), err)
