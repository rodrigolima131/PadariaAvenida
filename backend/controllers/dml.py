from backend.database.db import Database
from backend.database.schema import Cliente
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class DML:
    def __init__(self):
        self.conn = Database().create_connection()
        self.query_comanda_exists = """
        SELECT * FROM Comandas 
        WHERE cliente_id = {} 
            AND fim IS NULL 
            AND data_comanda = '{}';
        """

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

    def find_client(self, where):
        try:
            execute = self.conn.execute(f"SELECT * FROM Clientes WHERE {where}")
            fetch = execute.fetchone()
            return {k[0]: v for k, v in list(zip(execute.description, fetch))}
        except Exception as e:
            logging.critical(e, type(e))
            return {}

    ##############################################
    #                  Comandas                  #
    ##############################################
    def insert_comanda(self, cliente_id: str, inicio: str, data_comanda: str):
        try:
            verify = self.conn.execute(
                self.query_comanda_exists.format(cliente_id, data_comanda)
            )
            if not verify.fetchone():
                self.conn.execute(
                    "INSERT INTO Comandas (cliente_id, inicio, data_comanda) VALUES (?, ?, ?)",
                    (cliente_id, inicio, data_comanda)
                )
                self.conn.commit()
        except Exception as err:
            logging.critical(type(err), err)

    def delete_comanda(self, cliente_id: int, data_comanda: str):
        try:
            self.conn.execute(
                f"DELETE FROM Comandas WHERE cliente_id = {str(cliente_id)} AND data_comanda = '{data_comanda}' AND fim IS NULL"
            )
            self.conn.commit()
        except Exception as err:
            logging.critical(type(err), err)

    def find_active_comanda_by_client_id(self, cliente_id: int, data_comanda: str):
        try:
            execute = self.conn.execute(
                "SELECT ID FROM Comandas WHERE cliente_id = {} AND fim IS NULL and data_comanda = '{}'".format(
                    cliente_id, data_comanda
                )
            )
            fetch = execute.fetchone()
            return fetch
        except Exception as err:
            logging.critical(err, type(err))
            return None
